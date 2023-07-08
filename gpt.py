import os

import gpt4all
import pyshark

from gpu_gpt import NewAiModel


def generate_first_prompt(packet_count):
    return """
        You are an advanced AI that detects malicious requests by parsing the various payloads of the protocols.
        Please analyze the {0} packets provided in the follow-up prompts 
        and determine if each packet is malicious or not. 
        Consider examining the payload, headers, and protocols in a step-by-step analysis.
        Your response should be a concise categorization of either \"Malicious\" or \"Not Malicious\". 
        Do not provide any additional information or context beyond this categorization. 
        Note that an empty payload is not considered malicious.
        As an AI model specialized in detecting malicious activity or network attacks you should carefully examine the payload and follow a step-by-step analysis.
        Avoid providing additional information or context beyond this categorization.
        The prompt for each packet will be provided after this instruction.
        ###Response:
    """.format(packet_count)


def generate_prompt(protocol, payload):
    return """
    ### Instructions:
    Your Task is to determine whether the below prompt containing Protocol and payload,is a malicious
    request or not? Follow the instructions provided in the beginning.
    Your response should be a concise categorization either : `Malicious` or `Not Malicious`.
    ### Prompt:
    protocol:{0}
    payload:{1}
    ### Response:
    """.format(protocol, payload)


def process_files(directory, file_extension, model_path, processor, suffix=None, gpu=False, base_path=None):
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(file_extension):
                    file_path = os.path.join(root, file_name)
                    processor(file_path, model_path, suffix, gpu, base_path)
    except Exception as e:
        print(f"Error processing files: {e}")


def get_file_path(root, file_name):
    return os.path.join(root, file_name)


def create_gpt_model(model_name):
    gptj = gpt4all.GPT4All(model_name)
    gptj.model.set_thread_count(4)
    return gptj


def create_gpu_gpt_model(model_name, base_path=None):
    if '' == base_path or None == base_path:
        base_path = model_name
    gptj = NewAiModel(model_name, base_path)
    # gptj = gpt4all.GPT4All(model_name)
    gptj.model.set_thread_count(4)
    return gptj


def create_result_file_path(file_path, extension):
    file_name_without_extension = os.path.splitext(
        os.path.basename(file_path))[0]
    return os.path.join('./output/' + file_name_without_extension + extension)


def analyze_streams(file_path, result_file_path, gptj=None):
    cap = pyshark.FileCapture(file_path, keep_packets=False)
    with open(result_file_path, 'w', encoding="utf-8") as f:
        for packet in cap:
            try:
                # Check if the packet has a payload
                if 'data' in packet:
                    payload = packet.data.data
                    print("Payload:", payload)

                # Check if the packet has a protocol type
                if 'frame_info' in packet:
                    protocol = packet.frame_info.protocol
                    print("Protocol:", protocol)

                generated_text = gptj.generate(generate_prompt(protocol, payload))

            except AttributeError:
                pass
            except Exception as e:
                generated_text = f"ERROR: {str(e)}"
            finally:
                print(generated_text, file=f)
                print("-" * 40, file=f)
                f.flush()
        cap.close()
        f.close()


def process_pcap_file(file_path, model_path, suffix="", gpu=False, base_path=None):
    try:
        gptj = None
        if gpu:
            gptj = create_gpu_gpt_model(model_path, base_path)
        else:
            gptj = create_gpt_model(model_path)
        result_file_path = create_result_file_path(
            file_path, '-' + suffix + '.txt')
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

# Non-GPU Library used , default Gpt4all
process_files('./inputs/', ".pcap", 'GPT4All-13B-snoozy.ggmlv3.q4_0', process_pcap_file, "snoozy")

# process_files('./inputs/', ".pcap", 'orca-mini-13b.ggmlv3.q4_0', process_pcap_file,"orca")

# process_files('./inputs/', ".pcap", 'nous-hermes-13b.ggmlv3.q4_0', process_pcap_file,"nous-hermes")


# custom nomic code technically gpt4all but uses transformers instead
# TheBloke/airoboros-7b-gpt4-fp16 has 4096 context size
process_files('./inputs/', ".pcap", 'TheBloke/airoboros-7b-gpt4-fp16',
              process_pcap_file, "airoboros", True)

process_files('./inputs/', ".pcap", 'TheBloke/Nous-Hermes-13B-GPTQ',
              process_pcap_file, "nous-hermes", True, "nous-hermes-13b-GPTQ-4bit-128g.no-act.order")
