from llama_index import GPTSimpleVectorIndex, download_loader

SimpleDirectoryReader = download_loader("SimpleDirectoryReader")

loader = SimpleDirectoryReader('../', recursive=True, exclude_hidden=True)
documents = loader.load_data()
index = GPTSimpleVectorIndex(documents)
res = index.query('这个项目使用的是许可证是?')
print(res)
