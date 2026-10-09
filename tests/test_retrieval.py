from codebase_atlas.indexing import FunctionEntry
from codebase_atlas.retrieval import get_score, search_functions, tokenize


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


def test_search_functions():
    entries = [
        FunctionEntry(
            file="a.py",
            symbol="check_token",
            start_line=1,
            end_line=2,
            source="def check_token():\n    pass",
        ),
        FunctionEntry(
            file="a.py",
            symbol="read_token",
            start_line=1,
            end_line=2,
            source="def read_token():\n    pass",
        ),
        FunctionEntry(
            file="z.py",
            symbol="validate_token",
            start_line=1,
            end_line=2,
            source="def validate_token():\n    pass",
        ),
        FunctionEntry(
            file="profile.py",
            symbol="get_profile",
            start_line=1,
            end_line=2,
            source="def get_profile():\n    token = None",
        ),
        FunctionEntry(
            file="database.py",
            symbol="find_user",
            start_line=1,
            end_line=2,
            source="def find_user():\n    return None",
        ),
    ]

    results = search_functions("token", entries, limit=3)

    assert [r.entry.symbol for r in results] == [
        "check_token",
        "read_token",
        "validate_token",
    ]
    assert [r.score for r in results] == [4, 4, 4]
