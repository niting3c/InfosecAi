from gpt4all import gpt4all
from transformers import pipeline

from gpu_gpt import NewAiModel


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
    gpu_gpt_model = NewAiModel(model_name, base_path)
    gpu_gpt_model.model.set_thread_count(4)
    return gpu_gpt_model


def send_to_model(protocol, payload,model,pipeline):
    print("do somethign here")