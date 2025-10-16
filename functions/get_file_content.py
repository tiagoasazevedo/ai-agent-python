from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    import os
    
    # Check if the file_path is outside the working_directory
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(file_path)
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if the file_path is not a file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # Read and return the file content
    with open(abs_file_path, 'r') as file:
        return file.read()