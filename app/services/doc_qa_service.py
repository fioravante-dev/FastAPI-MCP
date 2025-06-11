from app.agents.doc_qa.agent import create_doc_qa_engine

class DocQAService:
    def __init__(self):
        # The engine is created once when the service is instantiated
        self.query_engine = create_doc_qa_engine()

    def query(self, question: str) -> str:
        """Sends a query to the document agent and gets a response."""
        response = self.query_engine.query(question)
        return str(response)

# Create a single, reusable instance
doc_qa_service = DocQAService()

def get_doc_qa_service() -> DocQAService:
    """Dependency injector for the DocQAService."""
    return doc_qa_service