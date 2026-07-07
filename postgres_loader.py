import psycopg2


def load_products():

    conn = psycopg2.connect(
        host="localhost",
        database="demo_db",
        user="postgres",
        password="postgre",
        port=5432
    )


    cursor = conn.cursor()


    cursor.execute("""
SELECT
    id,
    title,
    content,
    category
FROM documents
""")


    rows = cursor.fetchall()


    documents = []
    metadata = []


    for row in rows:

        id = row[0]
        title = row[1]
        content = row[2]
        category = row[3]


        text = f"""
        id{id}
        Tên tài liệu:
        {title}

        Nội dung:
        {content}
        Phân loại:
        {category}
        """


        documents.append(text)


        metadata.append(
            {
                "source": "postgres",
                "table": "products",
                "id": id
            }
        )


    cursor.close()
    conn.close()


    return documents, metadata