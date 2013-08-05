import sublime_plugin

class JsVarDeleteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # If the view is not JavaScript, perform the default
        if self.view.settings().get('syntax') != u'Packages/JavaScript/JavaScript.tmLanguage':
            return self.run_default()

        print 'hi'

    def run_default(self):
        self.view.run_command("run_macro_file", {
            "file": "Packages/Default/Delete to Hard BOL.sublime-macro"
        })
