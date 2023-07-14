import logging

import torch
from transformers import pipeline

from pcap_operations import process_files
from utils import CONVERSATIONAL, TEXT_GENERATION, ZERO_SHOT, TEXT_TEXT

# Suppress unnecessary scapy warnings
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)


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
        if model_type is not None:
            initialised_model = pipeline(model_type, model=hugging_face_model_name, device=device)
        else:
            initialised_model = pipeline(model=hugging_face_model_name, device=device)
        print(f"Successfully initialized {hugging_face_model_name}")
        return initialised_model
    except Exception as e:
        print(f"Error initializing {hugging_face_model_name}: {e}")
        return None


# Dictionary of transformer models to be used
models = [

    {"model": None, "chat": None, "str": [], "suffix": "microsoft", "type": CONVERSATIONAL,
     "model_name": "microsoft/DialoGPT-medium"},
    {"model": None, "chat": None, "str": [], "suffix": "llama", "type": TEXT_GENERATION,
     "model_name": "openlm-research/open_llama_7b"},
    {"model": None, "chat": None, "str": [], "suffix": "fb", "type": ZERO_SHOT,
     "model_name": "facebook/bart-large-mnli"},
    {"model": None, "chat": None, "str": [], "suffix": "google", "type": TEXT_TEXT,
     "model_name": "google/flan-t5-xxl"},
    {"model": None, "chat": None, "str": [], "suffix": "vicuna", "type": TEXT_GENERATION,
     "model_name": "TheBloke/vicuna-13B-1.1-HF"},
    # {"suffix": "deberta-fever", "model_name": "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",
    # {"model": None, "suffix": "deepnight", "type": ZERO_SHOT, "model_name": "deepnight-research/zsc-text"},
    # "type": "zero-shot-classification"},
    # {"suffix": "sileod", "model_name": "sileod/deberta-v3-base-tasksource-nli", "type": "zero-shot-classification"}
]

# Directory containing pcap files to be processed
directory = './inputs'

# Process the pcap files for each model
for entry in models:
    entry["model"] = initialize_classifier(entry["model_name"], entry["type"])
    process_files(directory, entry)
    del entry  # save some space
