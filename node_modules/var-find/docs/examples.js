var varFind = require('../lib/var-find');
var fn = function abc() {
  // Group: `var def = 123;`
  // Declaration: `def = 123`
  var def = 123;

  console.log('hi');
} + '';
console.log(fn);
console.log(
  JSON.stringify(
    varFind(fn), null, 2
  )
);