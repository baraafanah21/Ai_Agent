import os


def resolve_path(working_directory: str, relative_path: str) -> tuple[str, bool]:
    """Resolve relative_path inside working_directory.

    Returns the absolute target path and whether it stays within the working
    directory. Callers own the error message, since each tool phrases it
    differently ("Cannot list", "Cannot read", ...).
    """
    working_dir_abs = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_dir_abs, relative_path))
    is_within = os.path.commonpath([working_dir_abs, target]) == working_dir_abs
    return target, is_within
