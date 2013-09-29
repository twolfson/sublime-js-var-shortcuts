# Load in core dependencies
import os

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

    # Automatically load in tests from flat files
    test_filenames = os.listdir(__dir__ + '/delete_files')
    skip_tests = [
        'comma-in-var',  # Edge case not yet supported (move to esprima)
        'multi-var-all',  # Wide selection not yet supported (implement in plugin_tests)
        'multi-var-multiple',  # Wide selection not yet supported (implement in plugin_tests)
    ]

    for filename in test_filenames:
        # If the test is marked for skipping, skip it
        if filename in skip_tests:
            continue

        # Otherwise, define the test
        def test_abc(self):
            return ''
