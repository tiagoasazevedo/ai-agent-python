from functions.get_file_content import get_file_content

def run_case(working_directory: str, file_path: str):
    print(f'get_file_content("{working_directory}", "{file_path}"):')
    
    result = get_file_content(working_directory, file_path)
    
    if isinstance(result, str) and result.startswith("Error:"):
        print(f"    {result}")
    else:
        # Print the full content
        for line in result.splitlines():
            print(f"    {line}")
    print()

if __name__ == "__main__":
    run_case("calculator", "main.py")
    run_case("calculator", "pkg/calculator.py")
    run_case("calculator", "/bin/cat")
    run_case("calculator", "pkg/does_not_exist.py")
