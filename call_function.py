import inspect
import json
from collections.abc import Callable

from config import MAX_TOOL_RESULT_CHARS, WORKING_DIR
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def _tool_message(tool_call_id: str, content: str) -> dict:
    if len(content) > MAX_TOOL_RESULT_CHARS:
        content = (
            content[:MAX_TOOL_RESULT_CHARS]
            + f"\n[...result truncated at {MAX_TOOL_RESULT_CHARS} characters]"
        )
    return {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": content,
    }


def _drop_unexpected_args(function: Callable[..., str], function_args: dict) -> dict:
    """Keep only kwargs the function actually accepts.

    Weaker models sometimes emit malformed argument names (e.g. "file_path=file_path"),
    which would raise TypeError on the call. Dropping them lets the function return
    its own error string instead, which the agent can read and recover from.
    """
    accepted = inspect.signature(function).parameters
    return {k: v for k, v in function_args.items() if k in accepted}


def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name

    try:
        function_args = json.loads(tool_call.function.arguments or "{}")
    except json.JSONDecodeError as e:
        return _tool_message(
            tool_call.id, f"Error: Could not parse arguments for {function_name}: {e}"
        )

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return _tool_message(tool_call.id, f"Error: Unknown function: {function_name}")

    function = function_map[function_name]
    function_args = _drop_unexpected_args(function, function_args)
    function_args["working_directory"] = WORKING_DIR

    try:
        result = function(**function_args)
    except Exception as e:
        result = f"Error: {function_name} failed: {e}"

    return _tool_message(tool_call.id, result)
