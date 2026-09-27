import os

from config import MAX_CHARS
from functions.paths import resolve_path

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Reads and returns the first {MAX_CHARS} characters of the content of a specified file, relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file whose content should be read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target_file, is_within = resolve_path(working_directory, file_path)
        if not is_within:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except UnicodeDecodeError:
        return f'Error: "{file_path}" is not a readable text file (it looks binary)'
    except Exception as e:
        return f"Error: {e}"
