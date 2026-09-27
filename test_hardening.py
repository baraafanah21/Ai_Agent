"""Checks for the failure modes that used to crash the dispatcher."""

from types import SimpleNamespace

from call_function import call_function
from functions.get_file_content import get_file_content


def fake_tool_call(name: str, arguments: str, call_id: str = "call_1"):
    return SimpleNamespace(
        id=call_id, function=SimpleNamespace(name=name, arguments=arguments)
    )


def main() -> None:
    print("Malformed argument key (used to raise TypeError):")
    print(call_function(fake_tool_call("run_python_file", '{"file_path=file_path": "main.py"}')))
    print()

    print("Unparseable arguments JSON:")
    print(call_function(fake_tool_call("get_files_info", "{not json")))
    print()

    print("Unknown function name:")
    print(call_function(fake_tool_call("delete_everything", "{}")))
    print()

    print("Binary file read:")
    print(get_file_content("calculator", "pkg/__pycache__/calculator.cpython-312.pyc"))


if __name__ == "__main__":
    main()
