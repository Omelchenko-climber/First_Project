import os
import shutil
import re
from src.View.base_view import ConsoleView


# Dictionary mapping file types to their corresponding extensions
DIRECTORIES = {
    "Images": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", ".svg", ".heif", ".psd"],
    "Videos": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng", ".qt", ".mpg", ".mpeg", ".3gp"],
    "Documents": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  ".pptx", ".csv"],
    "Audio": [".aac", ".aa", ".aacp", ".dsd", ".dvf", ".m4a", ".m4b", ".m4p",
              ".mp3", ".msv", ".ogg", ".oga", ".raw", ".vox", ".wav", ".wma"],
    "Text": [".txt", ".in", ".out"],
    "Programming": [".py", ".ipynb", ".c", ".cpp", ".class", ".h", ".java",
                    ".sh", ".html", ".css", ".js", ".go", ".json"]
}


def normalize(name):
    """
    Normalize file name to replace special characters and spaces with underscores.

    Args:
        name (str): File name to be normalized.

    Returns:
        str: Normalized file name.
    """
    translit = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
                'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
                'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shc', 'ъ': '',
                'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
    name = name.lower()
    for cyr, lat in translit.items():
        name = name.replace(cyr, lat)
    name = re.sub(r'[^\w\s-]', '_', name)
    name = re.sub(r'\s+', ' ', name)
    name = name.strip().replace(' ', '_')
    return name


def create_directories(root):
    """
    Create directories for different types of files.

    Args:
        root (str): Root directory where the directories will be created.
    """
    for directory in DIRECTORIES:
        directory_path = os.path.join(root, directory)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)


def process_file(file_path, root):
    """
    Process a file and move it to the corresponding directory based on its extension.

    Args:
        file_path (str): Path to the file to be processed.
        root (str): Root directory where the file is located.
    """
    for directory, extensions in DIRECTORIES.items():
        for extension in extensions:
            if file_path.lower().endswith(extension):
                file_directory = os.path.join(root, directory)
                file_name, file_ext = os.path.splitext(os.path.basename(file_path))
                file_name = normalize(file_name) + file_ext
                destination = os.path.join(file_directory, file_name)
                shutil.move(file_path, destination)
                return

    archive_extensions = [".zip", ".tar", ".gz"]
    if any(file_path.lower().endswith(extension) for extension in archive_extensions):
        archive_name, _ = os.path.splitext(os.path.basename(file_path))
        archive_directory = os.path.join(root, "Archives", archive_name)
        if not os.path.exists(archive_directory):
            os.makedirs(archive_directory)
        shutil.unpack_archive(file_path, archive_directory)

        os.remove(file_path)
        return

    unknown_directory = os.path.join(root, "Unknown")
    if not os.path.exists(unknown_directory):
        os.makedirs(unknown_directory)
    destination = os.path.join(unknown_directory, os.path.basename(file_path))
    shutil.move(file_path, destination)
    return


def process_directory(root):
    """
    Process all files in a directory and move them to their corresponding directories.

    Args:
        root (str): Root directory containing the files to be processed.
    """
    print("File sorting in progress ...")
    create_directories(root)
    for path, _, files in os.walk(root):
        for file in files:
            file_path = os.path.join(path, file)
            process_file(file_path, root)
    print("File sorting completed.")


def delete_empty_directories(root):
    """
    Delete empty directories within the root directory.

    Args:
        root (str): Root directory containing directories to be checked and deleted if empty.
    """
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        if not dirnames and not filenames:
            os.rmdir(dirpath)


def run_file_sorter():
    """
    Entry point to run the file sorting process.
    """
    view = ConsoleView()
    while True:
        path = view.get_input("Enter the path to directory you want to sort (press Enter to return to the previous menu): ")
        if not path:
            return  # Return to the previous menu
        elif os.path.exists(path):
            delete_empty_directories(path)
            create_directories(path)
            process_directory(path)
            return
        else:
            view.display_message("The specified path does not exist. Please enter a valid path or press Enter to return to the previous menu.")


if __name__ == '__main__':
    run_file_sorter()
