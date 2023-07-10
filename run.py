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


# Dictionary of transformer models to be used
models = {
    "deepnight": "deepnight-research/zsc-text",
    "fb": "facebook/bart-large-mnli",
    "deberta-fever": "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",
    "sileod": "sileod/deberta-v3-base-tasksource-nli"
}

# Directory containing pcap files to be processed
directory = './inputs'

# Process the pcap files for each model
for suffix, model_name in models.items():
    classifier = initialize_classifier(model_name)
    if classifier:
        process_files(directory, classifier, suffix)
    else:
        print(f"Skipping {model_name} due to initialization error.")
