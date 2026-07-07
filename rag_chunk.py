# pyrefly: ignore [missing-import]
from ollama import chat
import chromadb

from splitter import split_text


# đọc file

with open(
    "data.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()



# chia chunk

chunks = split_text(
    text,
    chunk_size=20
)



# tạo database

client = chromadb.Client()


collection = client.create_collection(
    name="knowledge"
)



# lưu chunks

ids = []

for i in range(len(chunks)):
    ids.append(
        f"chunk_{i}"
    )


collection.add(
    documents=chunks,
    ids=ids
)



# hỏi

question = input(
    "Bạn hỏi: "
)



# tìm kiếm

result = collection.query(
    query_texts=[
        question
    ],
    n_results=2
)



contexts = result["documents"][0]


context = "\n".join(contexts)



prompt = f"""
Bạn hãy trả lời dựa trên thông tin sau:

{context}


Câu hỏi:

{question}
"""


response = chat(
    model="vicuna:7b-v1.5-q5_1",
    messages=[
        {
            "role":"user",
            "content":prompt
        }
    ]
)


print(
    response.message.content
)