import logging
import os

from scapy.utils import rdpcap

from PromptMaker import generate_first_prompt
from llm_model import send_to_model, process_string_input
from utils import create_result_file_path

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)


def process_files(directory, model, pipeline=False):
    """
    This function processes all pcap files in the specified directory.

    Args:
        directory (str): The path to the directory containing pcap files.
    """
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(".pcap"):
                    file_path = os.path.join(root, file_name)
                    analyse_packet(file_path, model, pipeline)
                    print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing files: {e}")


def analyse_packet(file_path, model, pipeline):
    """
    Analyzes a pcap file and extracts packet information for further processing.

    Args:
        file_path (str): The path to the pcap file.
    """
    result_file_path = create_result_file_path(file_path, '.txt', "./output/")
    with open(result_file_path, 'w', encoding="utf-8") as output_file:
        try:
            packets = rdpcap(file_path)
            # send initial prompt to model
            process_string_input(generate_first_prompt(len(packets)), model, pipeline, output_file)
            for packet in packets:
                if packet.haslayer('IP'):
                    if packet.haslayer('Raw'):
                        payload = packet['Raw'].load
                    else:
                        payload = packet['IP'].payload.load
                    protocol = "IP"
                elif packet.haslayer('TCP'):
                    if packet.haslayer('Raw'):
                        payload = packet['Raw'].load
                    elif packet.haslayer('FTP'):
                        if packet['TCP'].haslayer('Raw'):
                            payload = packet['TCP']['Raw'].load
                        else:
                            payload = packet['TCP']['FTP'].payload.load
                    else:
                        payload = packet['TCP'].payload.load
                    protocol = "TCP"
                elif packet.haslayer('UDP'):
                    if packet.haslayer('Raw'):
                        payload = packet['Raw'].load
                    else:
                        payload = packet['UDP'].payload.load
                    protocol = "UDP"
                elif packet.haslayer('ICMP'):
                    if packet.haslayer('Raw'):
                        payload = packet['Raw'].load
                    else:
                        payload = packet['ICMP'].payload.load
                    protocol = "ICMP"
                else:
                    protocol = "unknown"
                    payload = "Unknown protocol or No Payload"

                send_to_model(protocol, payload, model, pipeline, output_file)
        except AttributeError:
            pass
        except Exception as e:
            print(f"Error processing packet: {e}")


# Example usage:
process_files("./inputs/")
