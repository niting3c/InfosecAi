import os
import shutil
import tempfile

from scapy.all import rdpcap

from gpt4all import AiModel


def process_pcap_files(directory):
    with tempfile.TemporaryDirectory(prefix='pcap_temp_') as temp_dir:
        try:
            for root, dirs, files in os.walk(directory):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if file_name.endswith(".pcap"):
                        process_pcap_file(file_path)
        except Exception as e:
            print(f"Error processing pcap files: {e}")
        finally:
            # Cleanup the temporary directory
            shutil.rmtree(temp_dir)

def process_pcap_file(file_path):
    try:
        # available models to use
        # GPT4All-13B-snoozy.ggmlv3.q4_0
        # nous-hermes-13b.ggmlv3.q4_0
        gptj = AiModel("TheBloke/orca_mini_13B-GPTQ")
        gptj.model.set_thread_count(6)
        # gptj = gpt4all.GPT4All(os.environ['GPT_MODEL_NAME'])

        packets = rdpcap(file_path)
        file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
        result_file_path = os.path.join(file_name_without_extension + '-snoozy-13b.txt')
        if os.path.isfile(result_file_path):
            os.remove(result_file_path)
        # Iterate over each packet and extract streams
        with open(result_file_path, 'w', encoding="utf-8") as f:
            print(gptj.generate(generate_first_prompt()), file=f)
            print("-" * 40, file=f)
            for packet in packets:
                # Create packet input dictionary
                summary = packet.summary()
                print(f"Sending Prompt: {generate_prompt(summary)}\n\n", file=f)
                print(gptj.generate(generate_prompt(summary)), file=f)
                print("-" * 40, file=f)
                f.flush()
            f.close()
        print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


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
    packet Summary from rdpcap tool: {}
    ### Response
    """.format(
        packet
    )


# Usage: Call the process_pcap_files function with the path to the directory containing the PCAP files
process_pcap_files('./inputs/')
