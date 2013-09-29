# Load in core dependencies
import json
import re
import subprocess
import sublime
import sublime_plugin
import tempfile


# Localize Region
Region = sublime.Region


# Define a custom RegionSet (cannot use sublime's =_=)
class RegionSet():
    def __init__(self):
        self.regions = set()

    def add(self, region):
        self.regions.add(region)

    def contains(self, needle):
        contains = False

        for haystack in self.regions:
            if haystack.contains(needle):
                contains = True

        return contains


# Define a deletion command
class JsVarDeleteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # If the view is not JavaScript, perform the default
        view = self.view
        if view.settings().get('syntax') != u'Packages/JavaScript/JavaScript.tmLanguage':
            return self.run_default()

        # Write to a temporary fie
        (i, filepath) = tempfile.mkstemp()
        f = open(filepath, 'w')
        script = view.substr(Region(0, view.size()))
        f.write(script)
        f.close()

        # Get the var locations via esprima (JS AST parser)
        child = subprocess.Popen(["node", "--eval", """
            var fs = require('fs'),
                varFind = require('var-find'),
                filepath = process.argv[1],
                script = fs.readFileSync(filepath, 'utf8'),
                varGroups = varFind(script);
            console.log(JSON.stringify(varGroups));
        """, filepath], stdout=subprocess.PIPE)
        var_group_json = child.stdout.read()

        # Kill the child
        child.kill()

        # Interpret the variable groups
        var_groups = json.loads(var_group_json)

        # TODO: If any var_groups are adjacent via whitespace, join them (handles multi-var-wide case)
        # TODO: The technicality being... how we delete things multiple `var`s

        # Collect all of the variable regions
        var_regions = RegionSet()
        for group in var_groups:
            # Generate and save a region to our RegionSet
            region = Region(group['start'], group['end'])
            var_regions.add(region)

            # Save the region to the group for later
            group['region'] = region

        # If none of the selections are not in a variable region, perform the default behavior
        selection = view.sel()
        in_var_region = map(lambda sel_region: var_regions.contains(sel_region), selection)
        if not any(in_var_region):
            self.run_default()
        # Otherwise, if all of the selections are in a variable region
        elif all(in_var_region):
            # Generate a collection for each selection region
            for group in var_groups:
                group['selections'] = []

            # Map each selection to its group
            for sel in selection:
                for group in var_groups:
                    if group['region'].contains(sel):
                        group['selections'].append(sel)

            # TODO: What about when we delete a comma

            # TODO: Sort the groups by region and iterate in reverse order to not fuck up indexes

            # For each group
            for group in var_groups:
                # Create a region for each var
                vars = group['vars']
                for var in vars:
                    var['region'] = Region(var['start'], var['end'])
                    var['matched'] = False

                # Iterate over the selections
                for sel in group['selections']:
                    # Mark any vars that match
                    matched_any = False
                    for var in vars:
                        if var['region'].intersects(sel):
                            var['matched'] = True
                            matched_any = True

                    # If no vars matched, find the "closest" one(s) and mark them
                    # va|r abc, def;
                    # var abc[,] def;
                    # var abc, def|;
                    if not matched_any:
                        # TODO: If they aren't ordered, order the vars by region start
                        for i, var in enumerate(vars):
                            # If we are before the first variable, mark the first variable
                            # va|r abc, def;
                            if i == 0 and sel.begin() < var['start']:
                                var['matched'] = True
                                prev_var = var
                                break

                            # If we are after the last variable,  mark the last variable
                            if i == (len(vars) - 1) and sel.end() > var['end']:
                                var['matched'] = True
                                prev_var = var
                                break

                            # If we are between two vars
                            # TODO: This won't work for when multiple parts of a var were selected
                            # var abc [, def], ghi;
                            # TODO: We could `subtract` a var from sel each time it is used. Need to fragment if it is a wide straddle
                            # var abc [, def, ] ghi, jkl;
                            # var jkl;
                            if prev_var['start'] < sel.start() and prev_var['end'] > sel.end():
                                # If our right is left of the comma, mark the previous var
                                # var abc | , def;

                                # If our left is right of the comma, mark the next var
                                # var abc , | def;

                                # Otherwise, mark the surrounding vars
                                # var abc [,] def;

                # If the all vars are being deleted, delete the group
                matches = map(lambda var: var['matched'], vars)
                if all(matches):
                    view.erase(edit, group['region'])
                else:
                # Otherwise...
                    # TODO: Sort the vars in and iterate in reverse order to not fuck up indexes -- this will affect prev_var
                    # Buffer out selections to contain surrounding whitespace
                    # var [ab|c,] def[, g|hi];
                    in_head = True
                    for var in vars:
                        # If the var has not been matched, mark leaving the head and continue
                        # var abc, ^def, ghi;
                        print 'www', var['matched']
                        if not var['matched']:
                            in_head = False
                            prev_var = var
                            continue

                        # If we are in the head group, buffer on the right
                        # var [^abc, ]def, ghi;
                        if in_head:
                            var_end = var['end']
                            pattern = re.compile('\s+')
                            buffered_end = pattern.search(script, var_end).end(0)
                            print var['start'], buffered_end
                            view.erase(edit, Region(var['start'], buffered_end))

                        # Otherwise, (we are in the tail), buffer on the left
                        # var abc, def[, ^ghi];
                        print 'x', in_head
                        if not in_head:
                            print 'aaa', prev_var
                            prev_var_start = prev_var['start']
                            pattern = re.compile('\s+')
                            buffered_start = pattern.search(script, prev_var_start).end(0) + 1
                            view.erase(edit, Region(buffered_start, var['end']))

                        prev_var = var



    def run_default(self):
        self.view.run_command("delete_word", {"forward": False})
