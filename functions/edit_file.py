import os

from functions.paths import resolve_path

schema_edit_file = {
    "type": "function",
    "function": {
        "name": "edit_file",
        "description": (
            "Replaces an exact string in a file with new text, relative to the working "
            "directory. Prefer this over write_file when changing part of an existing "
            "file: it leaves the rest of the file untouched. The old_string must appear "
            "exactly once in the file, so include enough surrounding context to make it "
            "unique."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to edit, relative to the working directory",
                },
                "old_string": {
                    "type": "string",
                    "description": "The exact text to replace. Must match the file byte for byte, including indentation, and must occur exactly once.",
                },
                "new_string": {
                    "type": "string",
                    "description": "The text to put in its place. Use an empty string to delete the old text.",
                },
            },
            "required": ["file_path", "old_string", "new_string"],
        },
    },
}


def edit_file(
    working_directory: str, file_path: str, old_string: str, new_string: str
) -> str:
    try:
        target_file, is_within = resolve_path(working_directory, file_path)
        if not is_within:
            return f'Error: Cannot edit "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        if old_string == new_string:
            return "Error: old_string and new_string are identical, nothing to change"

        with open(target_file, "r") as f:
            content = f.read()

        occurrences = content.count(old_string)
        if occurrences == 0:
            return f'Error: old_string was not found in "{file_path}"'
        if occurrences > 1:
            return (
                f'Error: old_string appears {occurrences} times in "{file_path}"; '
                "include more surrounding context so it matches exactly once"
            )

        with open(target_file, "w") as f:
            f.write(content.replace(old_string, new_string))

        return (
            f'Successfully edited "{file_path}" '
            f"({len(old_string)} characters replaced with {len(new_string)})"
        )
    except UnicodeDecodeError:
        return f'Error: "{file_path}" is not a readable text file (it looks binary)'
    except Exception as e:
        return f"Error: {e}"
