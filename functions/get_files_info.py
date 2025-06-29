import os
import sys
from google.genai import types

def get_files_info(working_directory, directory=None):
    if directory is None or len(directory) == 0:
        return f'Error: Please specify the directory'
    if directory.startswith("../") or directory.startswith("/"):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    abs_path = os.path.abspath(working_directory)
    joined_paths = os.path.join(abs_path, directory)

    if not os.path.isdir(joined_paths):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if os.path.commonpath([abs_path,joined_paths]) != abs_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    dir_items = os.listdir(joined_paths)
    dir_info = []
    try:
        for item in dir_items:
            item_info = ""
            item_path = os.path.join(joined_paths, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            item_info = f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            dir_info.append(item_info)

        result = "\n".join(sorted(dir_info))

        return result
    except Exception as e:
        return f"Error: Unable to get files info: {e}"
    

schema_get_files_info = types.FunctionDeclaration(
name="get_files_info",
description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "directory": types.Schema(
            type=types.Type.STRING,
            description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
        ),
    },
),
)