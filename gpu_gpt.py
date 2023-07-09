from auto_gptq import AutoGPTQForCausalLM
from transformers import AutoTokenizer, AutoModelForCausalLM


class ai_model():
    def __init__(self, llama_path=None, model_base_name=None):
        if llama_path is None:
            raise ValueError('Please pass a path to your alpaca model.')

        self.model_path = llama_path
        self.tokenizer_path = llama_path
        self.lora_path = 'nomic-ai/vicuna-lora-multi-turn_epoch_2'

        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)

        if '' == model_base_name or None == model_base_name:
            self.model = AutoModelForCausalLM.from_pretrained(llama_path, trust_remote_code=True)
        else:
            self.model = AutoGPTQForCausalLM.from_quantized(llama_path,
                                                            use_safetensors=True,
                                                            trust_remote_code=True,
                                                            device="cuda:0",
                                                            use_triton=False,
                                                            model_basename=model_base_name,
                                                            quantize_config=None)

        added_tokens = self.tokenizer.add_special_tokens(
            {"bos_token": "<s>", "eos_token": "</s>", "pad_token": "<pad>"})

        if added_tokens > 0:
            self.model.resize_token_embeddings(len(self.tokenizer))

        print(f"Mem needed: {self.model.get_memory_footprint() / 1024 / 1024 / 1024:.2f} GB")

    def generate(self, prompt):
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.model.device)
        outputs = self.model.generate(inputs=input_ids, temperature=0.7)

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        return decoded[len(prompt):]


def new_ai_model(path, base):
    return ai_model(path, base)
