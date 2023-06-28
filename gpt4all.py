from transformers import AutoModelForCausalLM, AutoTokenizer


class AiModel():
    def __init__(self, llama_path=None):
        if llama_path is None:
            raise ValueError('Please pass a path to your alpaca model.')

        self.model_path = llama_path
        self.tokenizer_path = llama_path
        self.lora_path = 'nomic-ai/vicuna-lora-multi-turn_epoch_2'
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path,
                                                          device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)
        added_tokens = self.tokenizer.add_special_tokens(
            {"bos_token": "<s>", "eos_token": "</s>", "pad_token": "<pad>"})

        if added_tokens > 0:
            self.model.resize_token_embeddings(len(self.tokenizer))

        print(f"Mem needed: {self.model.get_memory_footprint() / 1024 / 1024 / 1024:.2f} GB")

    def generate(self, prompt, generate_config=None):
        if generate_config is None:
            generate_config = {}

        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.model.device)
        outputs = self.model.generate(input_ids=input_ids,
                                      **generate_config)

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        return decoded[len(prompt):]
