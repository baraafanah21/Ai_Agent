import os

from functions.paths import resolve_path

# Stop collecting after this many matching lines, to keep results bounded.
MAX_MATCHES = 100

schema_search_files = {
    "type": "function",
    "function": {
        "name": "search_files",
        "description": (
            "Searches text files under a directory, relative to the working directory, "
            "for lines containing an exact string. Returns each match as "
            "path:line_number: line. Use this to find where something is defined or "
            "used before reading or editing a file."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The exact text to look for (case-sensitive)",
                },
                "directory": {
                    "type": "string",
                    "description": "Directory to search in, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["query"],
        },
    },
}


def search_files(working_directory: str, query: str, directory: str = ".") -> str:
    try:
        target_dir, is_within = resolve_path(working_directory, directory)
        if not is_within:
            return f'Error: Cannot search "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        if not query:
            return "Error: query must not be empty"

        working_dir_abs = os.path.abspath(working_directory)
        matches = []
        for root, dirs, files in os.walk(target_dir):
            dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d != "__pycache__")
            for name in sorted(files):
                path = os.path.join(root, name)
                try:
                    with open(path, "r") as f:
                        for line_number, line in enumerate(f, start=1):
                            if query in line:
                                rel_path = os.path.relpath(path, working_dir_abs)
                                matches.append(f"{rel_path}:{line_number}: {line.rstrip()}")
                                if len(matches) >= MAX_MATCHES:
                                    matches.append(f"[...stopped after {MAX_MATCHES} matches]")
                                    return "\n".join(matches)
                except UnicodeDecodeError:
                    continue

        if not matches:
            return f'No matches for "{query}" in "{directory}"'
        return "\n".join(matches)
    except Exception as e:
        return f"Error: {e}"
