import os

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