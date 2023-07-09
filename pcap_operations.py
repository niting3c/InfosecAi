import os
from scapy.utils import rdpcap
from llm_model import send_to_model
import logging

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

def process_files(directory):
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
                    analyse_packet(file_path)
    except Exception as e:
        print(f"Error processing files: {e}")


def analyse_packet(file_path):
    """
    Analyzes a pcap file and extracts packet information for further processing.

    Args:
        file_path (str): The path to the pcap file.
    """
    try:
        packets = rdpcap(file_path)
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

            send_to_model(protocol, payload)
    except AttributeError:
        pass
    except Exception as e:
        print(f"Error processing packet: {e}")


# Example usage:
process_files("/path/to/directory")
