import os

import gpt4all
from packet_parser import summarize_streams


def generate_first_prompt():
    return """
    ### Instruction: 
    You are an AI smart packet analyser that excels at finding malicious requests 
    among multiple TCP Streams.
    The prompt below is a task to check wether provided tcp stream is malicious or not.
    Think step by step , carefully . 
    Are the following packet streams malicious ? 
    Think carefully but only answer with either `Malicious` or `Not Malicious`! Do not be verbose .   
    ### Prompt: 
    Review the following packet capture,
    we will provide one by one TCP Stream summary. 
    Check the TCP Stream for any malicious request or attempt.
    Here is the packet file with multiple streams.
    ### Response:
    """


def generate_prompt(packet):
    return """
     ### Instruction: 
     For a provided TCP Stream summary in the Prompt below, check whether its a malicious request or not.
     Think step by step and carefully but only answer with either `Malicious` or `Not Malicious`! Do not be verbose .    
    ###Prompt
    Check the TCP Stream payloads if they have a malicious behaviour , like carrying a malware or doing actions that maybe harmfull.
    Classify if this Packet is Malicious ? 
    ### Response
    """.format(
        packet
    )


def process_files(directory, file_extension, model_path, processor):
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(file_extension):
                    file_path = os.path.join(root, file_name)
                    processor(file_path, model_path)
    except Exception as e:
        print(f"Error processing files: {e}")


def get_file_path(root, file_name):
    return os.path.join(root, file_name)


def create_gpt_model(model_name):
    gptj = gpt4all.GPT4All(model_name)
    gptj.model.set_thread_count(4)
    return gptj


def create_result_file_path(file_path, extension):
    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    return os.path.join('./output/' + file_name_without_extension + extension)


def analyze_streams(file_path, result_file_path, gptj=None):
    streams = summarize_streams(file_path)
    with open(result_file_path, 'w', encoding="utf-8") as f:
        print(gptj.generate(generate_first_prompt()), file=f)
        print("-" * 40, file=f)
        for stream_index, stream in streams.items():
            print(f"Stream {stream_index}:\n{stream}", file=f)
            prompt = generate_prompt(str(stream))
            print(gptj.generate(prompt), file=f)
            print("-" * 40, file=f)
            f.flush()
        f.close()


def process_pcap_file(file_path, model_path):
    try:
        gptj = create_gpt_model(model_path)
        result_file_path = create_result_file_path(file_path, '-snoozy-13b.txt')
        if os.path.isfile(result_file_path):
            os.remove(result_file_path)
        analyze_streams(file_path, result_file_path, gptj)
        print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


# available models to use
# GPT4All-13B-snoozy.ggmlv3.q4_0
# nous-hermes-13b.ggmlv3.q4_0
model_path = 'GPT4All-13B-snoozy.ggmlv3.q4_0'
# Usage: Call the process_files function with the path to the directory containing the PCAP files
process_files('./inputs/', ".pcap", model_path, process_pcap_file)
