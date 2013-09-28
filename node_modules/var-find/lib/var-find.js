// Load in dependencies
var falafel = require('falafel');

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
function varFind(script) {
  // Create placeholder for groups
  var groups = [];

  // Walk the AST
  falafel(script, function varFindFn (node) {
    // If the node is a variable declaration
    if (node.type === 'VariableDeclaration') {
      // Look at its declaractions
      var declarations = node.declarations || [];

      // Iterate over the declarations
      var vars = declarations.map(function walkDeclarations (declaration) {
        // Save start and end
        return {
          start: declaration.range[0],
          end: declaration.range[1]
        };
      });

      // Save the declarations
      groups.push({
        vars: vars,
        start: node.range[0],
        end: node.range[1]
      });
    }
  });

  // Return the groups
  return groups;
}
module.exports = varFind;