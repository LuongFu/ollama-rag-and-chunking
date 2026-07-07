# chatbot
from db import get_connection
# pyrefly: ignore [missing-import]
import ollama
import configuration as config

def run():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            question = input("Bạn hỏi: ")
            if not question.strip():
                return
            from search_engine import analyze_query, hybrid_search
            
            # === BƯỚC 1: Query Rewriting - Sửa lỗi chính tả + Trích xuất tên thuốc ===
            print("\n[AI] Đang phân tích câu hỏi...")
            corrected_question, drug_keyword = analyze_query(question)

            if corrected_question.lower() != question.lower():
                print(f" Đang hiển thị kết quả cho: {corrected_question}")
                print(f"   (Tìm kiếm thay thế cho: {question})")
            if drug_keyword:
                print(f" Từ khóa thuốc: {drug_keyword}\n")
            else:
                print()

            # === BƯỚC 2: HYBRID SEARCH (Fuzzy + Vector) ===
            rows, search_query = hybrid_search(cursor, corrected_question, drug_keyword)
            
            if not rows:
                print("\n=== LỖI ===")
                print("Không tìm thấy dữ liệu thuốc nào trong Cơ sở dữ liệu (Hoặc DB chưa được tạo vector).")
                print("Vui lòng chạy file `python app/embed_med.py` trước để tạo dữ liệu.")
                return

            contexts = []

            for i, row in enumerate(rows):
                # Clean up None values
                r = [str(x) if x is not None else "" for x in row]
                
                print("================")
                print("ID:", r[0])
                print("Tên thuốc:", r[1])
                print("Distance:", row[8], "(0.0 = Khớp tên chính xác)" if row[8] == 0.0 else "")

                context = f"""Thuốc {r[1]} (Hoạt chất: {r[2]}, Hàm lượng: {r[3]}, Dạng bào chế: {r[4]}, Đường dùng: {r[5]})
- Công ty sản xuất: {r[6]}
- Công ty đăng ký: {r[7]}"""
                contexts.append(context)

            context_str = "\n\n".join(contexts)

            prompt = f"""Bạn là Dược sĩ AI. Dưới đây là danh sách các thuốc hệ thống đã trích xuất từ Cơ sở dữ liệu.
LƯU Ý QUAN TRỌNG: 
- Người dùng thường xuyên gõ sai chính tả (ví dụ: "paraxetamin" = "paracetamol", "panadon" = "panadol").
- Hãy khéo léo tự hiểu ý định của người dùng và đối chiếu với danh sách DỮ LIỆU THUỐC. Nếu trong Dữ liệu có thuốc/hoạt chất tương tự hoặc cùng loại, hãy liệt kê ra để tư vấn.
- TUYỆT ĐỐI KHÔNG BỊA RA THÔNG TIN BÊN NGOÀI DỮ LIỆU.

DỮ LIỆU THUỐC:
{context_str}

CÂU HỎI CỦA NGƯỜI DÙNG: {search_query}
TRẢ LỜI CỦA DƯỢC SĨ AI:"""

            response = ollama.chat(
                model=config.CHAT_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={"temperature": 0.1}
            )

            print("\n=== TRẢ LỜI ===")
            print(response["message"]["content"])
            print("\n--------------------------------------------------")
            print("LƯU Ý: Tôi chỉ là Trợ lý AI hỗ trợ tra cứu thông tin.")
            print("Các thông tin này KHÔNG thay thế cho chỉ định của Bác sĩ.")
            print("Vui lòng tham vấn dược sĩ của hệ thống một cách cẩn thận trước khi sử dụng thuốc.")
            print("--------------------------------------------------\n")
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()

if __name__ == "__main__":
    run()