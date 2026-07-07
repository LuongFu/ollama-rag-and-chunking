from embedding import create_embedding


vector = create_embedding(
    "Python là ngôn ngữ lập trình"
)


print(len(vector))
print(vector[:5])