import os


def create_file_if_not_exist(path):
    """
    Create a file at the specified path if it doesn't already exist.

    Args:
        path (str): The path of the file to be created.

    Returns:
        None
    """
    # TODO path type check
    if os.path.exists(path):
        pass
    else:
        with open(path, "w", encoding="utf-8"):
            pass


def create_dir_if_not_exist(path):
    """
    Create a directory if it doesn't already exist.

    Args:
        path (str): The path of the directory to be created.

    Returns:
        None
    """
    # TODO path type check
    if not os.path.exists(path):
        # if playlist directory doesn't exist, create it
        os.mkdir(path)
