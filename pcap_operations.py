import logging
import os

from scapy.all import rdpcap

from PromptMaker import generate_first_prompt, generate_text_chat_last_prompt
from llm_model import send_to_model, ZERO_SHOT, process_string_input
from utils import create_result_file_path

# Suppress unnecessary scapy warnings
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)


def process_files(directory, model_entry):
    """
    Processes all pcap files in the specified directory.

    Args:
        directory (str): The directory containing pcap files.
    """
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(".pcap"):
                    file_path = os.path.join(root, file_name)
                    analyse_packet(file_path, model_entry)
                    print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing files: {e}")


def analyse_packet(file_path, model_entry):
    """
    Analyzes a pcap file and extracts packet information for further processing.

    Args:
        file_path (str): The path to the pcap file.
        classifier: The classifier model.
    """
    try:
        # Create a path for the result file
        result_file_path = create_result_file_path(file_path, '.txt', "./output/", model_entry["suffix"])

        with open(result_file_path, 'w', encoding="utf-8") as output_file:
            packets = rdpcap(file_path)
            # # Send initial prompt to classifier
            if model_entry[type] != ZERO_SHOT:
                process_string_input(generate_first_prompt(len(packets)), model_entry, output_file)
            # Loop over each packet and extract necessary information
            for packet in packets:
                protocol, payload = extract_payload_protocol(packet)
                send_to_model(protocol, payload, model_entry, output_file)
            if model_entry[type] != ZERO_SHOT:
                process_string_input(generate_text_chat_last_prompt(), model_entry, output_file)
        print(f"\nfile processed successfully: {file_path}\n")
    except Exception as e:
        print(f"Error analysing packet: {e}")


def extract_payload_protocol(packet):
    """
    Extracts payload and protocol from the packet.

    Args:
        packet: The packet to process.

    Returns:
        tuple: The payload and protocol.
    """
    try:
        payload = repr(packet.payload)
        if packet.haslayer('IP'):
            protocol = "IP"
        elif packet.haslayer('TCP'):
            if packet.payload.haslayer('FTP'):
                protocol = "TCP"
            else:
                protocol = "TCP"
        elif packet.haslayer('UDP'):
            protocol = "UDP"
        elif packet.haslayer('ICMP'):
            protocol = "ICMP"
        else:
            protocol = "unknown"

        print("Payload:", payload)
        print("Protocol:", protocol)

        return protocol, payload
    except AttributeError:
        print("Error: Attribute not found in the packet.")
    except Exception as e:
        print(f"Error extracting payload and protocol: {e}")

    return "", ""

# Example usage:
# classifier = create_pipeline_model()
# process_files("./inputs/", None, "hi")
