import os
from pprint import pprint

import tiktoken
from scapy.all import rdpcap


def process_files(directory, tokenizer, counter):
    """
    Recursively process files in the given directory with the specified file extension.
    """
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(".pcap"):
                    file_path = os.path.join(root, file_name)
                    print_token_data(file_path, tokenizer, counter)
    except Exception as e:
        print(f"Error processing files: {e}")


def print_token_data(filename, tokenizer, count_obj={}):
    packets = rdpcap(filename)

    max = 0
    for packet in packets:
        try:
            payload = ''
            if packet.haslayer('IP'):
                if 'Raw' in packet['IP']:
                    payload = packet['IP']['Raw'].load
                else:
                    payload = packet['IP'].payload
            elif packet.haslayer('TCP'):
                if 'Raw' in packet['TCP']:
                    payload = packet['TCP']['Raw'].load
                elif packet['TCP'].haslayer('FTP'):
                    if 'Raw' in packet['TCP']['FTP']:
                        payload = packet['TCP']['FTP']['Raw'].load
                    else:
                        payload = packet['TCP']['FTP'].payload
                else:
                    payload = packet['TCP'].payload
            elif packet.haslayer('UDP'):
                if 'Raw' in packet['UDP']:
                    payload = packet['UDP']['Raw'].load
                else:
                    payload = packet['UDP'].payload
            elif packet.haslayer('ICMP'):
                if 'Raw' in packet['ICMP']:
                    payload = packet['ICMP']['Raw'].load
                else:
                    payload = packet['ICMP'].payload
            else:
                payload = "Unknown protocol or No Payload"

            print(packet.summary())
            print(payload)  # print raw payload data
            print("---" * 40)
            tokens = tokenizer.encode(str(payload))
            if max < len(tokens):
                max = len(tokens)
            count_obj[filename] = max
        except AttributeError:
            continue
        except Exception as e:
            print(f"Error processing packet: {e}")


# Initialize OpenAI tokenizer
enc = tiktoken.encoding_for_model("gpt-4")
counter = {}
process_files("./inputs", enc, counter)
pprint(counter)
