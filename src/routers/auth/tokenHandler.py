from src.utils.singelton import singleton

@singleton
class TokenHandler():
    def __init__(self) -> None:
        self.tokens:dict = {}

    def add_token(self, email:str, token:str) -> None:
        if not token in self.tokens:
            self.tokens[email] = token
        
    def is_token_active(self, token:str) -> bool:
        if token in self.tokens.values():
            return True
        else:
            return False
        
    def delete_token(self, token:str) -> None:
        self.tokens = {key: val for key, val in self.tokens.items() if val != token}