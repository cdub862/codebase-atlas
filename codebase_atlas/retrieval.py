import re
from dataclasses import dataclass

from codebase_atlas.indexing import FunctionEntry


@dataclass(frozen=True)
class SearchResult:
    entry: FunctionEntry
    score: int


def tokenize(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", s.lower()))


def get_score(query: str, entry: FunctionEntry):
    query_tokens = tokenize(query)
    symbol_tokens = tokenize(entry.symbol)
    source_tokens = tokenize(entry.source)

    points = 0
    points += len(query_tokens & symbol_tokens) * 3
    points += len(query_tokens & source_tokens) * 1

    return points


def search_functions(
    query: str,
    entries: list[FunctionEntry],
    limit: int = 5,
) -> list[SearchResult]:

    results = [
        SearchResult(entry=entry, score=get_score(query, entry)) for entry in entries
    ]
    results = sorted(
        [r for r in results if r.score > 0],
        key=lambda r: (-r.score, r.entry.file, r.entry.symbol),
    )[:limit]

    return results
