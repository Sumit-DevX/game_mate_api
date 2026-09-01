from pwdlib import PasswordHash
from pydantic import validate_call

password_hash = PasswordHash.recommended()

@validate_call
def generate_hash(password : str) -> str:

    hashed_password = password_hash.hash(password)

    return hashed_password

@validate_call
def verify_password(password : str , hashed_password : str) -> bool:
    

    try:
        return password_hash.verify(password, hashed_password)
    except Exception: 
        return False
