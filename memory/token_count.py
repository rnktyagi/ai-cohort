import tiktoken

encoder = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(encoder.encode(text))