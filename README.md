# Medical RAG Search System

Hệ thống tra cứu thông tin Thuốc và Dược phẩm thông minh dựa trên kiến trúc RAG (Retrieval-Augmented Generation) kết hợp Hybrid Search, hoạt động hoàn toàn offline (Local) để đảm bảo bảo mật dữ liệu.

## Kiến trúc Hệ thống

Hệ thống sử dụng các công nghệ cốt lõi:
- **PostgreSQL**: Lưu trữ dữ liệu thuốc, tích hợp extension `pgvector` cho semantic search và `pg_trgm` cho fuzzy search.
- **Ollama**: Nền tảng chạy mô hình AI cục bộ, sử dụng mô hình sinh văn bản (như Qwen2.5 7B, Llama 3) và mô hình nhúng vector (nomic-embed-text).
- **Python**: Quản lý luồng xử lý RAG và tương tác với Database.

## Các tính năng nổi bật

1. **Query Rewriting (Sửa lỗi truy vấn bằng AI)**:
   - Hệ thống không sử dụng trực tiếp câu hỏi người dùng để tra cứu ngay lập tức.
   - LLM sẽ đọc câu hỏi, tự động sửa các lỗi chính tả phổ biến ở tiếng Việt hoặc tên biệt dược (ví dụ: "banadon" -> "panadol"), sau đó trích xuất riêng từ khóa tên thuốc để đảm bảo độ chính xác.

2. **Hybrid Search (Tìm kiếm Lai)**:
   - **Text Match (Fuzzy Search)**: Sử dụng hàm `word_similarity` của PostgreSQL để tìm các thuốc có tên hoặc hoạt chất gần giống với từ khóa, sắp xếp theo độ tương đồng giảm dần.
   - **Vector Match (Semantic Search)**: Sử dụng `pgvector` để tìm các thuốc có ý nghĩa ngữ nghĩa liên quan, bổ sung cho các trường hợp tìm kiếm trừu tượng.

3. **AI Pharmacist (Dược sĩ AI)**:
   - Hệ thống RAG tổng hợp kết quả tìm kiếm và cung cấp ngữ cảnh cho mô hình ngôn ngữ lớn (LLM).
   - Mô hình đọc hiểu thông tin và đóng vai trò như một chuyên gia tư vấn y tế, với bộ nguyên tắc đảm bảo không bịa đặt thông tin (Hallucination) và từ chối cung cấp tư vấn sai lệch.

## Cấu trúc thư mục ứng dụng

- `app/rag_chat.py`: Giao diện chatbot hỏi đáp RAG chính thức.
- `app/search.py`: Giao diện dòng lệnh để test riêng tính năng Hybrid Search.
- `app/search_engine.py`: Module lõi chứa logic xử lý Query Rewriting và truy vấn Database chung cho toàn bộ app.
- `app/migrate_data.py`: Kịch bản di chuyển dữ liệu từ Database cũ sang Database có hỗ trợ Vector mới.
- `app/embed_med.py`: Script dùng Ollama tạo sinh Vector Embedding cho dữ liệu thuốc.
- `app/db.py` & `app/configuration.py`: Cấu hình kết nối Database và thiết lập hệ thống.
- `docker-compose.yml`: Triển khai môi trường PostgreSQL + pgvector nhanh chóng.

## Hướng dẫn cài đặt và chạy thử nghiệm

1. **Khởi động Database**:
   Mở terminal tại thư mục gốc và chạy lệnh:
   ```bash
   docker-compose up -d
   ```

2. **Cài đặt thư viện Python**:
   Cần cài đặt các thư viện sau để kết nối Database và gọi Ollama API:
   ```bash
   pip install psycopg2-binary pgvector ollama
   ```

3. **Khởi chạy nền tảng Ollama**:
   Cài đặt Ollama và tải các mô hình cần thiết:
   ```bash
   ollama pull nomic-embed-text
   ollama pull qwen2.5:7b
   ```

4. **Tạo dữ liệu và Vector Embedding**:
   Nếu Database đang trống, bạn cần chuyển dữ liệu vào và nhúng vector:
   ```bash
   python app/migrate_data.py
   python app/embed_med.py
   ```

5. **Chạy ứng dụng tra cứu**:
   Mở giao diện Chat AI:
   ```bash
   python app/rag_chat.py
   ```
   Hoặc chỉ tìm kiếm kết quả thô:
   ```bash
   python app/search.py
   ```   

   ## Link cào data từ Bộ Y tế https://github.com/LuongFu/DrugDataCrawler ##

## Tuyên bố miễn trừ trách nhiệm y tế
Ứng dụng chỉ có mục đích hỗ trợ tra cứu thông tin từ cơ sở dữ liệu có sẵn. Phản hồi từ AI không thay thế cho chẩn đoán và chỉ định của Bác sĩ hoặc chuyên gia Y tế có chuyên môn.
