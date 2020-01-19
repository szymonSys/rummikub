import secrets
from TypeControl import TypeControl


class KeyGenerator(TypeControl):
    def __init__(self): pass

    @staticmethod
    def generate_key():
        return secrets.token_urlsafe(16)
