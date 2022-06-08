import jwt
from config import CONFIG
from typing import TypeVar

T = TypeVar("T")

class AuthorizationHandler:
    
    def encode_jwt_token(self, payload: T) -> str:
        return jwt.encode(payload.__dict__, CONFIG['token_secret'], CONFIG['token_algorithm'])
    
    def decode_jwt_token(self, token: str) -> dict:
        return jwt.decode(token, CONFIG['token_secret'], CONFIG['token_algorithm'])
    
    def is_valid(self, toValidate: T, token: str) -> bool:
        return toValidate.__dict__ == self.decode_jwt_token(token)