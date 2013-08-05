import sublime
import sublime_plugin

class JsVarDeleteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # If the view is not JavaScript, perform the default
        view = self.view
        if view.settings().get('syntax') != u'Packages/JavaScript/JavaScript.tmLanguage':
            return self.run_default()

        # Determine which selections are in a `var` block
        # DEV: This is determined by being between a `var` and a `;`
        # DEV: If this fails, use esprima to detect var blocks and return locations
        content_region = sublime.Region(0, view.size())
        content = view.substr(content_region)
        print content

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
