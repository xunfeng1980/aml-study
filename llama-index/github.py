import pickle
import os

assert (
        os.getenv("OPENAI_API_KEY") is not None
), "Please set the OPENAI_API_KEY environment variable."

from llama_index import download_loader, GPTSimpleVectorIndex

download_loader("GithubRepositoryReader")

from llama_index.readers.github_readers.github_api_client import GithubClient
from llama_index.readers.github_readers.github_repository_reader import GithubRepositoryReader

docs = None

docs = None
if os.path.exists("docs.pkl"):
    with open("docs.pkl", "rb") as f:
        docs = pickle.load(f)

if docs is None:
    github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
    loader = GithubRepositoryReader(
        # github_client,
        owner="xunfeng1980",
        repo="rust-study",
        # filter_directories=(["gpt_index", "docs"], GithubRepositoryReader.FilterType.INCLUDE),
        # filter_file_extensions=([".py"], GithubRepositoryReader.FilterType.INCLUDE),
        verbose=True,
        concurrent_requests=10,
    )

    docs = loader.load_data(branch="main")

    with open("docs.pkl", "wb") as f:
        pickle.dump(docs, f)

index = GPTSimpleVectorIndex(docs)

res = index.query("优化代码依赖?")
print(res)
