import logging
import os

from scapy.all import rdpcap, wrpcap, Raw
from scapy.layers.dns import DNS
from scapy.layers.http import HTTP
from scapy.layers.inet import TCP
from scapy.packet import Padding
from termcolor import colored

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

# Define the packet filters
FILTERS = {
    "layers": ["ARP", "ICMP", "ICMPv6MLReport", "IPv6ExtHdrHopByHop", "ICMPv6ND_NS", "IPv6", "LLMNRQuery",
               "IGMP", "ICMPv6ND_RS", "igmp", "DHCP6_Advertise", "DHCP6_Request"],
    "tcp_flags": [],
    "extras": []
}


def get_readable_payload(packet):
    """
    This function tries to decode the packet payload and checks for potential signs of malicious activity.
    """
    payload_info = ""

    # If the packet has Raw layer (meaning it has payload)
    if packet.haslayer(Raw):
        try:
            # Try to decode the payload
            payload = bytes(packet[Raw].load).decode('UTF8', 'replace')
            payload_info += "\nRaw Layer Payload: " + payload
        except:
            payload_info += "\nRaw Layer Payload: " + repr(packet[Raw].load)

    # If the packet has Padding layer
    elif packet.haslayer(Padding):
        try:
            # Try to decode the padding
            padding = bytes(packet[Padding].load).decode('UTF8', 'replace')
            payload_info += "\nPadding Layer Payload: " + padding
        except:
            payload_info += "\nPadding Layer Payload: " + repr(packet[Padding].load)

    # If the packet has TCP layer
    elif packet.haslayer(TCP):
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        payload_info += "\nTCP Layer: Src Port = " + str(src_port) + ", Dst Port = " + str(dst_port)

    # If the packet has HTTP layer
    elif packet.haslayer(HTTP):
        http_info = packet[HTTP].fields
        payload_info += "\nHTTP Layer: " + str(http_info)

    # If the packet has DNS layer
    elif packet.haslayer(DNS):
        dns_info = packet[DNS].fields
        payload_info += "\nDNS Layer: " + str(dns_info)

    return payload_info


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

    for i, packet in enumerate(packets, 1):
        # Filter the packet
        if not packet_filter(packet, filters):
            continue
        summary = packet.summary()

        # Print a summary of the packet
        print(colored(f"Packet No: `{i}`" + summary, 'magenta'))
        print(colored("Payload: " + get_readable_payload(packet), 'green'))

        # Ask the user whether to keep the packet
        keep = input(
            colored("Do you want to keep this packet? (yes/y, rest all is no ): ", 'yellow'))

        # If the user presses enter without typing anything, interpret it as 'yes'
        if keep.lower() in ('yes', 'y'):
            packets_to_keep.append(packet)
            print(colored("Packet stored", 'blue'))
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\n')

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Write the packets to keep to a new pcap file in the output folder
    output_file = os.path.join(output_folder, os.path.basename(input_file))
    if len(packets_to_keep) > 0:
        wrpcap(output_file, packets_to_keep)
    print(colored(f"Processed {input_file}\n\n\n", 'blue'))


def process_files(directory, file_extension='.pcap', filters=None):
    """
    This function processes all pcap files in the specified directory.
    """
    if filters is None:
        filters = {}
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(file_extension):
                    file_path = os.path.join(root, file_name)
                    sanitize_pcap(file_path, filters=filters)
    except Exception as e:
        print(f"Error processing files: {e}")


# Call the process_files function to start processing pcap files in the 'inputs' directory
process_files('./inputs', filters=FILTERS)
