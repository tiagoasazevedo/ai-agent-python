from functions.run_python_file import run_python_file

def run_case(working_directory: str, file_path: str, args=None):
    if args is None:
        args = []
    
    args_str = f', {args}' if args else ''
    print(f'run_python_file("{working_directory}", "{file_path}"{args_str}):')
    
    result = run_python_file(working_directory, file_path, args)
    
    # Print each line of the result with indentation
    for line in result.splitlines():
        print(f"    {line}")
    print()

if __name__ == "__main__":
    run_case("calculator", "main.py")
    run_case("calculator", "main.py", ["3 + 5"])
    run_case("calculator", "tests.py")
    run_case("calculator", "../main.py")
    run_case("calculator", "nonexistent.py")
    run_case("calculator", "lorem.txt")
