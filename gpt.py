import os

import gpt4all
from packet_parser import summarize_streams
from gpu_gpt import NewAiModel

def generate_prompt(packet):
    return """
    ### Instructions:
    [AI Smart TCP/UDP Packet Stream Analyzer]
    Your task is to analyze the provided TCP/UDP packet stream in the prompt and determine if it is malicious or not. 
    As an AI model specialized in detecting malicious activity, you should carefully examine the payload and follow a step-by-step analysis.
    Your response should be a concise categorization: either `Malicious` or `Not Malicious`.
    Avoid providing additional information or context beyond this categorization.
    ### Prompt:
    Analyze the content of the following packet stream:
    {0}
    ### Response:
    """.format(packet)

def process_files(directory, file_extension, model_path, processor,suffix=None):
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(file_extension):
                    file_path = os.path.join(root, file_name)
                    processor(file_path, model_path,suffix)
    except Exception as e:
        print(f"Error processing files: {e}")


def get_file_path(root, file_name):
    return os.path.join(root, file_name)


def create_gpt_model(model_name):
    gptj= NewAiModel(model_name)
    #gptj = gpt4all.GPT4All(model_name)
    gptj.model.set_thread_count(4)
    return gptj


def create_result_file_path(file_path, extension):
    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    return os.path.join('./output/' + file_name_without_extension + extension)


def analyze_streams(file_path, result_file_path, gptj=None):
    streams = summarize_streams(file_path)
    with open(result_file_path, 'w', encoding="utf-8") as f:
        for stream_index, stream in streams.items():
            print(f"Stream {stream_index}:\n{stream}", file=f)
            prompt = generate_prompt(str(stream))
            print(gptj.generate(prompt), file=f)
            print("-" * 40, file=f)
            f.flush()
        f.close()


def process_pcap_file(file_path, model_path,suffix=""):
    try:
        gptj = create_gpt_model(model_path)
        result_file_path = create_result_file_path(file_path, '-'+suffix+'.txt')
        if os.path.isfile(result_file_path):
            os.remove(result_file_path)
        analyze_streams(file_path, result_file_path, gptj)
        print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


# available models to use
# GPT4All-13B-snoozy.ggmlv3.q4_0
# nous-hermes-13b.ggmlv3.q4_0
# Usage: Call the process_files function with the path to the directory containing the PCAP files

#Non-GPU Library used , default Gpt4all
#process_files('./inputs/', ".pcap", 'GPT4All-13B-snoozy.ggmlv3.q4_0', process_pcap_file,"snoozy")

#process_files('./inputs/', ".pcap", 'orca-mini-13b.ggmlv3.q4_0', process_pcap_file,"orca")

#process_files('./inputs/', ".pcap", 'nous-hermes-13b.ggmlv3.q4_0', process_pcap_file,"nous-hermes")


#custom nomic code technically gpt4all but uses transformers instead
process_files('./inputs/', ".pcap", 'GPT4All-13B-snoozy.ggmlv3.q4_0', process_pcap_file,"snoozy")

process_files('./inputs/', ".pcap", 'orca-mini-13b.ggmlv3.q4_0', process_pcap_file,"orca")

process_files('./inputs/', ".pcap", 'nous-hermes-13b.ggmlv3.q4_0', process_pcap_file,"nous-hermes")
