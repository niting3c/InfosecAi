import logging
import os

from scapy.utils import rdpcap

from PromptMaker import generate_first_prompt
from llm_model import send_to_model, process_string_input
from utils import create_result_file_path

# Suppress unnecessary scapy warnings
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)


def process_files(directory, classifier,suffix):
    """
    Processes all pcap files in the specified directory.

    Args:
        directory (str): The directory containing pcap files.
        classifier: The classifier model.
    """
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(".pcap"):
                    file_path = os.path.join(root, file_name)
                    analyse_packet(file_path, classifier,suffix)
                    print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing files: {e}")


def analyse_packet(file_path, classifier,suffix):
    """
    Analyzes a pcap file and extracts packet information for further processing.

    Args:
        file_path (str): The path to the pcap file.
        classifier: The classifier model.
    """
    try:
        # Create a path for the result file
        result_file_path = create_result_file_path(file_path, '.txt', "./output/",suffix)

        with open(result_file_path, 'w', encoding="utf-8") as output_file:
            packets = rdpcap(file_path)

            # Send initial prompt to classifier
            process_string_input(generate_first_prompt(len(packets)), classifier, output_file)

            # Loop over each packet and extract necessary information
            for packet in packets:
                payload, protocol = extract_payload_protocol(packet)
                send_to_model(protocol, payload, classifier, output_file)
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
        if packet.haslayer('IP'):
            payload = packet['Raw'].load if packet.haslayer('Raw') else packet['IP'].payload.load
            protocol = "IP"
        elif packet.haslayer('TCP'):
            if packet.haslayer('Raw'):
                payload = packet['Raw'].load
            elif packet.haslayer('FTP'):
                payload = packet['TCP']['Raw'].load if packet['TCP'].haslayer('Raw') else packet['TCP'][
                    'FTP'].payload.load
            else:
                payload = packet['TCP'].payload.load
            protocol = "TCP"
        elif packet.haslayer('UDP'):
            payload = packet['Raw'].load if packet.haslayer('Raw') else packet['UDP'].payload.load
            protocol = "UDP"
        elif packet.haslayer('ICMP'):
            payload = packet['Raw'].load if packet.haslayer('Raw') else packet['ICMP'].payload.load
            protocol = "ICMP"
        else:
            protocol = "unknown"
            payload = "Unknown protocol or No Payload"

        return payload, protocol
    except AttributeError:
        print("Error: Attribute not found in the packet.")
    except Exception as e:
        print(f"Error extracting payload and protocol: {e}")

    return None, None

# Example usage:
# classifier = create_pipeline_model()
# process_files("./inputs/", classifier)