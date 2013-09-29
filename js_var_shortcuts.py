# Load in core dependencies
import json
import subprocess
import sublime
import sublime_plugin
import tempfile


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
        content = view.substr(sublime.Region(0, view.size()))
        f.write(content)
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
            region = sublime.Region(group['start'], group['end'])
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
                # Iterate over the vars
                vars = group['vars']
                for var in vars:
                    var_region = sublime.Region(var['start'], var['end'])
                    # Find if it matches any selections
                    for sel in group['selections']:
                        var['matched'] = var_region.intersects(sel)

                # If the all vars are being deleted, delete the group
                matches = map(lambda var: var['matched'], vars)
                if all(matches):
                    view.erase(edit, group['region'])
                else:
                # Otherwise...
                    # TODO: Sort the vars in and iterate in reverse order to not fuck up indexes
                    # Buffer out selections to contain surrounding whitespace
                    # var [ab|c,] def[, g|hi];
                    in_head = True
                    for var in vars:
                        # If the var has not been matched, mark leaving the head and continue
                        # var abc, ^def, ghi;
                        if not var['matched']:
                            in_head = False
                            continue

                        # If we are in the head group, buffer on the right
                        # var [^abc,] def, ghi;
                        if in_head:
                            var_end = var['end']
                            print var_end

                        # Otherwise, (we are in the tail), buffer on the left
                        # var abc, def[, ^ghi];



    def run_default(self):
        self.view.run_command("delete_word", {"forward": False})
