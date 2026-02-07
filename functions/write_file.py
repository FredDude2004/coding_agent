import os

from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        print(target_file)
        if not is_valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(working_directory, 0o777, exist_ok=True)

        with open(target_file, "w") as f:
            chars_written = f.write(content)
            if chars_written:
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            f.close()
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Opens a file and overwrites its content, returns a string if successful",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to run",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to overwrite the file at file_path with",
            ),
        },
        required=["file_path", "content"],
    ),
)
