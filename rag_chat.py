import chromadb
# pyrefly: ignore [missing-import]
import ollama


client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_collection(
    name="knowledge"
)


question = input(
    "Bạn hỏi: "
)


# ==========================
# tạo embedding cho câu hỏi
# ==========================

question_embedding = ollama.embeddings(
    model="nomic-embed-text",
    prompt=question
)


# ==========================
# tìm chunk gần nhất
# ==========================

result = collection.query(
    query_embeddings=[
        question_embedding["embedding"]
    ],
    n_results=2
)


context = "\n".join(
    result["documents"][0]
)



# ==========================
# gửi cho LLM
# ==========================

prompt = f"""
Dựa vào thông tin:

{context}


Trả lời câu hỏi:

{question}
"""


response = ollama.chat(
    model="vicuna:7b-v1.5-q5_1",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


print(
    response["message"]["content"]
)