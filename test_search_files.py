from functions.search_files import search_files


def main() -> None:
    print("Search for 'def ' in the whole working directory:")
    print(search_files("calculator", "def "))
    print()

    print("Search inside 'pkg' only:")
    print(search_files("calculator", "class Calculator", "pkg"))
    print()

    print("No matches:")
    print(search_files("calculator", "this string does not exist anywhere"))
    print()

    print("Empty query:")
    print(search_files("calculator", ""))
    print()

    print("Outside the working directory:")
    print(search_files("calculator", "import", "../"))
    print()

    print("Not a directory:")
    print(search_files("calculator", "import", "main.py"))


if __name__ == "__main__":
    main()
