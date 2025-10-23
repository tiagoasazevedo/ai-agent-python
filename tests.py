from functions.write_file import write_file

def run_case(working_directory: str, file_path: str, content: str):
    print(f'write_file("{working_directory}", "{file_path}", "{content}"):')
    
    result = write_file(working_directory, file_path, content)
    print(f"    {result}")
    print()

if __name__ == "__main__":
    run_case("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    run_case("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    run_case("calculator", "/tmp/temp.txt", "this should not be allowed")
