from transformers import pipeline
from pcap_operations import process_files


def initialize_classifier(model_name):
    """
    Initializes a transformer classifier for the given model name.

    Args:
        model_name (str): The name of the transformer model.

    Returns:
        A transformer classifier for the given model name.
    """
    try:
        classifier = pipeline("zero-shot-classification", model=model_name)
        print(f"Successfully initialized {model_name}")
        return classifier
    except Exception as e:
        print(f"Error initializing {model_name}: {e}")
        return None


# List of transformer models to be used
models = [
    "deepnight-research/zsc-text",
    "facebook/bart-large-mnli",
    "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",
    "sileod/deberta-v3-base-tasksource-nli"
]

# Directory containing pcap files to be processed
directory = './inputs'

# Initialize each model and process the pcap files
for model in models:
    classifier = initialize_classifier(model)
    if classifier:
        process_files(directory, classifier)
    else:
        print(f"Skipping {model} due to initialization error.")
