from typing import Optional

from app.core.config import Settings, get_settings
from app.embeddings.base import EmbeddingProvider
from app.embeddings.factory import get_embedding_provider
from app.llm.base import LLMProvider
from app.llm.factory import get_llm_provider
from app.observability.llm import record_llm_call
from app.prompts.registry import get_prompt_template
from app.rag.repository import DocumentRepository
from app.schemas.document import Citation, RAGQueryResponse


class RAGService:
    def __init__(
        self,
        repository: DocumentRepository,
        embedding_provider: Optional[EmbeddingProvider] = None,
        llm_provider: Optional[LLMProvider] = None,
        settings: Optional[Settings] = None,
    ):
        self.repository = repository
        self.embedding_provider = embedding_provider or get_embedding_provider()
        self.llm_provider = llm_provider or get_llm_provider()
        self.settings = settings or get_settings()

    async def answer(self, question: str, top_k: Optional[int] = None) -> RAGQueryResponse:
        requested_top_k = top_k or self.settings.rag_default_top_k
        effective_top_k = min(requested_top_k, self.settings.rag_max_top_k)
        query_embedding = (await self.embedding_provider.embed([question]))[0]
        matches = self.repository.search_chunks(
            query_embedding=query_embedding,
            limit=effective_top_k,
            min_similarity=self.settings.rag_min_similarity,
            embedding_provider=self.embedding_provider.name,
            embedding_model=self.settings.embedding_model,
        )

        citations = [
            Citation(
                citation_id=f"S{index}",
                document_id=match.chunk.document_id,
                document_title=match.document_title,
                chunk_id=match.chunk.chunk_id,
                chunk_index=match.chunk.chunk_index,
                content=match.chunk.content,
                score=round(match.score, 4),
            )
            for index, match in enumerate(matches, start=1)
        ]
        context = "\n\n".join(
            f"[{citation.citation_id}] {citation.document_title}\n{citation.content}"
            for citation in citations
        ) or "No relevant knowledge was retrieved."

        prompt_template = get_prompt_template("rag.answer")
        prompt = prompt_template.render(question=question, context=context)
        result = await self.llm_provider.generate(prompt)
        record_llm_call(
            prompt_id=prompt_template.prompt_id,
            result=result,
            metadata={
                "workflow": "rag:v1",
                "retrieval_count": len(citations),
            },
        )

        return RAGQueryResponse(
            answer=result.content,
            citations=citations,
            retrieval_count=len(citations),
            provider=result.provider,
            model=result.model,
            prompt_id=prompt_template.prompt_id,
        )
