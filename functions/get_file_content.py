from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    """
    Read file content from a given path within the working directory.
    
    Args:
        working_directory: Base directory to restrict file access
        file_path: Path to the file to read
        
    Returns:
        File content as string, or error message if invalid
    """
    import os
    
    try:
        # Resolve absolute paths to prevent directory traversal attacks
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        # Validate file is within permitted directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Validate file exists and is a regular file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read file content with size limit
        with open(abs_file_path, "r") as f:
            # Read slightly more than limit to detect truncation
            data = f.read(MAX_CHARS + 1)
        
        # Return full content if within limit
        if len(data) <= MAX_CHARS:
            return data
        
        # Truncate and append notice if content exceeds limit
        truncation_notice = f'\n[...File truncated at {MAX_CHARS} characters]'
        return data[:MAX_CHARS] + truncation_notice
    except Exception as e:
        return f"Error: {str(e)}"

from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)