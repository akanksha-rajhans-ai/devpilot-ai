from dataclasses import dataclass
from statistics import mean

from app.embeddings.base import EmbeddingProvider
from app.rag.repository import DocumentRepository


@dataclass(frozen=True)
class RetrievalCase:
    question: str
    expected_document_id: str


@dataclass(frozen=True)
class RetrievalEvaluation:
    case_count: int
    hit_rate_at_k: float
    mean_reciprocal_rank: float
    failures: list[dict]


async def evaluate_retrieval(
    repository: DocumentRepository,
    embedding_provider: EmbeddingProvider,
    cases: list[RetrievalCase],
    top_k: int = 4,
) -> RetrievalEvaluation:
    reciprocal_ranks = []
    failures = []

    for case in cases:
        query_embedding = (await embedding_provider.embed([case.question]))[0]
        matches = repository.search_chunks(query_embedding, top_k, -1.0)
        ranked_document_ids = [match.chunk.document_id for match in matches]

        try:
            rank = ranked_document_ids.index(case.expected_document_id) + 1
            reciprocal_ranks.append(1.0 / rank)
        except ValueError:
            reciprocal_ranks.append(0.0)
            failures.append(
                {
                    "question": case.question,
                    "expected_document_id": case.expected_document_id,
                    "retrieved_document_ids": ranked_document_ids,
                }
            )

    if not cases:
        return RetrievalEvaluation(0, 0.0, 0.0, [])

    return RetrievalEvaluation(
        case_count=len(cases),
        hit_rate_at_k=round(
            sum(rank > 0 for rank in reciprocal_ranks) / len(cases),
            4,
        ),
        mean_reciprocal_rank=round(mean(reciprocal_ranks), 4),
        failures=failures,
    )
