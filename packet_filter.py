import os

from scapy.all import rdpcap, wrpcap, Raw
from scapy.layers.inet import TCP
from termcolor import colored
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

# Define the packet filters
FILTERS = {
    "layers": ["ARP", "ICMP", "ICMPv6MLReport", "IPv6ExtHdrHopByHop", "ICMPv6ND_NS", "IPv6", "LLMNRQuery", "DNS",
               "IGMP", "ICMPv6ND_RS", "igmp"],
    "tcp_flags": ["S", "SA", "A", "R", "RA"],
    "extras": []
}


def packet_filter(packet, filters):
    """
    This function checks if the packet should be kept or not, based on the defined filters.
    """
    # Check for specified layers
    for layer in filters['layers']:
        if packet.haslayer(layer):
            return False

    # Check for specified TCP flags
    if packet.haslayer(TCP):
        for flag in filters['tcp_flags']:
            if flag in packet[TCP].sprintf('%TCP.flags%'):
                return False

    # Check if packet has payload
    if not packet.haslayer(Raw):
        return False

    summary = packet.summary().lower()
    if any(word in summary for word in filters['extras']):
        return False
    return True


def sanitize_pcap(input_file, output_folder='sanitised_inputs', filters={}):
    """
    This function sanitizes a pcap file by removing the packets that match the defined filters.
    """
    print(f"Processing file: {input_file}\n\n")

    # Read packets from the pcap file
    packets = rdpcap(input_file)

    # List to store the packets to keep
    packets_to_keep = []

    for packet in packets:
        # Filter the packet
        if not packet_filter(packet, filters):
            continue
        summary = packet.summary()

        # Print a summary of the packet
        print(colored(summary, 'green'))
        print(colored("Payload: " + summary, 'green'))

        # Ask the user whether to keep the packet
        keep = input(
            colored("Do you want to keep this packet? (yes/y, rest all is no ): ", 'yellow'))

        # If the user presses enter without typing anything, interpret it as 'yes'
        if keep.lower() in ('yes', 'y'):
            packets_to_keep.append(packet)
            print(colored("Packet stored", 'blue'))
        print('\n\n')

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Write the packets to keep to a new pcap file in the output folder
    output_file = os.path.join(output_folder, os.path.basename(input_file))
    if len(packets_to_keep)>0:
        wrpcap(output_file, packets_to_keep)
    print(colored(f"Processed {input_file}\n\n\n", 'blue'))


def process_files(directory, file_extension='.pcap', filters={}):
    """
    This function processes all pcap files in the specified directory.
    """
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(file_extension):
                    file_path = os.path.join(root, file_name)
                    sanitize_pcap(file_path, filters=filters)
    except Exception as e:
        print(f"Error processing files: {e}")


# Call the process_files function to start processing pcap files in the 'inputs' directory
process_files('./inputs', filters= FILTERS)
