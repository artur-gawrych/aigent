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
    
    def test_directory_pkg(self):
        result = get_files_info("calculator", "pkg")
        self.assertEqual(
            result,
            "\n".join([
            "- __pycache__: file_size=4096 bytes, is_dir=True",
            "- calculator.py: file_size=1737 bytes, is_dir=False",
            "- render.py: file_size=766 bytes, is_dir=False"
        ])
        )
    
    def test_directory_slash(self):
        result = get_files_info("calculator", "/bin")
        self.assertEqual(
            result,
            f'Error: Cannot list "/bin" as it is outside the permitted working directory'
        )
    def test_directory_traversal(self):
        result = get_files_info("calculator", "../")
        self.assertEqual(
            result,
            f'Error: Cannot list "../" as it is outside the permitted working directory'
        )

    def test_directory_invalid(self):
        result = get_files_info("calculator", "calculator")
        self.assertEqual(
            result,
            f'Error: Cannot list "calculator" as it is outside the permitted working directory'
        )


if __name__ == '__main__':
    unittest.main()