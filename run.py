from transformers import pipeline

from pcap_operations import process_files


def initialize_classifier(hugging_face_model_name):
    """
    Initializes a transformer initialised_model for the given model name.

    Args:
        hugging_face_model_name (str): The name of the transformer model.

    Returns:
        A transformer initialised_model for the given model name.
    """
    try:
        initialised_model = pipeline("zero-shot-classification", model=hugging_face_model_name)
        print(f"Successfully initialized {hugging_face_model_name}")
        return initialised_model
    except Exception as e:
        print(f"Error initializing {hugging_face_model_name}: {e}")
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
