import os


def create_result_file_path(file_path, extension, output_dir="./output/"):
    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    return os.path.join(output_dir, file_name_without_extension + extension)


def get_file_path(root, file_name):
    return os.path.join(root, file_name)
