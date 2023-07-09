def generate_first_prompt(packet_count):
    """
    Generates the initial prompt for analyzing packets.

    Args:
        packet_count (int): The number of packets to analyze.

    Returns:
        str: The generated prompt.
    """
    return """
        You are an advanced AI that detects malicious requests by parsing the various payloads of the protocols.
        Please analyze the {0} packets provided in the follow-up prompts 
        and determine if each packet is malicious or not. 
        Packet Payload if bigger, will be split into chunks and sent for analysis.
        Consider examining the payload, headers, and protocols in a step-by-step analysis.
        Your response should be a concise categorization of either "Malicious" or "Not Malicious". 
        Do not provide any additional information or context beyond this categorization. 
        Note that an empty payload is not considered malicious.
        As an AI model specialized in detecting malicious activity or network attacks, 
        you should carefully examine the payload and follow a step-by-step analysis.
        Avoid providing additional information or context beyond this categorization.
        If even One of the packet is malicious , mark the whole pcap file as malicious.
        The prompt for each packet will be provided after this instruction.
    """.format(packet_count)


def generate_prompt(protocol, payload):
    """
    Generates a prompt for analyzing a packet with the given protocol and payload.

    Args:
        protocol (str): The protocol of the packet.
        payload (str): The payload of the packet.

    Returns:
        str: The generated prompt.
    """
    return """
    Your task is to determine whether the protocol and payload are malicious requests or not. 
    Follow the instructions provided in the beginning.
    Your response should be a concise categorization either: `Malicious` or `Not Malicious`.
    Protocol: {0}
    Payload: {1}
    """.format(protocol, payload)


def generate_part_prompt(protocol, payload, count, total):
    """
    Generates a prompt for analyzing a part of a packet's payload.

    Args:
        protocol (str): The protocol of the packet.
        payload (str): The payload of the packet part.
        count (int): The part count of the payload.
        total (int): The total number of parts.

    Returns:
        str: The generated prompt.
    """
    return """
    Your task is to determine whether the protocol and payload are malicious requests or not.
    Follow the instructions provided in the beginning.
    As the payload is large, we will split the payload into {3} parts.
    Here is part {2} of the payload:
    Protocol: {0}
    Payload: {1}
    """.format(protocol, payload, count, total)


def generate_part_prompt_final():
    """
    Generates the final prompt for analyzing the parts of a packet's payload.
    This needs to be called once all the parts have been sent , to conclude the request
    Returns:
        str: The generated prompt.
    """
    return """
    Your task is to determine whether the protocol and payload are malicious requests or not.
    Follow the instructions provided in the beginning.
    All the parts of the payload in the packet are provided, please analyze them as a whole
    and categorize whether they are malicious or not.
    """
