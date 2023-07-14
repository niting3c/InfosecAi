from transformers import pipeline

from PromptMaker import generate_prompt, generate_part_prompt, generate_part_prompt_final
from utils import CONVERSATIONAL, TEXT_GENERATION, ZERO_SHOT, TEXT_TEXT
candidate_labels = ['malicious', 'not malicious', 'attack']


def create_pipeline_model(hugging_face_model_name):
    """
    Creates a pipeline model for text generation tasks.

    Args:
        hugging_face_model_name (str): The name of the model.

    Returns:
        A pipeline model.
    """
    try:
        return pipeline("text-generation", model=hugging_face_model_name)
    except Exception as e:
        print(f"Error creating pipeline model: {e}")
        return None


def pipe_response_generate(initialised_model, classifier_input_str):
    """
    Generate a response from the classifier for the given input string.

    Args:
        initialised_model: The classifier model.
        classifier_input_str (str): The input string for the classifier.

    Returns:
        The response from the classifier.
    """
    try:
        return initialised_model(classifier_input_str, candidate_labels)
    except Exception as e:
        print(f"Error generating response from classifier: {e}")
        return None


def process_string_input(input_string, model_entry, outputfile):
    """
    Processes the input string with the classifier and write the result to output file.

    Args:
        input_string (str): The input string for the classifier.
        model_entry: Model entry with all the references
        outputfile: The output file.
    """
    print("-----" * 40, file=outputfile)
    try:
        if model_entry["type"] == CONVERSATIONAL:
            print(f"\nInput:{input_string}\n", file=outputfile)
            conversation_input = model_entry["chat"].add_user_input(input_string)
            model_entry["chat"] = conversation_input
            result = model_entry["model"](conversation_input)
        elif model_entry["type"] == ZERO_SHOT:
            result = pipe_response_generate(model_entry["model"], input_string)
        else:
            # update this as needed
            result = pipe_response_generate(model_entry["model"], input_string)
        print(f"\nString processed with result = {str(result)}", file=outputfile)
        print("-----" * 40, file=outputfile)
    except Exception as e:
        print(f"Error processing string input: {e}")


def prepare_input_strings(protocol, payload, model_entry):
    """
    Sends the protocol and payload to the model for classification.

    Args:
        protocol (str): The protocol.
        payload: The payload.
        model_entry: The model_entry model.
        outputfile: The output file.
    """
    try:
        # Calculate the number of batches
        batch_size = 800
        num_batches = len(payload) // batch_size
        if len(payload) % batch_size:
            num_batches += 1

        # Process the payload
        if num_batches > 1:
            # Split the payload into batches
            for i in range(num_batches):
                start_index = i * batch_size
                end_index = start_index + batch_size
                model_entry["str"].append(
                    generate_part_prompt(protocol,
                                         payload[start_index:end_index],
                                         i + 1,
                                         num_batches))
            model_entry["str"].append(generate_part_prompt_final())
        else:
            # Directly process the payload without creating batches
            model_entry["str"].append(generate_prompt(protocol, payload))
    except Exception as e:
        print(f"Error sending to model: {e}")
