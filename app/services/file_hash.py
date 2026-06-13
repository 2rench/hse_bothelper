import hashlib


def calculate_hash(
    content: bytes,
) -> str:

    return hashlib.sha256(
        content
    ).hexdigest()
