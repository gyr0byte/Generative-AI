import os
os.environ["HF_HOME"] = r"D:\HuggingFace"

from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=128,
        do_sample=False,
        repetition_penalty=1.1,
        return_full_text=False,
        eos_token_id=2,
        pad_token_id=2,
    ),
)

chat_model = ChatHuggingFace(llm=llm)

response = chat_model.invoke("Hello, how are you?")
print(response.content)