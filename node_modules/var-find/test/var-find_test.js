// Load in dependencies and library
var fs = require('fs'),
    assert = require('assert'),
    varFind = require('../lib/var-find.js');

// Load in test files
var testDir = __dirname + '/test_files',
    testFiles = fs.readdirSync(testDir);

// Define our test suite
describe('var-find', function () {
  // Iterate over the test files (cases)
  testFiles.forEach(function (filename) {
    // DEV: Test only one file
    // if (filename !== 'single.js') { return; }

    describe('parsing ' + filename, function () {
      // Parse out content from selection in our file
      before(function () {
        // TODO: We could have done right to left finding to not deal with splice errors (e.g. >= groupEnd)
        // TODO: I wonder how we can abstract this...
        // Load in the file contents
        // [{var abc;}]
        var testFile = fs.readFileSync(testDir + '/' + filename, 'utf8'),
            testChars = testFile.split('');

        // Extract the var groups
        var groups = [];
        while (true) {
          // Find the next group start
          // `[` + {var abc;}]
          var groupStart = testChars.indexOf('[');

          // If there was no match, stop
          if (groupStart === -1) {
            break;
          }

          // Remove the starting piece
          // {var abc;}]
          testChars.splice(groupStart, 1);

          // Find the group end
          // {var abc;} + `]`
          var groupEnd = testChars.indexOf(']');
          assert.notEqual(groupEnd, -1, 'Group starting at "' + groupStart + '" did not have an end.');

          // Remove the group end
          testChars.splice(groupEnd, 1);

          // Extract each var piece
          var vars = [];
          while (true) {
            // Find the next var start
            // `{` + var abc;}]
            var varStart = testChars.indexOf('{');

            // If there was no match or we have gone beyond the group end, stop
            if (varStart === -1 || varStart >= groupEnd) {
              break;
            }

            // Remove the starting piece
            // var abc;}]
            testChars.splice(varStart, 1);
            groupEnd -= 1;

            // Find the var end
            // var abc; + `}` + ]
            var varEnd = testChars.indexOf('}');
            assert.notEqual(varEnd, -1, '`var` starting at "' + varStart + '" did not have an end.');

            // If we have gone beyond the group end, stop
            if (varEnd >= groupEnd) {
              break;
            }

            // Remove the var end
            testChars.splice(varEnd, 1);
            groupEnd -= 1;

            // Collect the var start and end
            vars.push({
              start: varStart,
              end: varEnd
            });
          }

          // Save the vars for later
          groups.push({
            vars: vars,
            start: groupStart,
            end: groupEnd
          });
        }

        // Collect chars
        var content = testChars.join('');

        // If there are any special chars remaining, complain
        var specialMatch = content.match(/\[|{|}|\]/);
        assert.strictEqual(specialMatch, null);

        // Save content and groups for later
        this.content = content;
        this.expectedGroups = groups;
      });

      // Run the content through varFind
      before(function () {
        this.actualGroups = varFind(this.content);
      });

      // Run our assertion
      it('contains expected groups of variables', function () {
        assert.deepEqual(this.actualGroups, this.expectedGroups);
      });
    });
  });
});
