import os

from scapy.all import rdpcap, wrpcap


def get_readable_payload(packet):
    if packet.haslayer('Raw'):
        try:
            return packet['Raw'].load.decode('utf-8', errors='replace')
        except AttributeError:
            return str(packet['Raw'].load)
    elif packet.haslayer('Padding'):
        try:
            return packet['Padding'].load.decode('utf-8', errors='replace')
        except AttributeError:
            return str(packet['Padding'].load)
    else:
        return str(packet.payload)


def process_files(directory, file_extension='.pcap'):
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(file_extension):
                    file_path = os.path.join(root, file_name)
                    sanitize_pcap(file_path)
    except Exception as e:
        print(f"Error processing files: {e}")


def sanitize_pcap(input_file, output_folder='sanitised_inputs'):
    # Read packets from the pcap file
    packets = rdpcap(input_file)

    # List to store the packets to keep
    packets_to_keep = []

    for packet in packets:
        # Print a summary of the packet payload
        print(packet.summary() + "\nPayload: " + get_readable_payload(packet))

        # Ask the user whether to keep the packet
        keep = input("Do you want to keep this packet? (yes/no, default is yes): ")

        # If the user presses enter without typing anything, interpret it as 'yes'
        if keep.lower() in ('yes', '', 'y'):
            packets_to_keep.append(packet)
            print("Packet stored")
        print('\n\n')
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Write the packets to keep to a new pcap file in the output folder
    output_file = os.path.join(output_folder, os.path.basename(input_file))
    wrpcap(output_file, packets_to_keep)
    print(f"processed {input_file}\n\n\n")

def summarize_pcap(input_file):
    # Read packets from the pcap file
    packets = rdpcap(input_file)

    # Return a list of string summaries for each packet
    return [packet.summary() for packet in packets]


process_files('./inputs')
