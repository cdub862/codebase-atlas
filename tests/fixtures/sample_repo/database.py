USERS = {
    "alice": {"id": 1, "name": "Alice"},
    "bob": {"id": 2, "name": "Bob"},
}


def find_user(username: str):
    return USERS.get(username)
