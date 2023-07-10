from transformers import pipeline

from pcap_operations import process_files

deep_night_research_classifier = pipeline("zero-shot-classification", model="deepnight-research/zsc-text")
facebook_bart_large_mnli_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
Deberta_mnli_anli_classifier = pipeline("zero-shot-classification",
                                        model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli")
deberta_tasksource_nli_classifier = pipeline("zero-shot-classification", model="sileod/deberta-v3-base-tasksource-nli")

process_files('./inputs', deep_night_research_classifier)
process_files('./inputs', facebook_bart_large_mnli_classifier)
process_files('./inputs', Deberta_mnli_anli_classifier)
process_files('./inputs', deberta_tasksource_nli_classifier)
