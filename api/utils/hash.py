from hashlib import md5


def hash_password(email: str, password: str) -> str:
    return md5(f'{email}:{password}'.encode()).hexdigest()
