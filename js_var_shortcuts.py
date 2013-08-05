import re

import sublime
import sublime_plugin

class JsVarDeleteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # If the view is not JavaScript, perform the default
        view = self.view
        if view.settings().get('syntax') != u'Packages/JavaScript/JavaScript.tmLanguage':
            return self.run_default()

        # Grab the `var` and selected regions
        # DEV: `var` regions are defined by a `var` and a `;`
        var_regions = view.find_all(r'var[^;]+;')
        selected_regions = view.sel()

        # Determine which `var` block each selection is in
        # DEV: If this fails, use esprima to detect var blocks and return locations
        def find_var_region(selected_region):
            # By default, no region is found
            var_region = None

            # For each `var` region
            for region in var_regions:
                # If the region contains our selected region, save it and break
                if region.contains(selected_region):
                    var_region = region
                    break

            # Return the found region
            return var_region
        selected_var_regions = map(find_var_region, selected_regions)

        # If all selections are in a `var` block
        if all(selected_var_regions):
            # Map the selections for a variable
            # DEV: Variable is defined by a `var|,` and a `,|;`
            # TODO: This is the esprima part since the variable could have a `,` or `;` in its definition
            variable_regions = []
            for i, var_region in enumerate(selected_var_regions):
                # Grab the selection region and variable content
                # TODO: I am being naive here since edge cases deserve a testing framework
                selected_region = selected_regions[i]
                var_content = view.substr(var_region)

                # Find the region containing our selection
                var_region_start = var_region.begin()
                variable_region = None

                # Find all of the variable chunk in our `var` block
                for match in re.finditer(r'(var|,)[^,;]+;?', var_content):
                    # Generate a region for the variable
                    matched_region = sublime.Region(var_region_start + match.start(),
                                                    var_region_start + match.end())

                    # If the matched region *contains* the selected region (meaning full encapsulation)
                    # TODO: For multiple variables selected, we will prob be on esprima
                    # TODO: and it should be an intersection which collects onto an array of regions
                    if matched_region.contains(selected_region):
                        variable_region = matched_region
                        break

                # If there was a region, save it
                # DEV: This check is intended for the multiple selected variables case
                if variable_region:
                    variable_regions.append(variable_region)

            # Filter out repeated selections
            print variable_regions
            # Delete the selected variable from each block

        # Otherwise, if all selections are not in a `var` block
        elif not any(selected_var_regions):
            # Run the default command
            self.run_default()

    def run_default(self):
        self.view.run_command("run_macro_file", {
            "file": "Packages/Default/Delete to Hard BOL.sublime-macro"
        })
