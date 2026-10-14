import os
os.environ["HF_HOME"] = r"D:\HuggingFace"

import torch
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

if not torch.cuda.is_available():
    raise RuntimeError("CUDA GPU is unavailable. Check your PyTorch installation.")

print("Using GPU:", torch.cuda.get_device_name(0))

llm = HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    device=0,
    model_kwargs={"torch_dtype": torch.float16},
    pipeline_kwargs={
        "max_new_tokens": 512,
        "do_sample": False,
        "repetition_penalty": 1.03,
    },
)

chat_model = ChatHuggingFace(llm=llm)

result = chat_model.invoke("Hello, how are you?")

print("Response:", result.content)