def generate_first_prompt(packet_count):
    """
    Generate the initial prompt for the AI model.
    """
    return """
        You are an advanced AI that detects malicious requests by parsing the various payloads of the protocols.
        Please analyze the {0} packets provided in the follow-up prompts 
        and determine if each packet is malicious or not. 
        Consider examining the payload, headers, and protocols in a step-by-step analysis.
        Your response should be a concise categorization of either "Malicious" or "Not Malicious". 
        Do not provide any additional information or context beyond this categorization. 
        Note that an empty payload is not considered malicious.
        As an AI model specialized in detecting malicious activity or network attacks, 
        you should carefully examine the payload and follow a step-by-step analysis.
        Avoid providing additional information or context beyond this categorization.
        The prompt for each packet will be provided after this instruction.
    """.format(packet_count)


def generate_prompt(protocol, payload):
    """
    Generate a prompt for each packet based on protocol and payload.
    """
    return """
    Your Task is to determine whether the Protocol and payload is a malicious
    request or not? Follow the instructions provided in the beginning.
    Your response should be a concise categorization either: `Malicious` or `Not Malicious`.
    protocol:{0}
    payload:{1}
    """.format(protocol, payload)


