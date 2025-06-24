import unittest
from get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_directory_dot(self):
        result = get_files_info("calculator", ".")
        self.assertEqual(
            result,
            "\n".join([
            "- main.py: file_size=575 bytes, is_dir=False",
            "- pkg: file_size=4096 bytes, is_dir=True",
            "- tests.py: file_size=1342 bytes, is_dir=False"
            ])
        )

if __name__ == '__main__':
    unittest.main()