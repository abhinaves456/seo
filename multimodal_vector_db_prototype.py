import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import os

def main():
    print("Initializing Presidency University MULTIMODAL Vector DB Prototype...")
    print("This database can search across both Images and Text simultaneously!\n")

    # 1. Setup Multimodal Embeddings
    # We use OpenCLIP, which can map both text and images into the same vector space.
    # Note: Running this locally requires 'open-clip-torch' and 'torch' installed.
    embedding_function = OpenCLIPEmbeddingFunction()

    # ImageLoader allows ChromaDB to load images directly from file paths
    image_loader = ImageLoader()

    # Initialize ChromaDB client
    chroma_client = chromadb.Client()

    # Create a Multimodal Collection
    # Notice we pass the embedding_function and data_loader for images
    collection = chroma_client.create_collection(
        name="presidency_multimedia",
        embedding_function=embedding_function,
        data_loader=image_loader
    )

    # --- 1. DATA INGESTION (Text & Images combined) ---
    print("Ingesting Multimedia Data (Simulated)...")

    # We will simulate having some images by generating small blank JPEGs using PIL.
    # In reality, these would be paths to actual images of campus, timetables, or notices.
    from PIL import Image
    os.makedirs("mock_images", exist_ok=True)
    Image.new('RGB', (100, 100), color = 'red').save('mock_images/library.jpg')
    Image.new('RGB', (100, 100), color = 'blue').save('mock_images/timetable_cs.jpg')

    # We insert both raw text documents AND image file paths
    documents = [
        "The central library is open from 8 AM to 10 PM.",
        "Computer Science Midterm Timetable for Fall Semester.",
    ]

    image_uris = [
        "mock_images/library.jpg",
        "mock_images/timetable_cs.jpg"
    ]

    # Metadata from Zain (Logical DB constraints)
    metadatas = [
        {"type": "facility_photo", "department": "all", "zain_sql_id": "fac_001"},
        {"type": "exam_timetable_image", "department": "computer_science", "zain_sql_id": "exam_104"}
    ]

    ids = ["media_1", "media_2"]

    # Add to ChromaDB. Notice we can add `uris` for images alongside text.
    collection.add(
        ids=ids,
        documents=documents,
        uris=image_uris,
        metadatas=metadatas
    )
    print("Successfully added images and text to the Multimodal DB!\n")


    # --- 2. SEARCH: TEXT-TO-IMAGE ---
    # Scenario: Student types text, wants to find a corresponding image/document.
    student_query = "Show me the schedule for CS exams."

    print(f"--- Search 1: Text-to-Image ---")
    print(f"Student asked (Text): '{student_query}'")

    text_results = collection.query(
        query_texts=[student_query],
        n_results=1,
        include=['uris', 'metadatas', 'documents']
    )

    print(f"Returned Image URI: {text_results['uris'][0][0]}")
    print(f"Matched Metadata (for Zain to use): {text_results['metadatas'][0][0]}\n")


    # --- 3. HYBRID SEARCH: IMAGE-TO-TEXT (WITH ZAIN'S FILTERS) ---
    # Scenario: Student uploads an image (e.g. they took a photo of an old timetable)
    # and Wasim passes it to you. You use the image to search, BUT you apply Zain's logical filter.

    uploaded_image_path = "mock_images/library.jpg"

    print(f"--- Search 2: Image-to-Text (Hybrid with Filters) ---")
    print(f"Student uploaded (Image): '{uploaded_image_path}'")
    print(f"Wasim/Zain applied filter: {{'type': 'facility_photo'}}")

    image_results = collection.query(
        query_uris=[uploaded_image_path], # Searching using an IMAGE!
        where={"type": "facility_photo"}, # Zain's Logical Filter
        n_results=1,
        include=['documents', 'metadatas']
    )

    print(f"Found related text: {image_results['documents'][0][0]}")
    print(f"SQL ID for Zain: {image_results['metadatas'][0][0]['zain_sql_id']}\n")

    print("Prototype complete. This shows how you handle multimodal inputs while keeping sync with Wasim and Zain!")

if __name__ == "__main__":
    main()
