from codebase_atlas.retrieval import tokenize


def test_tokenize():
    assert tokenize("validate_token") == {"validate", "token"}
    assert tokenize("Where is TOKEN validated?") == {"where", "is", "token", "validated"}
    assert tokenize("token token token") == {"token"}
    assert tokenize("getUser123") == {"getuser123"}
    assert tokenize("") == set()
