import os
from google.genai import types

def get_file_content(working_directory, file_path):
    if file_path is None or len(file_path) == 0:
        return f'Error: Please specify the directory'    

    abs_work_path = os.path.abspath(working_directory)
    abs_file_path = os.path.join(abs_work_path, file_path)

    if os.path.commonpath([abs_work_path, abs_file_path]) != abs_work_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        MAX_CHARS = 10000
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        
        if len(file_content_string) >= MAX_CHARS:
            return file_content_string + f'...File "{file_path}" truncated at 10000 characters'

        return file_content_string
    
    except Exception as e:
        return f'Error: Unable to read the file {file_path}: {e}'
    
schema_get_file_content = types.FunctionDeclaration(
name="get_file_content",
description="Reads content of a file, constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="Path to the file to read the contents of, relative to the working directory."
        )
    }
)
)