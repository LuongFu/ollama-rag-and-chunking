def build_document(row):
    return f"""
Tên thuốc: {row["ten_thuoc"]}
Hoạt chất chính: {row["hoat_chat_chinh"]}
Hàm lượng: {row["ham_luong"]}
Dạng bào chế: {row["dang_bao_che"]}
Đường dùng: {row["duong_dung"]}
Đóng gói: {row["dong_goi"]}
Tiêu chuẩn: {row["tieu_chuan"]}
Tuổi thọ: {row["tuoi_tho"]}
Công ty sản xuất: {row["cong_ty_san_xuat"]}
Quốc gia sản xuất: {row["nuoc_san_xuat"]}
Công ty đăng ký: {row["cong_ty_dang_ky"]}
Quốc gia đăng ký: {row["nuoc_dang_ky"]}
Địa chỉ sản xuất: {row["dia_chi_san_xuat"]}
Địa chỉ đăng ký: {row["dia_chi_dang_ky"]}
Ghi chú: {row["ghi_chu"]}
"""