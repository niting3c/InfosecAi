import os
import zipfile
import json
import pyshark
def process_pcap_files(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            if file_name.endswith(".pcap"):
                process_pcap_file(file_path)
            elif file_name.endswith(".zip"):
                process_zip_file(file_path, file_name)


def process_pcap_file(file_path, filename):
    PacketInput = []
    attackType = filename.split("=")[0]
    content = ""
    packets = pyshark.FileCapture(file_path)
    for packet in packets:
        field_names = packet.tcp._all_fields
        field_values = packet.tcp._all_fields.values()
        for field_name in field_names:
            for field_value in field_values:
                content += str.lower(field_name) + "=" + str.lower(field_value)
    packets.close()
    PacketInput.append({'prompt': content, 'completion': attackType})
    with open('./output/'+filename+'.json', 'w') as json_file:
        json.dump(PacketInput, json_file)


def process_zip_file(file_path, filename):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith(".pcap"):
                extracted_path = zip_ref.extract(file_name)
                process_pcap_file(extracted_path, filename)
                os.remove(extracted_path)


# Usage: Call the process_pcap_files function with the path to the directory containing the PCAP files
process_pcap_files('./inputs/')

