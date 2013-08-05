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

        print selected_var_regions

        # If all selections are in a `var` block
            # Map the selections for a varible
            # Filter out repeated selections
            # Delete the selected variable from each block

        # Otherwise, if all selections are not in a `var` block
            # Run the default command

    def run_default(self):
        self.view.run_command("run_macro_file", {
            "file": "Packages/Default/Delete to Hard BOL.sublime-macro"
        })
