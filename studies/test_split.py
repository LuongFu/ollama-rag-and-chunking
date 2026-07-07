from studies.splitter import split_text


with open(
    "data.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()


chunks = split_text(
    text,
    chunk_size=20
)


for i, chunk in enumerate(chunks):
    print("================")
    print("Chunk:", i)
    print(chunk)