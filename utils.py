import os

TEXT_GENERATION = "text-generation"
ZERO_SHOT = "zero-shot-classification"
TEXT_TEXT = "text2text-generation"
CONVERSATIONAL = "conversational"
def create_result_file_path(file_path, extension=".txt", output_dir="./output/", suffix="model"):
    """
    Generates a new file path for a result file in the output directory.

    Args:
        file_path (str): The original file path.
        extension (str): The desired file extension for the new file.
        output_dir (str, optional): The directory for the new file. Defaults to './output/'.
        suffix (str) : The extra folder inside directory for easier seggregation
    Returns:
        str: The path for the new file.
    """
    try:
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if not os.path.exists(output_dir+suffix+"/"):
            os.makedirs(output_dir+suffix+"/")

        file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
        new_file_path = os.path.join(output_dir + suffix + "/", file_name_without_extension + extension)
        print(f"Created new file path: {new_file_path}")
        return new_file_path
    except Exception as e:
        print(f"Error creating result file path: {e}")
        return None


def get_file_path(root, file_name):
    """
    Combines a directory path and a file name into a full file path.

    Args:
        root (str): The directory path.
        file_name (str): The file name.

    Returns:
        str: The full file path.
    """
    try:
        # Create the root directory if it doesn't exist
        if not os.path.exists(root):
            os.makedirs(root)

        file_path = os.path.join(root, file_name)
        print(f"Generated file path: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error generating file path: {e}")
        return None
