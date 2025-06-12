from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.doc_qa_service import DocQAService, get_doc_qa_service
from app.core.security import require_role

router = APIRouter()

class QARequest(BaseModel):
    question: str

class QAResponse(BaseModel):
    answer: str

@router.post(
    "/doc-qa",
    response_model=QAResponse,
    dependencies=[Depends(require_role("app-user"))],
    )
async def query_documents(
    request: QARequest,
    doc_qa_service: DocQAService = Depends(get_doc_qa_service),
):
    """
    Ask a question about the documents loaded into the system.
    """
    answer = doc_qa_service.query(request.question)
    return QAResponse(answer=answer)