# Load in core dependencies
import os
import glob

# Load in local dependencies
from sublime_plugin_tests import framework
from sublime_plugin_tests.utils.selection import split_selection

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))
delete_dir = __dir__ + '/delete_files'

# Define our class
class TestVarDelete(framework.TestCase):
    @framework.template(delete_dir + '/plugin.template.py')
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

    @classmethod
    def _add_io_test_case(cls, namespace):
        def test_var_delete_fn(self):
            return self.parse_io_files(delete_dir + '/' + namespace)
        setattr(cls, 'test_var_delete_' + namespace, test_var_delete_fn)

# Grab files to load in as tests
test_filenames = glob.glob(delete_dir + '/*.input.js')
test_namespaces = map(lambda filename: (filename.replace(delete_dir + '/', '')
                                                .replace('.input.js', '')), test_filenames)
skip_tests = [
    'comma-in-var',  # Edge case not yet supported (move to esprima)
    'multiline-all',  # Wide selection not yet supported (implement in plugin_tests)
    'multiline-multiple',  # Wide selection not yet supported (implement in plugin_tests)
    'same-line',  # TODO: Deal with nuance of cursor relocation during edit
    'multiline-middle',  # TODO: Deal with nuance of cursor relocation during edit
    'multiline-end-of-var',  # TODO: Deal with nuance of cursor relocation during edit
    'multi-var',  # TODO: Interesting edge case for sets...
    'multiline-start',  # TODO: This is an arguable case... I will wait until the logic is done
]

# For each of the namespaces
for namespace in test_namespaces:
    # If the test is marked for skipping, skip it
    if namespace in skip_tests:
        continue

    # Otherwise, define the test
    TestVarDelete._add_io_test_case(namespace)
