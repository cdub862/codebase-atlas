from auth import validate_token
from database import find_user


def get_profile(token: str):
    username = validate_token(token)

    if username is None:
        return {"error": "Unauthorized"}

    return {
        "data": find_user(username)
    }