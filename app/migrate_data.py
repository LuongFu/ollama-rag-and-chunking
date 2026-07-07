import psycopg2
from psycopg2.extras import execute_batch

def migrate_data():
    print("Đang kết nối tới 2 Database...")
    
    # Kết nối DB cũ chứa dữ liệu thật (port 5432)
    conn_old = psycopg2.connect(
        host="localhost", database="drfamilyoi_db", user="postgres", password="postgre", port=5432
    )
    
    # Kết nối DB mới của Docker (port 5433)
    conn_new = psycopg2.connect(
        host="localhost", database="drfamilyoi_db", user="postgres", password="postgre", port=5433
    )
    
    cursor_old = conn_old.cursor()
    cursor_new = conn_new.cursor()
    
    # 1. Lấy tất cả tên cột từ bảng thuoc (bỏ qua cột embedding vì nó chưa có data)
    cursor_old.execute("SELECT * FROM thuoc LIMIT 0")
    columns = [desc[0] for desc in cursor_old.description if desc[0] != 'embedding']
    col_names = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    
    print(f"Bắt đầu Copy 50.000+ bản ghi... Vui lòng đợi khoảng 10-20 giây.")
    
    # 2. Đọc dữ liệu từ DB cũ theo lô (batch) để không tràn RAM
    cursor_old.execute(f"SELECT {col_names} FROM thuoc")
    
    while True:
        rows = cursor_old.fetchmany(5000)
        if not rows:
            break
            
        # 3. Ghi dữ liệu vào DB mới
        try:
            insert_query = f"INSERT INTO thuoc ({col_names}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
            execute_batch(cursor_new, insert_query, rows)
            conn_new.commit()
            print(f"Đã copy thành công thêm {len(rows)} dòng...")
        except Exception as e:
            print("Lỗi:", e)
            conn_new.rollback()
            break
        
    cursor_old.close()
    conn_old.close()
    cursor_new.close()
    conn_new.close()
    
    print(" MỌI THỨ ĐÃ HOÀN TẤT! Dữ liệu đã sang nhà mới.")

if __name__ == "__main__":
    migrate_data()
