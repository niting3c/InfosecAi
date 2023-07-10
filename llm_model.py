from transformers import pipeline

from PromptMaker import generate_prompt, generate_part_prompt, generate_part_prompt_final

candidate_labels = ['malicious', 'non-malicious', 'attack', 'normal']


def create_pipeline_model(model_name):
    """
    Creates a pipeline model for text generation tasks.

    Args:
        model_name (str): The name of the model.

    Returns:
        A pipeline model.
    """
    try:
        return pipeline("text-generation", model=model_name)
    except Exception as e:
        print(f"Error creating pipeline model: {e}")
        return None


def pipe_response_generate(classifier, classifier_input_str):
    """
    Generate a response from the classifier for the given input string.

    Args:
        classifier: The classifier model.
        classifier_input_str (str): The input string for the classifier.

    Returns:
        The response from the classifier.
    """
    try:
        return classifier(classifier_input_str, candidate_labels)
    except Exception as e:
        print(f"Error generating response from classifier: {e}")
        return None


def process_string_input(classifier_input_str, classifier, outputfile):
    """
    Processes the input string with the classifier and write the result to output file.

    Args:
        classifier_input_str (str): The input string for the classifier.
        classifier: The classifier model.
        outputfile: The output file.
    """
    try:
        print("Input:\n", file=outputfile)
        print(classifier_input_str, file=outputfile)
        result = pipe_response_generate(classifier_input_str, classifier)
        print(f"String processed with result = {result}", file=outputfile)
        print("-----" * 40, file=outputfile)
    except Exception as e:
        print(f"Error processing string input: {e}")


def send_to_model(protocol, payload, classifier, outputfile):
    """
    Sends the protocol and payload to the model for classification.

    Args:
        protocol (str): The protocol.
        payload: The payload.
        classifier: The classifier model.
        outputfile: The output file.
    """
    try:
        # Calculate the number of batches
        batch_size = 1600
        num_batches = len(payload) // batch_size
        if len(payload) % batch_size:
            num_batches += 1

        # Split the payload into batches
        for i in range(num_batches):
            start_index = i * batch_size
            end_index = start_index + batch_size
            batch = payload[start_index:end_index]

            print(f"Processing batch {i + 1} with protocol: {protocol}")
            print(f"Batch content: {batch}")
            process_string_input(generate_part_prompt(protocol, payload, i + 1, batch), classifier, outputfile)

        process_string_input(generate_part_prompt_final(), classifier, outputfile)
    except Exception as e:
        print(f"Error sending to model: {e}")
    else:
        try:
            process_string_input(generate_prompt(protocol, payload), classifier, outputfile)
        except Exception as e:
            print(f"Error processing string input: {e}")
