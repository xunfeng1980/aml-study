from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import PromptTemplate
from langchain.document_loaders import TextLoader
from langchain import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import HuggingFaceEmbeddings
from gpt4all.gpt4all import GPT4All


# add the path to the CV as a PDF
loader = TextLoader('data.txt')
# Embed the document and store into chroma DB
index = VectorstoreIndexCreator(embedding= HuggingFaceEmbeddings()).from_loaders([loader])

# specify the path to the .bin downloaded file
local_path = './models/ggml-gpt4all-j-v1.3-groovy.bin'  # replace with your desired local file path
# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]
# Verbose is required to pass to the callback manager
llm = GPT4All(model=local_path, callbacks=callbacks, verbose=True, backend='gptj')

results = index.vectorstore.similarity_search("what is the solution for soar throat", k=4)
# join all context information (top 4) into one string
context = "\n".join([document.page_content for document in results])
print(f"Retrieving information related to your question...")
print(f"Found this content which is most similar to your question: {context}")