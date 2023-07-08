import os

import gpt4all
import pyshark
import transformers
from gpu_gpt import NewAiModel
import matplotlib.pyplot as plt


def process_files(directory, file_extension, model_path, suffix=None, gpu=False, base_path=None):
    """
    Recursively process files in the given directory with the specified file extension.
    """
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(file_extension):
                    file_path = os.path.join(root, file_name)
                    process_pcap_file(file_path, model_path, suffix, gpu, base_path)
    except Exception as e:
        print(f"Error processing files: {e}")


def get_file_path(root, file_name):
    """
    Get the full file path given the root directory and file name.
    """
    return os.path.join(root, file_name)


def create_gpt_model(model_name):
    """
    Create a GPT model instance.
    """
    gpt_model = gpt4all.GPT4All(model_name)
    gpt_model.model.set_thread_count(4)
    return gpt_model


def create_gpu_gpt_model(model_name, base_path=None):
    """
    Create a GPU GPT model instance.
    """
    if base_path == '' or base_path is None:
        base_path = model_name
    gpu_gpt_model = NewAiModel(model_name, base_path)
    gpu_gpt_model.model.set_thread_count(4)
    return gpu_gpt_model


def create_result_file_path(file_path, extension):
    """
    Create the result file path based on the original file path and the desired extension.
    """
    file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
    return os.path.join('./output/', file_name_without_extension + extension)


def analyze_streams(file_path, result_file_path, gpt_model=None):
    """
    Analyze packet streams in the given file and generate responses using the AI model.
    """
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

                generated_text = gpt_model.generate(generate_prompt(protocol, payload))

            except AttributeError:
                pass
            except Exception as e:
                generated_text = f"ERROR: {str(e)}"
            finally:
                print(generated_text, file=f)
                print("-" * 40, file=f)
                f.flush()
    cap.close()  # Close the capture file handle
    f.close()  # Close the result file handle


def process_pcap_file(file_path, model_path, suffix="", gpu=False, base_path=None):
    """
    Process a single PCAP file using the specified model and generate the result file.
    """
    try:
        gpt_model = None
        if gpu:
            gpt_model = create_gpu_gpt_model(model_path, base_path)
        else:
            gpt_model = create_gpt_model(model_path)
        result_file_path = create_result_file_path(file_path, '-' + suffix + '.txt')
        if os.path.isfile(result_file_path):
            os.remove(result_file_path)
        analyze_streams(file_path, result_file_path, gpt_model)
        print_token_data(file_path)
        print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


# process files based on models
# process with lates open


# available models to use
# GPT4All-13B-snoozy.ggmlv3.q4_0
# nous-hermes-13b.ggmlv3.q4_0
# Usage: Call the process_files function with the path to the directory containing the PCAP files

# Non-GPU Library used, default Gpt4all
process_files('./inputs/', ".pcap", 'GPT4All-13B-snoozy.ggmlv3.q4_0', "snoozy")

# process_files('./inputs/', ".pcap", 'orca-mini-13b.ggmlv3.q4_0', process_pcap_file,"orca")

# process_files('./inputs/', ".pcap", 'nous-hermes-13b.ggmlv3.q4_0', process_pcap_file,"nous-hermes")


# custom nomic code technically gpt4all but uses transformers instead
# TheBloke/airoboros-7b-gpt4-fp16 has 4096 context size
process_files('./inputs/', ".pcap", 'TheBloke/airoboros-7b-gpt4-fp16',
              "airoboros", True)

process_files('./inputs/', ".pcap", 'TheBloke/Nous-Hermes-13B-GPTQ',
              "nous-hermes", True, "nous-hermes-13b-GPTQ-4bit-128g.no-act.order")
