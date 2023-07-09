






# process files based on models
# process with lates open


# available models to use
# GPT4All-13B-snoozy.ggmlv3.q4_0
# nous-hermes-13b.ggmlv3.q4_0
# Usage: Call the process_files function with the path to the directory containing the PCAP files

# Non-GPU Library used, default Gpt4all
process_files('./inputs/', ".pcap", 'GPT4All-13B-snoozy.ggmlv3.q4_0', "snoozy")

# process_files('./inputs/', ".pcap", 'orca-mini-13b.ggmlv3.q4_0', process_pcap_file,"orca")

# process_files('./inputs/', ".pcap", 'nous-hermes-13b.ggmlv3.q4_0', process_pcap_file,"nous-hermes")


# custom nomic code technically gpt4all but uses transformers instead
# TheBloke/airoboros-7b-gpt4-fp16 has 4096 context size
process_files('./inputs/', ".pcap", 'TheBloke/airoboros-7b-gpt4-fp16',
              "airoboros", True)

process_files('./inputs/', ".pcap", 'TheBloke/Nous-Hermes-13B-GPTQ',
              "nous-hermes", True, "nous-hermes-13b-GPTQ-4bit-128g.no-act.order")
