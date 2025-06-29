import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):

    real_work_path = os.path.realpath(working_directory)
    joined_paths = os.path.join(real_work_path, file_path)
    real_file_path = os.path.realpath(joined_paths)

    if os.path.commonpath([real_work_path, real_file_path]) != real_work_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(real_file_path):
        return f'Error: File "{file_path}" not found.'
    if not real_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        process = subprocess.run(
            ['python3', real_file_path], 
            capture_output=True, 
            text=True,
            timeout=30,
        )

        if not process.stdout.strip() and not process.stderr.strip():
            return f"No output produced"

        output = []

        if process.stdout.strip():
            output.append(f"STDOUT: {process.stdout}")
        if process.stderr.strip():
            output.append(f"STDERR: {process.stderr}")
        if process.returncode != 0:
            output.append(f"Process exited with code {process.returncode}")

        return "\n".join(output)

    
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
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