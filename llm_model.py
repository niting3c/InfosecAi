from transformers import pipeline

from PromptMaker import generate_prompt, generate_part_prompt, generate_part_prompt_final

TEXT_GENERATION = "text-generation"
ZERO_SHOT = "zero-shot-classification"
TEXT_TEXT = "text2text-generation"
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
    try:
        print("-----" * 40, file=outputfile)
        if model_entry["type"] != ZERO_SHOT:
            print(f"\nInput:{input_string}\n", file=outputfile)
        result = pipe_response_generate(model_entry["model"], input_string)
        print(f"\nString processed with result = {str(result)}", file=outputfile)
        print("-----" * 40, file=outputfile)
    except Exception as e:
        print(f"Error processing string input: {e}")


def send_to_model(protocol, payload, model_entry, outputfile):
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
        batch_size = 900
        num_batches = len(payload) // batch_size
        if len(payload) % batch_size:
            num_batches += 1

        # Process the payload
        if num_batches > 1:
            # Split the payload into batches
            for i in range(num_batches):
                start_index = i * batch_size
                end_index = start_index + batch_size
                batch = payload[start_index:end_index]

                print(f"Processing batch {i + 1} with protocol: {protocol}")
                print(f"Batch content: {batch}")
                process_string_input(generate_part_prompt(protocol, payload, i + 1, num_batches), model_entry,
                                     outputfile)
            process_string_input(generate_part_prompt_final(), model_entry, outputfile)
        else:
            # Directly process the payload without creating batches
            print(f"Processing payload with protocol: {protocol}")
            print(f"Payload content: {payload}")
            process_string_input(generate_prompt(protocol, payload), model_entry, outputfile)
    except Exception as e:
        print(f"Error sending to model: {e}")
