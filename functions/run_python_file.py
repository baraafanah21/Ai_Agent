import os
import subprocess
import sys

from config import TIMEOUT_SECONDS
from functions.paths import resolve_path

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file with the interpreter, relative to the working directory, and returns its output. Accepts optional command-line arguments and times out after 30 seconds",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional command-line arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        target_file, is_within = resolve_path(working_directory, file_path)
        if not is_within:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = [sys.executable, target_file]
        if args:
            command.extend(args)

        completed = subprocess.run(
            command,
            cwd=os.path.abspath(working_directory),
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )

        parts = []
        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")
        if not completed.stdout and not completed.stderr:
            parts.append("No output produced")
        else:
            if completed.stdout:
                parts.append(f"STDOUT:\n{completed.stdout}")
            if completed.stderr:
                parts.append(f"STDERR:\n{completed.stderr}")

        return "\n".join(parts)
    except subprocess.TimeoutExpired:
        return f'Error: "{file_path}" timed out after {TIMEOUT_SECONDS} seconds'
    except Exception as e:
        return f"Error: executing Python file: {e}"
