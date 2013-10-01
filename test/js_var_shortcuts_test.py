# Load in core dependencies
import glob
import os
import re

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
        # Load in input/output
        with open('%s.js' % base_path) as f:
            input_output = f.read()

        # Break up input and output
        (input, expected_output) = re.split(r'---+', input_output)

        # Break up target and expected selection
        input_obj = split_selection(input.strip())
        expected_obj = split_selection(expected_output.strip())

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
# TODO: Clump input/output into a single file
test_filenames = glob.glob(delete_dir + '/*.js')
test_namespaces = map(lambda filename: (filename.replace(delete_dir + '/', '')
                                                .replace('.js', '')), test_filenames)
skip_tests = [
    'multiline-all',  # Wide selection not yet supported (implement in plugin_tests)
    'multiline-multiple',  # Wide selection not yet supported (implement in plugin_tests)
    'same-line',  # TODO: Deal with nuance of cursor relocation during edit
    'multiline-middle',  # TODO: Deal with nuance of cursor relocation during edit
    'multiline-end-of-var',  # TODO: Deal with nuance of cursor relocation during edit
    'multiline-start',  # TODO: This is an arguable case... I will wait until the logic is done
]

# For each of the namespaces
for namespace in test_namespaces:
    # If the test is marked for skipping, skip it
    if namespace in skip_tests:
        continue

    # Otherwise, define the test
    TestVarDelete._add_io_test_case(namespace)
