# ADR 0037: Establish Retrieval Metrics Before Model-Based Evaluation

## Status

Accepted

## Decision

The first evaluation layer uses deterministic hit rate at K and mean reciprocal
rank against versioned expected documents. Generation and faithfulness evaluators
will be added after a representative dataset exists.

## Consequences

The initial metrics are explainable and inexpensive but do not measure answer
correctness by themselves.
