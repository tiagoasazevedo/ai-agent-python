from functions.get_files_info import get_files_info

def run_case(working_directory: str, directory: str):
    print(f'get_files_info("{working_directory}", "{directory}"):')

    if directory == ".":
        print("Result for current directory:")
    else:
        print(f"Result for '{directory}' directory:")

    result = get_files_info(working_directory, directory)

    if isinstance(result, str) and result.startswith("Error:"):
        print(f"    {result}")
    else:
        for line in result.splitlines():
            print(f" {line}")
    print()

if __name__ == "__main__":
    run_case("calculator", ".")
    run_case("calculator", "pkg")
    run_case("calculator", "/bin")
    run_case("calculator", "../")
