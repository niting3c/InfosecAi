import json
import os

import pyshark
from termcolor import colored

def sanitize_pcap(input_file, output_folder='sanitised_inputs'):
    print(colored(f"Processing {input_file}...", 'yellow'))

    # Creating an instance of FileCapture to parse the pcap file
    pcap = pyshark.FileCapture(input_file)

    # Defining the dictionary to store the packet payloads
    streams_dict = {}

    # Looping over each packet in the pcap file
    for packet in pcap:
        try:
            # Filter http stream and exclude other protocols
            if 'http' in packet:
                stream_number = int(packet.http.stream)  # Get the stream number
                seq_number = int(packet.tcp.seq)  # Get the sequence number

                # Ensure the stream number is already a key in the dictionary
                if stream_number not in streams_dict:
                    streams_dict[stream_number] = []

                # Extract packet payload and convert to ASCII
                payload = ''.join(chr(int(byte, 16)) for byte in packet.data.data.split(':'))

                # Store the sequence number and payload as a tuple in the list for this stream number
                streams_dict[stream_number].append((seq_number, payload))

        except AttributeError:
            # Ignore packets that aren't TCP or don't have payload data
            continue

    # Now sort the payloads in each stream based on their sequence numbers
    for stream_number, payloads in streams_dict.items():
        streams_dict[stream_number] = [payload for _, payload in sorted(payloads)]

    # Create output file name from input file name
    output_file_name = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + '.json')

    # Write the output dictionary to a JSON file
    with open(output_file_name, 'w') as f:
        json.dump(streams_dict, f, ensure_ascii=False, indent=4)

    print(colored(f"Done processing {input_file}. Output saved to {output_file_name}", 'green'))
    return streams_dict


def process_files(directory, file_extension='.pcap'):
    """
    This function processes all pcap files in the specified directory.
    """
    try:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith(file_extension):
                    file_path = os.path.join(root, file_name)
                    sanitize_pcap(file_path)
    except Exception as e:
        print(colored(f"Error processing files: {e}", 'red'))


# Call the process_files function to start processing pcap files in the 'inputs' directory
process_files('./inputs')
