from functions.write_file import write_file


def main() -> None:
    print("Result for 'lorem.txt':")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print()

    print("Result for 'pkg/morelorem.txt':")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print()

    print("Result for '/tmp/temp.txt':")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


if __name__ == "__main__":
    main()
