# Training AI for Information Security: MSC Dissertation Project

This repository contains the implementation of my MSC Dissertation project on "Training AI for Information Security". The project uses machine learning algorithms for detecting and classifying cyber threats in network traffic, specifically utilizing transformer-based models for zero-shot classification tasks.

## Table of Contents

- [Installation](#installation)
- [Detailed File Descriptions](#detailed-file-descriptions)
- [Usage](#usage)
- [Models](#models)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the project, follow these steps:

1. Clone the repository:
    ```
    git clone https://github.com/niting3c/InfosecAi.git
    ```

2. Change directory to the cloned repository:
    ```
    cd InfosecAi
    ```

3. Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```
**Note**: This project has been tested on Python 3.11 and the required dependencies are listed in the `requirements.txt` file.

## Detailed File Descriptions

Here are brief descriptions of the main files in this repository:

1. `run.py`: This is the main script that initializes multiple zero-shot classification models from the Transformers library, processes input files with each model, and writes the results.

2. `utils.py`: This script contains helper functions to handle file-related operations such as creating file paths.

    - `create_result_file_path`: This function creates a result file path for the output files based on the original file path and the specified extension and directory.

3. `promptmaker.py`: This script includes functions that generate prompts for the classification tasks. These prompts help guide the AI in its analysis of packets and instruct it on how to report its findings.

    - `generate_first_prompt`: Generates the initial prompt for analyzing packets.
    - `generate_prompt`: Generates a prompt for analyzing a packet with the given protocol and payload.
    - `generate_part_prompt`: Generates a prompt for analyzing a part of a packet's payload.
    - `generate_part_prompt_final`: Generates the final prompt for analyzing the parts of a packet's payload. 

4. `pcap_operations.py`: This script contains functions that handle pcap file operations, including reading packets from pcap files, analyzing packets using the zero-shot classification models, and writing the results to an output file.

    - `process_files`: Processes all pcap files in the specified directory.
    - `analyse_packet`: Analyzes a pcap file and extracts packet information for further processing.

5. `llm_model.py`: This script includes functions that handle the interaction with the transformer models. It prepares the inputs for the classifier, generates the classifier's response, and processes the response.

    - `create_pipeline_model`: Creates a pipeline model using the specified model name.
    - `pipe_response_generate`: Generates a response from the classifier for the given input string.
    - `process_string_input`: Processes an input string with the classifier and writes the result to an output file.
    - `send_to_model`: Processes the given payload and sends it to the classifier in batches.

## Usage

1. Make sure you have installed all necessary packages (see [Installation](#installation)).

2. The `run.py` script expects input files to be located in the `./inputs` directory. Make sure you have populated this directory with your pcap files for processing.

3. To start the program, simply run:
    ```
    python run.py
    ```
4. The results will be written to the `./output` directory.

## Models

The project uses the following transformer models for zero-shot classification tasks:

1. [Deep Night Research's ZSC Text](https://huggingface.co/deepnight-research/zsc-text)
2. [Facebook's BART Large MNLI](https://huggingface.co/facebook/bart-large-mnli)
3. [Moritz Laurer's DeBERTa v3 base MNLI+FEVER+ANLI](https://huggingface.co/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli)
4. [Sileod's DeBERTa v3 base tasksource NLI](https://huggingface.co/sileod/deberta-v3-base-tasksource-nli)

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Please follow these steps if you wish to contribute:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Nitin Gupta - nitin.gupta.22@ucl.ac.uk

Project Link: [https://github.com/niting3c/InfosecAi](https://github.com/niting3c/InfosecAi)
  
For specific requests or inquiries, feel free to contact me. Happy coding!