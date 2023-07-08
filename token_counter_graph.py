import os

import matplotlib.pyplot as plt
import pyshark
from transformers import AutoTokenizer


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
    packets = pyshark.FileCapture(filename, keep_packets=False)
    max = 0
    for packet in packets:
        try:
            # Check if the packet has a payload
            if 'data' in packet:
                payload = packet.data.data
                # Tokenize the payload
                tokens = tokenizer.encode(payload)
                # Add token count and filename to respective lists
                if max < len(tokens):
                    max = len(tokens)
                count_obj[filename] = max
        except AttributeError:
            pass
        except Exception as e:
            print(f"Error processing packet: {e}")
    # Close the capture file handle
    packets.close()


# Initialize OpenAI tokenizer
tokenizer = AutoTokenizer.from_pretrained("openchat/openchat_v2_w")
counter = {}
process_files("inputs/", tokenizer, counter)

# Extract the filenames and token counts from the counter dictionary
filenames = list(counter.keys())
token_counts = list(counter.values())

# Generate the token count graph
plt.figure(figsize=(10, 6))
plt.plot(filenames, token_counts, marker='o')
plt.xlabel('Filename')
plt.ylabel('Token Count')
plt.title('Number of max Tokens in Each File')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
