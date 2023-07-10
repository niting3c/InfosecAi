from gpt4all import gpt4all
from transformers import pipeline

from PromptMaker import generate_prompt, generate_part_prompt, generate_part_prompt_final
from gpu_gpt import new_ai_model


def create_pipeline_model(model_name="openchat/openchat_8192"):
    return pipeline("text-generation", model=model_name)


def pipe_response_generate(pipe, str):
    return pipe(str)


def create_gpt_model(model_name):
    gpt_model = gpt4all.GPT4All(model_name)
    gpt_model.model.set_thread_count(4)
    return gpt_model


def create_gpu_gpt_model(model_name, base_path=None):
    if base_path == '' or base_path is None:
        base_path = model_name
    gpu_gpt_model = new_ai_model(model_name, base_path)
    gpu_gpt_model.model.set_thread_count(4)
    return gpu_gpt_model


def process_string_input(str, model, pipeline, outputfile):
    print(f"Processing input and sending to model and pipeline={pipeline}")
    

def send_to_model(protocol, payload, model, pipeline, outputfile):
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
            print(f"Processing batch {i + 1} with protocol: {protocol}, model: {model}, pipeline: {pipeline}")
            print(f"Batch content: {batch}")
            process_string_input(generate_part_prompt(protocol, payload, i + 1, batch), model, pipeline, outputfile)
            # After doing something with the batch, you may want to pass it to your model/pipeline here

        process_string_input(generate_part_prompt_final(), model, pipeline, outputfile)
    else:
        process_string_input(generate_prompt(protocol, payload), model, pipeline, outputfile)
