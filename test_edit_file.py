from functions.edit_file import edit_file
from functions.write_file import write_file


def main() -> None:
    write_file("calculator", "edit_target.txt", "alpha\nbeta\ngamma\nbeta\n")

    print("Unique match:")
    print(edit_file("calculator", "edit_target.txt", "alpha", "ALPHA"))
    print()

    print("Ambiguous match (appears twice):")
    print(edit_file("calculator", "edit_target.txt", "beta", "BETA"))
    print()

    print("Missing match:")
    print(edit_file("calculator", "edit_target.txt", "delta", "DELTA"))
    print()

    print("Identical strings:")
    print(edit_file("calculator", "edit_target.txt", "gamma", "gamma"))
    print()

    print("Outside the working directory:")
    print(edit_file("calculator", "../main.py", "import os", "import sys"))
    print()

    print("Nonexistent file:")
    print(edit_file("calculator", "nope.txt", "a", "b"))
    print()

    print("File contents after the edits:")
    with open("calculator/edit_target.txt") as f:
        print(f.read())


if __name__ == "__main__":
    main()
