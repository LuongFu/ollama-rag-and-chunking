# pyrefly: ignore [missing-import]
from ollama import chat
from loader import load_text_file
import chromadb

client = chromadb.Client()
text = load_text_file("data.txt")

collection = client.create_collection(
    name="knowledge"
)


collection.add(
    documents=[
        text
    ],
    ids=[
        "doc1"
    ]
)


question = input("Bạn hỏi: ")


result = collection.query(
    query_texts=[question],
    n_results=1
)


context = result["documents"][0][0]


prompt = f"""
Dựa vào thông tin sau:

{context}


Trả lời câu hỏi:

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


print(response.message.content)