import pyshark

class Stream:
    def __init__(self, protocol):
        self.protocol = protocol
        self.payload = ''

    def __str__(self):
        summary = (
            f"  Protocol: {self.protocol}\n"
            f"  Payload: {self.payload}\n"
        )
        return summary

def decode_payload(packet, protocol):
    try:
        # Check if HTTP payload is present
        if 'http' in packet:
            payload = packet.http.file_data
        # If not, use the TCP or UDP payload
        else:
            payload = getattr(packet, protocol).payload
        return payload
    except AttributeError:
        # If there's no payload, return empty string
        return ''

def summarize_streams(pcap_file):
    cap = pyshark.FileCapture(pcap_file, keep_packets=False)
    streams = {}

    for pkt in cap:
        try:
            if 'TCP' in pkt:
                stream_index = 'TCP_' + pkt.tcp.stream
                protocol = 'tcp'
            elif 'UDP' in pkt:
                stream_index = 'UDP_' + pkt.udp.stream
                protocol = 'udp'
            else:
                continue  # Skip packet if not TCP or UDP

            if stream_index not in streams:
                streams[stream_index] = Stream(protocol)

            stream = streams[stream_index]
            # Append payload to stream
            payload = decode_payload(pkt, protocol)
            if payload:
                stream.payload += payload

        except AttributeError:
            pass  # Skip packet if not TCP or UDP, or missing some info

    cap.close()

    # Return a string summary of each stream
    return streams