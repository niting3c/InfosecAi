# AI Packet Classifier

This project uses HuggingFace's Transformers library to classify packets in pcap files as potentially malicious or benign. This is accomplished using Zero-Shot Classification models.

## Table of Contents

1. [Models Used](#models-used)
2. [Python Scripts](#python-scripts)
3. [Prerequisites](#prerequisites)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [Credits](#credits)
7. [Contact](#contact)

## Models Used

The following models are utilized in the project for packet classification:

1. [deepnight-research/zsc-text](https://huggingface.co/deepnight-research/zsc-text)
2. [facebook/bart-large-mnli](https://huggingface.co/facebook/bart-large-mnli)
3. [MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli](https://huggingface.co/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli)
4. [sileod/deberta-v3-base-tasksource-nli](https://huggingface.co/sileod/deberta-v3-base-tasksource-nli)

These models are powerful tools for Zero-Shot Classification tasks.

## Python Scripts

The project contains the following Python scripts:

1. `run.py` : This is the entry point of the program. It initializes the models and sets the directory for processing the pcap files.

2. `pcap_operations.py` : It processes all the pcap files in the specified directory and extracts packet information for further processing.

3. `llm_model.py` : This script is used for creating a pipeline model and sending inputs to the model for classification. It includes handling and processing of inputs and creating prompts for the models.

4. `PromptMaker.py` : This file is responsible for generating specific prompts based on the protocol and payload of the packet which is then sent to the model for classification.

5. `utils.py` : This contains utility functions used in the project such as creating the result file paths and getting the full file path.

## Prerequisites

The project is developed and tested with Python 3.11. Please make sure to install the necessary Python packages listed in `requirements.txt`.

## Usage

1. Clone this repository and navigate to the repository's directory.
2. Run `run.py` to start the processing of pcap files. This will generate output files with the analysis in the output directory.

```bash
python3 run.py
```

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check issues page if you want to contribute.

## Credits

This project utilizes the Transformers library by Hugging Face and the Scapy library for pcap file processing. 

Documentation and code improvements were made with the help of OpenAI's ChatGPT.

## Contact

For any queries, you can reach out to me at nitin.gupta.22@ucl.ac.uk.

---

Remember to change the necessary parts if you have made changes to the project that are not reflected here.