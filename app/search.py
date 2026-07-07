# semantic search
# pyrefly: ignore [missing-import]
import ollama
from db import get_connection
import configuration as config

def run():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            question = input("Bạn hỏi: ")
            if not question.strip():
                return
                
            from search_engine import analyze_query, hybrid_search
            
            print("\n[AI] Đang phân tích câu hỏi...")
            corrected_question, drug_keyword = analyze_query(question)

            if corrected_question.lower() != question.lower():
                print(f" Đang hiển thị kết quả cho: {corrected_question}")
                print(f"   (Tìm kiếm thay thế cho: {question})")
            if drug_keyword:
                print(f" Từ khóa thuốc: {drug_keyword}\n")
            else:
                print()

            rows, search_query = hybrid_search(cursor, corrected_question, drug_keyword)

            for row in rows:
                print(row)
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()

if __name__ == "__main__":
    run()