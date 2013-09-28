# var-find

Find and return indexes of variable declarations.

This was built to run inside of [twolfson/sublime-js-var-shortcuts][], a [Sublime Text][] plugin to make dealing with adding/removing `vars` easier.

[twolfson/sublime-js-var-shortcuts]: https://github.com/twolfson/sublime-js-var-shortcuts
[Sublime Text]: http://sublimetext.com/

## Getting Started
Install the module with: `npm install var-find`

```javascript
var varFind = require('var-find');
varFind(function abc() {
  // Group: `var def = 123;`
  // Declaration: `def = 123;`
  var def = 123;

  console.log('hi');
} + '');
// [{
//   "start": 78,
//   "end": 92,
//   "vars": [{
//     "start": 82,
//     "end": 91
//   }]
// }]
```

## Documentation
`varFind` is a function that takes in a JS source code.

```js
varFind(script);
/**
 * varFind parses JS source code and returns locations of variable groups and declarations
 * @param {String} script Source code to parse
 * @returns {Array} groups Collection of variable groups
 * @returns {Object} groups[i] Variable group instance
 * @returns {Number} groups[i].start Beginning index for variable group instance
 * @returns {Number} groups[i].end Finishing index for variable group instance
 * @returns {Array} groups[i].vars Collection of variable declarations
 * @returns {Object} groups[i].vars[i] Variable declaration instance
 * @returns {Number} groups[i].vars[i].start Beginning index for variable declaration instance
 * @returns {Number} groups[i].vars[i].end Finishing index for variable declaration instance
 */
```

## Examples
For visual representation, variable groups begin and end with `[` and `]`; for variable declarations, `{` and `}`.

**Single definition:**

```js
[var {abc = 123};]

console.log('hi');
```

**Comma-last definition:**

```js
[var {abc},
     {def};]

console.log('hi');
```

**Comma-first definition:**

```js
[var {abc}
   , {def};]

console.log('hi');
```

**Trailing whitespace (with semicolon):**

> Trailing whitespace without semicolon is considered another statement and ignored.

```js
[var {abc = 123}   ;]

console.log('hi');
```

## Donating
Support this project and [others by twolfson][gittip] via [gittip][].

[![Support via Gittip][gittip-badge]][gittip]

[gittip-badge]: https://rawgithub.com/twolfson/gittip-badge/master/dist/gittip.png
[gittip]: https://www.gittip.com/twolfson/

## Contributing
In lieu of a formal styleguide, take care to maintain the existing coding style. Add unit tests for any new or changed functionality. Lint via [grunt](https://github.com/gruntjs/grunt) and test via `npm test`.

## Unlicense
As of Sep 27 2013, Todd Wolfson has released this repository and its contents to the public domain.

It has been released under the [UNLICENSE][].

[UNLICENSE]: UNLICENSE
