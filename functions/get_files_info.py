import os

from functions.paths import resolve_path

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status. Use this ONLY when the user asks what files or directories exist. Do NOT use this to read a file's contents or to run a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        target_dir, is_within = resolve_path(working_directory, directory)
        if not is_within:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        lines = []
        for name in sorted(os.listdir(target_dir)):
            path = os.path.join(target_dir, name)
            lines.append(
                f"- {name}: file_size={os.path.getsize(path)} bytes, "
                f"is_dir={os.path.isdir(path)}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
