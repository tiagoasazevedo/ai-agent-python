import os

def write_file(working_directory, file_path, content):
    """
    Write content to a file within the working directory.
    
    Args:
        working_directory: Base directory to restrict file access
        file_path: Path to the file to write
        content: Content to write to the file
        
    Returns:
        Success message or error message string
    """
    try:
        # Resolve absolute paths to prevent directory traversal attacks
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        # Validate file is within permitted directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Create directory if it doesn't exist
        file_dir = os.path.dirname(abs_file_path)
        if file_dir:
            os.makedirs(file_dir, exist_ok=True)
        
        # Write content to file
        with open(abs_file_path, 'w') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {str(e)}'
    