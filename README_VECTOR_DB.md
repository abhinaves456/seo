# Vector Database Prototype Guidelines

Since `chromadb` cannot be installed in this restricted environment, I have provided the `vector_db_prototype.py` script as a reference for you (Abhinav) to run locally on your own machine.

To run it locally, you will need to install ChromaDB:
`pip install chromadb`

The script demonstrates:
1. **Initializing a Vector DB collection** for university policies.
2. **Generating embeddings** for unstructured text (like exam rules, cheating policies, and medical leave procedures).
3. **Attaching Metadata** to those vectors (e.g., `department: engineering`).
4. **Performing Hybrid Search**, showing how you can take logical filters from Zain/Wasim and apply them to your semantic search to get hyper-accurate answers for the students.

## Multimodal Vector Database (Images + Text)

A new prototype script, `multimodal_vector_db_prototype.py`, has been added.
This script demonstrates how you (Abhinav) can handle **Multimedia** queries alongside Wasim and Zain.

### How it works:
Instead of only embedding text, this script uses **OpenCLIP**. CLIP maps both images and text into the exact same vector space.
* If a student searches for "CS Timetable" (Text), your DB can return the actual image file of the timetable.
* If a student uploads a photo of a campus building (Image), your DB can return the text description and policies of that building.

### Running locally
To run this multimodal prototype locally, you will need some additional packages for handling images and neural networks:
`pip install chromadb open-clip-torch torch torchvision pillow`

Run it with:
`python3 multimodal_vector_db_prototype.py`
