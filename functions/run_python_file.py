import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    """
    Execute a Python file within the working directory.
    
    Args:
        working_directory: Base directory to restrict file access
        file_path: Path to the Python file to execute
        args: Optional list of command-line arguments to pass to the script
        
    Returns:
        String with execution output or error message
    """
    try:
        # Resolve absolute paths to prevent directory traversal attacks
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        # Validate file is within permitted directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Validate file exists
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        
        # Validate file is a Python file
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        # Execute the Python file
        completed_process = subprocess.run(
            ['python', abs_file_path] + args,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Build output string
        output_parts = []
        
        if completed_process.stdout:
            output_parts.append(f"STDOUT:\n{completed_process.stdout}")
        
        if completed_process.stderr:
            output_parts.append(f"STDERR:\n{completed_process.stderr}")
        
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")
        
        if not output_parts:
            return "No output produced."
        
        return "\n".join(output_parts)
    
    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"
