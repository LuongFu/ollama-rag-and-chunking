import psycopg2


def load_products():

    conn = psycopg2.connect(
        host="localhost",
        database="drfamilyoi_db",
        user="postgres",
        password="postgre",
        port=5432
    )


    cursor = conn.cursor()

    # LƯU Ý: Vui lòng thay đổi "ten_bang_cua_ban" thành tên bảng thực tế trong Database của bạn
    cursor.execute("SELECT * FROM thuoc")

    # Lấy danh sách các cột tự động
    columns = [desc[0] for desc in cursor.description]
    
    rows = cursor.fetchall()

    documents = []
    metadata = []


    for row in rows:
        # Gom các cột và giá trị thành dictionary
        row_dict = dict(zip(columns, row))
        
        # Xử lý các giá trị None thành chuỗi rỗng để tránh lỗi khi in
        for key in row_dict:
            if row_dict[key] is None:
                row_dict[key] = ""

        id = row_dict.get("id", "")
        
        # Format text cho RAG (LLM sẽ đọc đoạn text này)
        text = f"""
        Tên thuốc: {row_dict.get('ten_thuoc', '')}
        Số đăng ký: {row_dict.get('so_dang_ky', '')}
        Hoạt chất chính: {row_dict.get('hoat_chat_chinh', '')}
        Hàm lượng: {row_dict.get('ham_luong', '')}
        Dạng bào chế: {row_dict.get('dang_bao_che', '')}
        Đường dùng: {row_dict.get('duong_dung', '')}
        Đóng gói: {row_dict.get('dong_goi', '')}
        Tiêu chuẩn: {row_dict.get('tieu_chuan', '')}
        Tuổi thọ: {row_dict.get('tuoi_tho', '')}
        
        Công ty sản xuất: {row_dict.get('cong_ty_san_xuat', '')} (Quốc gia: {row_dict.get('nuoc_san_xuat', '')})
        Địa chỉ sản xuất: {row_dict.get('dia_chi_san_xuat', '')}
        
        Công ty đăng ký: {row_dict.get('cong_ty_dang_ky', '')} (Quốc gia: {row_dict.get('nuoc_dang_ky', '')})
        Địa chỉ đăng ký: {row_dict.get('dia_chi_dang_ky', '')}
        
        Ngày cấp SĐK: {row_dict.get('ngay_cap_so_dang_ky', '')}
        Ngày hết hạn SĐK: {row_dict.get('ngay_het_han_so_dang_ky', '')}
        Ghi chú: {row_dict.get('ghi_chu', '')}
        """

        documents.append(text.strip())

        metadata.append(
            {
                "source": "postgres",
                "table": "products",
                "id": id,
                "ten_thuoc": str(row_dict.get('ten_thuoc', ''))
            }
        )

    cursor.close()
    conn.close()

    return documents, metadata