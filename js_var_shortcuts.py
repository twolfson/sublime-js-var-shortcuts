import sublime_plugin

class JsVarDeleteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # If the view is not JavaScript, perform the default
        view = self.view
        if view.settings().get('syntax') != u'Packages/JavaScript/JavaScript.tmLanguage':
            return self.run_default()

        # Determine which selections are in a `var` block
        """
        // We are only supporting the comma-last format to start
        // However, they all should be detectable via being between a `var` and a `;`
        var abc;
        var abc,
            def;
        """

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
