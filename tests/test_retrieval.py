from codebase_atlas.indexing import FunctionEntry
from codebase_atlas.retrieval import get_score, tokenize


def test_tokenize():
    assert tokenize("validate_token") == {"validate", "token"}
    assert tokenize("Where is TOKEN validated?") == {"where", "is", "token", "validated"}
    assert tokenize("token token token") == {"token"}
    assert tokenize("getUser123") == {"getuser123"}
    assert tokenize("") == set()


def test_get_score():
    entry = FunctionEntry(
        file="auth.py",
        symbol="validate_token",
        start_line=1,
        end_line=2,
        source="def validate_token(token):\n    return token in TOKENS",
    )

    assert get_score("token", entry) == 4
    assert get_score("validate token", entry) == 8
    assert get_score("TOKENS", entry) == 1
    assert get_score("database", entry) == 0
    assert get_score("token token", entry) == 4
