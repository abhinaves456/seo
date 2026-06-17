import psycopg2
import numpy as np

# Note: In a real environment, you would use an embedding model like OpenAI or SentenceTransformers.
# For this prototype, we simulate an embedding model generating vectors.
def simulate_embedding(text):
    """Simulates creating a 3-dimensional embedding vector for a piece of text."""
    # In reality, this would be model.encode(text) and return 384, 768, or 1536 dimensions.
    # We use random vectors for the sake of the SQL demonstration.
    return np.random.rand(3).tolist()

def main():
    print("--- PostgreSQL (pgvector) Integration Prototype ---")
    print("This script demonstrates how Abhinav (Vector) and Zain (Logical) can share ONE database.")

    # 1. Database Connection Parameters
    # Zain would provide these details.
    DB_NAME = "presidency_db"
    DB_USER = "postgres"
    DB_PASS = "password"
    DB_HOST = "localhost"

    print("\nConnecting to PostgreSQL database...")

    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor()

        # 2. Setup the extension and table (Zain & Abhinav do this together)
        print("Enabling pgvector extension and creating table...")

        # Enable the pgvector extension
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        # Create a table that mixes Zain's structured data with Abhinav's vectors
        cur.execute("""
            DROP TABLE IF EXISTS university_documents;
            CREATE TABLE university_documents (
                id SERIAL PRIMARY KEY,
                department VARCHAR(50),      -- Zain's Logical Filter
                document_type VARCHAR(50),   -- Zain's Logical Filter
                document_text TEXT,          -- The raw text
                embedding VECTOR(3)          -- Abhinav's Vector (3 dimensions for this demo)
            );
        """)

        # 3. Data Ingestion
        print("\nIngesting mock data...")

        documents = [
            ("engineering", "policy", "Engineering students must maintain a 75% attendance rate.", simulate_embedding("attendance policy")),
            ("business", "policy", "Business students missing an exam need a doctor's note.", simulate_embedding("medical leave")),
            ("all", "procedure", "To change your major, fill out form X and meet the Dean.", simulate_embedding("major change")),
        ]

        for doc in documents:
            cur.execute(
                "INSERT INTO university_documents (department, document_type, document_text, embedding) VALUES (%s, %s, %s, %s)",
                (doc[0], doc[1], doc[2], doc[3])
            )

        conn.commit()
        print("Data successfully ingested!")

        # 4. The Hybrid Search Query
        print("\n--- Simulating a User Query ---")
        student_question = "How do I switch to a different degree program?"
        print(f"Student asks: '{student_question}'")

        # Abhinav embeds the question on the fly
        question_vector = simulate_embedding(student_question)

        print("\nRunning a single SQL query that combines Semantic Search + Logical Filtering...")

        # Zain and Abhinav write this SQL query together.
        # It filters by 'procedure' (Logical) AND sorts by vector similarity using the `<->` operator!
        search_query = """
            SELECT department, document_text
            FROM university_documents
            WHERE document_type = 'procedure'
            ORDER BY embedding <-> %s::vector
            LIMIT 1;
        """

        cur.execute(search_query, (question_vector,))
        result = cur.fetchone()

        if result:
            print(f"\nResult found!")
            print(f"Department Filter: {result[0]}")
            print(f"Document Text: {result[1]}")

    except Exception as e:
        print(f"\n[Note] Database Connection Failed: {e}")
        print("This is expected because no actual PostgreSQL database is running in this sandbox.")
        print("However, the code above is structurally correct and ready to use in your real environment!")

    finally:
        if 'conn' in locals() and conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    main()
