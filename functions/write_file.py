import os
from google.genai import types

def write_file(working_path, file_path, content):

    abs_work_path = os.path.abspath(working_path)
    abs_file_path = os.path.join(abs_work_path, file_path)

    if os.path.commonpath([abs_work_path, abs_file_path]) != abs_work_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        if not os.path.exists(os.path.dirname(abs_file_path)):
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
           
        with open(abs_file_path, "w") as f:
            f.write(content)    

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Unable to write to a file: {e}'
    

schema_write_file = types.FunctionDeclaration(
name="write_file",
description="Write contents to a file. If file deoes not exist it will create one. Constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type= types.Type.STRING,
            description="Path to a file, relative to working directory."
        ),
        "content": types.Schema(
            type=types.Type.STRING,
            description="Content to be written to a file."
        )
    }

)
)

schema_run_python_file = types.FunctionDeclaration(
name="run_python_file",
description="Runs python script, constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="Path to a python sctipt, relative to working directory"
        )
    }
)
)