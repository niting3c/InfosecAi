import os

import pyshark



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
