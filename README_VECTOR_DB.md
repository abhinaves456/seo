# Vector Database Prototype Guidelines

Since `chromadb` cannot be installed in this restricted environment, I have provided the `vector_db_prototype.py` script as a reference for you (Abhinav) to run locally on your own machine.

To run it locally, you will need to install ChromaDB:
`pip install chromadb`

The script demonstrates:
1. **Initializing a Vector DB collection** for university policies.
2. **Generating embeddings** for unstructured text (like exam rules, cheating policies, and medical leave procedures).
3. **Attaching Metadata** to those vectors (e.g., `department: engineering`).
4. **Performing Hybrid Search**, showing how you can take logical filters from Zain/Wasim and apply them to your semantic search to get hyper-accurate answers for the students.
