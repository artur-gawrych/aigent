import unittest
from get_files_info import get_files_info

class get_files_info_tests(unittest.TestCase):
    def test_directory_dot(self):
        result = get_files_info("calculator", ".")
        self.assertEqual(
            print(result),
            "- main.py: file_size=575, is_dir=False" \
            "- pkg: file_size=4096, is_dir=True" \
            "- tests.py: file_size=1342, is_dir=False"
        )

if __name__ == '__main__':
    unittest.main()