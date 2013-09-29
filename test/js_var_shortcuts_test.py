# Load in core dependencies
import os
import unittest

# Load in local dependencies
from sublime_plugin_tests import framework
from sublime_plugin_tests.utils.selection import split_selection

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))


# Define our class
class TestVarDelete(framework.TestCase):
    @framework.template(__dir__ + '/delete_files/plugin.template.py')
    def parse_io_files(self, base_path):
        # Load in input
        with open('%s.input.js' % base_path) as f:
            input = f.read()

        # Break up target selection from content
        input_obj = split_selection(input)

        # Load in single.output
        with open('%s.output.js' % base_path) as f:
            expected_output = f.read()

        # Break up expected selection from content
        expected_obj = split_selection(expected_output)

        # Return collected information
        return {
            'target_sel': input_obj['selection'],
            'content': input_obj['content'],
            'expected_sel': expected_obj['selection'],
            'expected_content': expected_obj['content'],
        }

    def test_var_delete_default(self):
        return self.parse_io_files(__dir__ + '/delete_files/default')

    @unittest.skip('Currently not supported')
    def test_var_delete_comma_in_var(self):
        return self.parse_io_files(__dir__ + '/delete_files/comma-in-var')

    @unittest.skip('Currently not supported')
    def test_var_delete_comma_in_var(self):
        return self.parse_io_files(__dir__ + '/delete_files/comma-in-var')
