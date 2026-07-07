# tạo embedding
# pyrefly: ignore [missing-import]
import ollama
from db import get_connection
from utils import build_document
import configuration as config

BATCH_SIZE = 500

def run():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            while True:
                cursor.execute(
                    "SELECT * FROM thuoc WHERE embedding IS NULL LIMIT %s",
                    (BATCH_SIZE,)
                )
                rows = cursor.fetchall()
                if not rows:
                    print("Hoàn thành.")
                    break

                columns = [desc[0] for desc in cursor.description]

                for row in rows:
                    row_dict = dict(zip(columns, row))
                    for key in row_dict:
                        if row_dict[key] is None:
                            row_dict[key] = ""

                    document = build_document(row_dict)
                    
                    embedding = ollama.embeddings(
                        model=config.EMBEDDING_MODEL,
                        prompt=document
                    )["embedding"]

                    cursor.execute(
                        "UPDATE thuoc SET embedding=CAST(%s AS vector) WHERE id=%s",
                        (embedding, row_dict["id"])
                    )

                    print("Embedded:", row_dict["ten_thuoc"])

                conn.commit()
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()

if __name__ == "__main__":
    run()