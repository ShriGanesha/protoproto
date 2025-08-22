import tiktoken

with open("../documents/tom.txt", "r") as f:
    text = f.read()

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

tokens = encoding.encode(text)
print(f"Token count: {len(tokens)}")