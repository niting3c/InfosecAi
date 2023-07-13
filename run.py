import torch
from transformers import pipeline

from pcap_operations import process_files


def initialize_classifier(hugging_face_model_name, model_type):
    """
    Initializes a transformer initialised_model for the given model name.

    Args:
        hugging_face_model_name (str): The name of the transformer model.
        model_type: type of model used
    Returns:
        A transformer initialised_model for the given model name.

    """
    try:
        device = -1
        if torch.cuda.is_available():
            device = 0
        initialised_model = pipeline(model_type, model=hugging_face_model_name, device=device)
        print(f"Successfully initialized {hugging_face_model_name}")
        return initialised_model
    except Exception as e:
        print(f"Error initializing {hugging_face_model_name}: {e}")
        return None


# Dictionary of transformer models to be used
models = [
    {"suffix": "vicuna", "model_name": "TheBloke/vicuna-13B-1.1-HF", "type": "text-generation"},
    {"suffix": "deepnight", "model_name": "deepnight-research/zsc-text", "type": "zero-shot-classification"},
    {"suffix": "llama", "type": "text-generation", "model_name": "openlm-research/open_llama_7b"},
    {"suffix": "fb", "model_name": "facebook/bart-large-mnli", "type": "zero-shot-classification"},
    {"suffix": "google", "type": "text2text-generation", "model_name": "google/flan-t5-xxl"},

    # {"suffix": "deberta-fever", "model_name": "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",
    # "type": "zero-shot-classification"},
    # {"suffix": "sileod", "model_name": "sileod/deberta-v3-base-tasksource-nli", "type": "zero-shot-classification"}
]

# Directory containing pcap files to be processed
directory = './inputs'

# Process the pcap files for each model
for entry in models:
    classifier = initialize_classifier(entry["model_name"], entry["type"])
    process_files(directory, classifier, entry["suffix"])
