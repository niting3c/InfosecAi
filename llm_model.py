from transformers import pipeline

from PromptMaker import generate_prompt, generate_part_prompt, generate_part_prompt_final

candidate_labels = ['malicious', 'non-malicious', 'attack', 'normal']


def create_pipeline_model(model_name="openchat/openchat_8192"):
    return pipeline("text-generation", model=model_name)


def pipe_response_generate(classifier, classifier_input_str):
    return classifier(classifier_input_str, candidate_labels)


def process_string_input(classifier_input_str, classifier, outputfile):
    print("Input:\n", file=outputfile)
    print(classifier_input_str, file=outputfile)
    result = pipe_response_generate(classifier_input_str, candidate_labels)
    print(f"String processed with result = {result}", file=outputfile)
    print("-----" * 40, file=outputfile)
    print(f"Processing classifier_input_str and sending to model and pipeline={classifier}")


def send_to_model(protocol, payload, classifier, outputfile):
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

            # Do something with the batch here
            print(f"Processing batch {i + 1} with protocol: {protocol}")
            print(f"Batch content: {batch}")
            process_string_input(generate_part_prompt(protocol, payload, i + 1, batch), classifier, outputfile)
            # After doing something with the batch, you may want to pass it to your classifier/classifier here

        process_string_input(generate_part_prompt_final(), classifier, outputfile)
    else:
        process_string_input(generate_prompt(protocol, payload), classifier, outputfile)
