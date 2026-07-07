# pyrefly: ignore [missing-import]
import ollama
import configuration as config

def analyze_query(question: str):
    """Sửa lỗi chính tả và trích xuất từ khóa thuốc bằng LLM."""
    rewrite_prompt = f"""You are a Vietnamese pharmacist. Given a user question about medicine, do TWO things:
1. Fix all Vietnamese spelling mistakes and drug name typos.
2. Extract ONLY the drug name or ingredient name from the question.

Common drug name corrections: banadon/panadon -> panadol, paraxetamin/paracetamon -> paracetamol, a mốc/amốc -> amoxicillin, aspyrin -> aspirin.

Reply in EXACTLY this format (2 lines only, no extra text):
CORRECTED: <corrected full question in Vietnamese>
DRUG: <extracted drug/ingredient name, or NONE if no specific drug mentioned>

User question: {question}"""

    try:
        rewrite_response = ollama.chat(
            model=config.CHAT_MODEL,
            messages=[{"role": "user", "content": rewrite_prompt}],
            options={"temperature": 0.0}
        )
        rewrite_text = rewrite_response["message"]["content"].strip()
        
        corrected_question = question
        drug_keyword = None
        for line in rewrite_text.split("\n"):
            line = line.strip()
            if line.upper().startswith("CORRECTED:"):
                corrected_question = line.split(":", 1)[1].strip().strip('"')
            elif line.upper().startswith("DRUG:"):
                drug_val = line.split(":", 1)[1].strip().strip('"')
                if drug_val.upper() != "NONE" and len(drug_val) >= 2:
                    drug_keyword = drug_val
    except Exception:
        corrected_question = question
        drug_keyword = None
        
    return corrected_question, drug_keyword

def hybrid_search(cursor, corrected_question: str, drug_keyword: str):
    """Thực hiện Hybrid Search (Text Match + Vector) trong DB."""
    search_query = corrected_question
    fuzzy_keyword = drug_keyword if drug_keyword else search_query
        
    question_embedding = ollama.embeddings(
        model=config.EMBEDDING_MODEL,
        prompt=search_query
    )["embedding"]

    cursor.execute(
        """
        WITH text_match AS (
            SELECT
                id, ten_thuoc, hoat_chat_chinh, ham_luong, dang_bao_che, duong_dung, cong_ty_san_xuat, cong_ty_dang_ky,
                0.0 AS distance
            FROM thuoc
            WHERE word_similarity(ten_thuoc, %s) > 0.3
               OR word_similarity(hoat_chat_chinh, %s) > 0.3
            ORDER BY GREATEST(word_similarity(ten_thuoc, %s), word_similarity(hoat_chat_chinh, %s)) DESC
            LIMIT 5
        ),
        vector_match AS (
            SELECT
                id, ten_thuoc, hoat_chat_chinh, ham_luong, dang_bao_che, duong_dung, cong_ty_san_xuat, cong_ty_dang_ky,
                embedding <=> CAST(%s AS vector) AS distance
            FROM thuoc
            WHERE embedding IS NOT NULL
              AND id NOT IN (SELECT id FROM text_match)
            ORDER BY embedding <=> CAST(%s AS vector)
            LIMIT 5
        )
        SELECT * FROM text_match
        UNION ALL
        SELECT * FROM vector_match
        """,
        (fuzzy_keyword, fuzzy_keyword, fuzzy_keyword, fuzzy_keyword, question_embedding, question_embedding)
    )
    
    return cursor.fetchall(), search_query
