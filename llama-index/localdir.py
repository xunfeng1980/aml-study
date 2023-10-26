from llama_index.prompts.prompts import SimpleInputPrompt
import logging
import sys
import torch

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llm_predictor import HuggingFaceLLMPredictor

documents = SimpleDirectoryReader('./').load_data()


# This will wrap the default prompts that are internal to llama-index
# taken from https://huggingface.co/Writer/camel-5b-hf
query_wrapper_prompt = SimpleInputPrompt(
    "Below is an instruction that describes a task. "
    "Write a response that appropriately completes the request.\n\n"
    "### Instruction:\n{query_str}\n\n### Response:"
)

hf_predictor = HuggingFaceLLMPredictor(
    max_input_size=2048,
    max_new_tokens=256,
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name="Writer/camel-5b-hf",
    model_name="Writer/camel-5b-hf",
    device_map="auto",
    tokenizer_kwargs={"max_length": 2048},
    # uncomment this if using CUDA to reduce memory usage
    model_kwargs={"torch_dtype": torch.float16}
)
service_context = ServiceContext.from_defaults(chunk_size=512, llm_predictor=hf_predictor)
index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
query_engine = index.as_query_engine()
response = query_engine.query("What did the code doing?")
response = query_engine.query("What  the model_name?")
response = query_engine.query("What max_length?")
response = query_engine.query("What is the tokenizer_name?")
print(response)