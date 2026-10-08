TOKENS = {
    "test-token-alice": "alice",
    "test-token-bob": "bob",
}

def validate_token(token: str):
    return TOKENS.get(token, None)