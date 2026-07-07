# pyrefly: ignore [missing-import]
from ollama import Client

client = Client(host="http://127.0.0.1:11434")

response = client.chat(
    model="vicuna:7b-v1.5-q5_1",
    messages=[
        {
            "role": "user",
            "content": "AI chạy trên máy tính, đọc trong data.txt ghi nguyên văn không bổ sung thêm"
        }
    ]
)

print(response["message"]["content"])