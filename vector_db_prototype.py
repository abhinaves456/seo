import chromadb
from chromadb.utils import embedding_functions

def main():
    print("Initializing Presidency University Vector DB Prototype...")

    # Initialize ChromaDB in memory (for prototyping)
    # In production, you would use persistent storage or a cloud provider
    chroma_client = chromadb.Client()

    # We use a default lightweight embedding model provided by Chroma
    # (all-MiniLM-L6-v2). For production, you might use OpenAI or Cohere.
    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    # Create a collection (think of this as a table in SQL)
    collection = chroma_client.create_collection(
        name="presidency_policies",
        embedding_function=embedding_function
    )

    # --- 1. DATA INGESTION ---
    # Here we simulate adding documents to your Vector DB.
    # Notice how we attach METADATA to each chunk of text.
    print("\nAdding policy documents to the database...")

    documents = [
        "If a student misses an exam due to a medical emergency, they must submit a medical certificate to the HOD within 48 hours. A makeup exam will be scheduled.",
        "To appeal a grade, students must fill out the Grievance Form on the portal and meet with the Dean of Students within 7 days of result declaration.",
        "Students caught plagiarizing or cheating during examinations will face immediate suspension and a hearing with the Disciplinary Committee.",
        "The library is open from 8 AM to 10 PM. Students must show their ID card to enter. Late fees apply for overdue books.",
        "If an engineering student misses a lab practical, they must contact the lab instructor directly. Makeup labs are only allowed for valid emergencies."
    ]

    metadatas = [
        {"type": "exam_policy", "topic": "medical_leave", "department": "all"},
        {"type": "academic_policy", "topic": "grade_appeal", "department": "all"},
        {"type": "disciplinary_policy", "topic": "cheating", "department": "all"},
        {"type": "facility_rules", "topic": "library", "department": "all"},
        {"type": "exam_policy", "topic": "makeup_lab", "department": "engineering"}
    ]

    ids = ["doc_1", "doc_2", "doc_3", "doc_4", "doc_5"]

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("Documents successfully added!")


    # --- 2. SEMANTIC SEARCH WITHOUT METADATA ---
    # Scenario: A student asks a general question.
    query_1 = "I was sick on the day of my test, what should I do?"

    print(f"\n--- Search 1 (No Metadata Filter) ---")
    print(f"User Query: '{query_1}'")

    results = collection.query(
        query_texts=[query_1],
        n_results=1 # Return top 1 match
    )

    print(f"Found Answer: {results['documents'][0][0]}")


    # --- 3. HYBRID SEARCH (SEMANTIC + METADATA FILTER) ---
    # Scenario: Wasim's intent processor realizes this is an engineering student
    # asking about a missed lab, so he passes you a metadata filter.
    query_2 = "How do I make up a missed session?"

    print(f"\n--- Search 2 (With Metadata Filter from Zain/Wasim) ---")
    print(f"User Query: '{query_2}'")
    print("Filter Applied: {'department': 'engineering'}")

    hybrid_results = collection.query(
        query_texts=[query_2],
        n_results=1,
        where={"department": "engineering"} # This is where the magic happens!
    )

    print(f"Found Answer: {hybrid_results['documents'][0][0]}")

    print("\nPrototype complete. This script demonstrates how your Vector DB will handle unstructured university policies while allowing Zain/Wasim to pass in strict filters!")

if __name__ == "__main__":
    main()
