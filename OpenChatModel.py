from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class ModelConfig:
    # Prompt
    system: Optional[str]

    role_prefix: dict
    ai_role: str
    eot_token: str
    bos_token: Optional[str] = None

    # Get template
    def generate_conversation_template(self, tokenize_fn, tokenize_special_fn, message_list):
        tokens = []
        masks = []

        # begin of sentence (bos)
        if self.bos_token:
            t = tokenize_special_fn(self.bos_token)
            tokens.append(t)
            masks.append(False)

        # System
        if self.system:
            t = tokenize_fn(self.system) + [tokenize_special_fn(self.eot_token)]
            tokens.extend(t)
            masks.extend([False] * len(t))

        # Messages
        for idx, message in enumerate(message_list):
            # Prefix
            t = tokenize_fn(self.role_prefix[message["from"]])
            tokens.extend(t)
            masks.extend([False] * len(t))

            # Message
            if "value" in message:
                t = tokenize_fn(message["value"]) + [tokenize_special_fn(self.eot_token)]
                tokens.extend(t)
                masks.extend([message["from"] == self.ai_role] * len(t))
            else:
                assert idx == len(message_list) - 1, "Empty message for completion must be on the last."

        return tokens, masks


MODEL_CONFIG_MAP = {
    # OpenChat / OpenChat-8192
    "openchat": ModelConfig(
        # Prompt
        system=None,

        role_prefix={
            "human": "Human: ",
            "gpt": "Assistant: "
        },
        ai_role="gpt",
        eot_token="<|end_of_turn|>",
        bos_token="<s>",
    ),

    # OpenCoder / OpenCoderPlus
    "opencoder": ModelConfig(
        # Prompt
        system=None,

        role_prefix={
            "human": "User:",
            "gpt": "Assistant:"
        },
        ai_role="gpt",
        eot_token="<|end_of_turn|>",
        bos_token=None,
    )
}
