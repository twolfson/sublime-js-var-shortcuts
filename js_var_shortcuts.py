# Load in core dependencies
import json
import os
import subprocess
import sublime
import sublime_plugin
import tempfile


# Localize Region
Region = sublime.Region


# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))


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


# Define a helper for adding linked list refs
def linked_listify(items):
    # Bind head to tail
    prev_item = None
    for item in items:
        item['prev'] = prev_item
        prev_item = item

    # Get tail item and bind in reverse
    last_item = item
    while last_item:
        item = last_item['prev']
        if item:
            item['next'] = last_item
            last_item = item
        else:
            last_item = None


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
        """, filepath], cwd=__dir__, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        var_group_json = child.stdout.read()
        var_group_stderr = child.stderr.read()

        # Kill the child
        child.kill()

        # If there is stderr, throw it
        if var_group_stderr:
            raise Exception(var_group_stderr)

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
            # *****
            # TODO: New strategy, break selection down into indices.
            # TODO: Iterate over indices, marking vars as used.
            # TODO: Use buffer logic for indices not directly on vars.
            # TODO: Optimization: When a var is marked, skip all remaining indicies contained.
            # TODO: Optimization: Each loop, check that all vars are marked. If they are, exit it.
            # *****

            # Generate a collection for each selection region
            for group in var_groups:
                group['selections'] = []

            # Map each selection to its group
            for sel in selection:
                for group in var_groups:
                    if group['region'].contains(sel):
                        group['selections'].append(sel)

            # Create placeholder for deletion actions
            delete_groups = []

            # Sort the groups into ascending order
            var_groups.sort(lambda a, b: a['start'] - b['start'])

            # Add ['prev'] and ['next'] properties for each group
            linked_listify(var_groups)

            # Iterate over the groups
            for group in var_groups:
                # Sort and link the variables
                vars = group['vars']
                vars.sort(lambda a, b: a['start'] - b['start'])
                linked_listify(vars)

                # Grab the first and last var
                first_var = vars[0]
                last_var = vars[len(vars) - 1]

                # Break down the selection into an ordered list of indicies
                selected_indicies = []
                for sel in group['selections']:
                    selected_indicies += range(sel.begin(), sel.end() + 1)
                selected_indicies.sort()

                # Iterate over the indicies
                for index in selected_indicies:
                    # TODO: Optimization: Binary search for lowest starting index (including 0)
                    # If we are before the first var, select the first var
                    if index < first_var['start']:
                        first_var['matched'] = True
                        continue

                    # If we are after the last var, select it
                    if index > last_var['end']:
                        last_var['matched'] = True
                        continue

                    # Walk the vars
                    for var in vars:
                        # If we are in the var
                        if index >= var['start'] and index <= var['end']:
                            var['matched'] = True

                        # Otherwise, if we are between this var and the next one
                        # DEV: var['next'] will be defined because we checked being after last_var['end']
                        elif index > var['end'] and index < var['next']['start']:
                            # If we are before the separating comma
                            next_nonwhitespace =


    def run_default(self):
        self.view.run_command("delete_word", {"forward": False})
