# 031 Document Ingestion Skeleton

## What Problem Did This Solve?

The RAG pipeline needs a clean entry point for adding documents before chunking, embeddings, vector search, or citations can happen.

## Why Was This Design Chosen?

We created a document ingestion API, service layer, and in-memory document store. This separates API validation, ingestion logic, and storage concerns.

## What Alternatives Exist?

- Start directly with a vector database
- Store documents only in local files
- Use Postgres immediately
- Upload files before supporting raw text
- Combine ingestion, chunking, and embeddings in one endpoint

## What Would Break If This Component Disappeared?

The platform would not have a stable boundary for documents entering the RAG pipeline. Chunking and embedding logic would be forced to handle raw request concerns directly.

## How Would This Evolve At 10x Traffic?

Raw content would be stored in S3 or object storage, metadata in Postgres, ingestion jobs would run asynchronously, and indexing status would be tracked through background workers.

## Interview Questions

1. Why does RAG start with ingestion?
2. Why separate document service from document store?
3. Why use an in-memory store first?
4. What metadata should a production document store track?
5. Why not create embeddings in the first ingestion step?