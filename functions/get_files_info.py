import os
from typing import List

def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
    Lists entries in `directory` (relative to `working_directory`) with size and is_dir flag.
    Always returns a string. On any failure returns an error string prefixed with 'Error:'.

    Format per line:
    - NAME: file_size=NNN bytes, is_dir=True|False
    """
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(wd_abs, directory))

        # boundary check
        if os.path.commonpath([wd_abs, target_abs]) != wd_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # must be a directory
        if not os.path.isdir(target_abs):
            return f'Error: "{directory}" is not a directory'

        lines: List[str] = []
        with os.scandir(target_abs) as it:
            for entry in it:
                # follow_symlinks=False to avoid escaping the tree
                is_dir = entry.is_dir(follow_symlinks=False)
                try:
                    size = entry.stat(follow_symlinks=False).st_size
                except Exception as e:
                    return f"Error: failed to stat {entry.name}: {e}"

                lines.append(f"- {entry.name}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {e}"

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
