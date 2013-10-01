# sublime-js-var-shortcuts

Insert and delete shortcuts for JavaScript variables in [Sublime Text][]

This was built for (1) quickly setting up and tearing down variables, (2) proof of concept for [Sublime Text plugin testing framework][sublime-plugin-tests].

Currently, only tear down is supported.

[sublime-plugin-tests]: https://github.com/twolfson/sublime-plugin-tests/

## Getting Started
### Requirements
You must have [node][] installed on your machine. We use [esprima][] to locate the `var` statements.

[node]: http://nodejs.org/
[esprima]: http://esprima.org/

### Usage
By default, we bind variable deletion to `ctrl+backspace` on Windows/Linux, `command+backspace` on Mac. If no variables are selected, the default action (delete word on left) will be taken.

If you would like to add your own key binding, the deletion command is available as `js_var_delete`.

```json
{
  "keys": ["ctrl+delete"],
  "command": "js_var_delete"
}
```

## Donating
Support this project and [others by twolfson][gittip] via [gittip][].

[gittip]: https://www.gittip.com/twolfson/

## License
Copyright (c) 2013 Todd Wolfson

Licensed under the MIT license.