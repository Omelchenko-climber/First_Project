import os
import argparse
import shutil
import re


# список директорий для создания
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
    # транслитерация кириллических символов на латиницу
    translit = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
                'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
                'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
                'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shc', 'ъ': '',
                'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}
    name = name.lower()
    for cyr, lat in translit.items():
        name = name.replace(cyr, lat)
    # замена недопустимых символов на '_'
    name = re.sub(r'[^\w\s-]', '_', name)
    # удаление повторяющихся пробелов
    name = re.sub(r'\s+', ' ', name)
    # замена пробелов на '_'
    name = name.strip().replace(' ', '_')
    return name


def create_directories(root):
    """
    Создает директории для файлов
    """
    for directory in DIRECTORIES:
        directory_path = os.path.join(root, directory)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)


def process_file(file_path, root):
    """
    Обрабатывает файл и перемещает его в соответствующую директорию
    """
    for directory, extensions in DIRECTORIES.items():
        for extension in extensions:
            if file_path.lower().endswith(extension):
                file_directory = os.path.join(root, directory)
                # разделение пути к файлу на имя и расширение
                file_name, file_ext = os.path.splitext(os.path.basename(file_path))
                # переименование файла с помощью функции normalize
                file_name = normalize(file_name) + file_ext
                destination = os.path.join(file_directory, file_name)
                shutil.move(file_path, destination)
                return

    # Если расширение файла не найдено, проверить, является ли файл архивом
    archive_extensions = [".zip", ".tar", ".gz"]
    if any(file_path.lower().endswith(extension) for extension in archive_extensions):
        # распаковка архива в папку Archives
        archive_name, _ = os.path.splitext(os.path.basename(file_path))
        archive_directory = os.path.join(root, "Archives", archive_name)
        if not os.path.exists(archive_directory):
            os.makedirs(archive_directory)
        shutil.unpack_archive(file_path, archive_directory)

        # удаление архива
        os.remove(file_path)
        return

    # Если файл не является архивом и расширение файла не найдено, переместить файл в папку "Unknown"
    unknown_directory = os.path.join(root, "Unknown")
    if not os.path.exists(unknown_directory):
        os.makedirs(unknown_directory)
    destination = os.path.join(unknown_directory, os.path.basename(file_path))
    shutil.move(file_path, destination)
    return


def process_directory(root):
    """
    Обрабатывает все файлы в директории
    """
    create_directories(root)
    for path, _, files in os.walk(root):
        for file in files:
            file_path = os.path.join(path, file)
            process_file(file_path, root)


def delete_empty_directories(root):
    """
    Удаляет пустые директории из корневой директории
    """
    excluded_directories = [os.path.join(args.path)]

    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        if not dirnames and not filenames and dirpath not in excluded_directories:
            os.rmdir(dirpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--exclude", nargs='+')
    args = parser.parse_args()
    delete_empty_directories(args.path)
    process_directory(args.path)
