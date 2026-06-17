import json
import re
from abc import ABC, abstractmethod

# ==========================================
# 1. THE INTERFACE (The "USB Port")
# ==========================================
class BaseIntentProcessor(ABC):
    """
    This is the blueprint. ANY intent processor Wasim builds
    must follow these rules. This guarantees modularity!
    """

    @abstractmethod
    def process_query(self, raw_text: str) -> dict:
        """
        Takes raw text and returns a dictionary with:
        - 'intent': What the user wants (e.g., 'policy_search', 'timetable')
        - 'logical_filters': Hard data for Zain (e.g., department, course code)
        - 'semantic_query': Cleaned text for Abhinav's Vector DB
        """
        pass

# ==========================================
# 2. IMPLEMENTATION A: Simple Regex/Keyword (Fast, Cheap)
# ==========================================
class SimpleRegexIntentProcessor(BaseIntentProcessor):
    """A basic processor to get the project started."""

    def process_query(self, raw_text: str) -> dict:
        text_lower = raw_text.lower()

        # 1. Determine Intent
        intent = "general_chat"
        if any(word in text_lower for word in ["policy", "rules", "leave", "makeup"]):
            intent = "policy_search" # Route to Abhinav (Vector DB)
        elif any(word in text_lower for word in ["exam", "timetable", "schedule"]):
            intent = "timetable_search" # Route to Zain (Logical DB)

        # 2. Extract Logical Filters for Zain
        filters = {}
        if "engineering" in text_lower:
            filters["department"] = "engineering"
        elif "business" in text_lower:
            filters["department"] = "business"

        # Extract course codes like CS101 or ENG204 using regex
        course_match = re.search(r'[a-z]{2,3}\d{3}', text_lower)
        if course_match:
            filters["course_code"] = course_match.group().upper()

        # 3. Clean query for Abhinav (Remove the hard filters so Vector DB doesn't get confused)
        # Note: In a real advanced setup, this step is handled by an LLM rewriting the query.
        semantic_query = text_lower

        return {
            "intent": intent,
            "logical_filters": filters,
            "semantic_query": semantic_query
        }

# ==========================================
# 3. IMPLEMENTATION B: Advanced LLM (Placeholder for the future)
# ==========================================
class LLMIntentProcessor(BaseIntentProcessor):
    """
    Wasim can build this later using OpenAI or an open-source model.
    Because it inherits from BaseIntentProcessor, it will drop right in!
    """
    def __init__(self, api_key: str):
        self.api_key = api_key

    def process_query(self, raw_text: str) -> dict:
        print("[LLM Processor] Sending prompt to AI model to extract entities...")
        # Simulate LLM Response
        return {
            "intent": "policy_search",
            "logical_filters": {"department": "engineering", "urgency": "high"},
            "semantic_query": "procedure for missing a lab due to medical emergency"
        }

# ==========================================
# 4. THE MAIN APPLICATION ROUTER
# ==========================================
def handle_student_query(processor: BaseIntentProcessor, query: str):
    """
    This function doesn't care which processor is used!
    It just runs the standard 'process_query' function.
    """
    print(f"\n--- Processing Query: '{query}' ---")

    # 1. Run Wasim's Intent Processing
    extracted_data = processor.process_query(query)

    print(json.dumps(extracted_data, indent=2))

    # 2. Routing Logic based on Intent
    intent = extracted_data["intent"]

    if intent == "timetable_search":
        print("-> ROUTING TO ZAIN (Logical DB): Exact timetable lookup using filters.")
    elif intent == "policy_search":
        print("-> ROUTING TO ABHINAV (Vector DB): Semantic search for policy.")
        if extracted_data["logical_filters"]:
            print(f"   * Applying Zain's Logical Filters: {extracted_data['logical_filters']}")
    else:
        print("-> ROUTING TO CHATBOT: General conversation.")

# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    # --- Modularity in Action ---
    # We instantiate the simple processor.
    # To upgrade later, Wasim simply changes this ONE line to:
    # active_processor = LLMIntentProcessor(api_key="sk-123")

    active_processor = SimpleRegexIntentProcessor()

    # Test Query 1 (Hard Facts - Goes to Zain)
    query_1 = "I am an engineering student. When is the CS101 midterm exam?"
    handle_student_query(active_processor, query_1)

    # Test Query 2 (Fuzzy Policy - Goes to Abhinav + Zain's filters)
    query_2 = "I missed my engineering lab because I was sick, what is the makeup policy?"
    handle_student_query(active_processor, query_2)
