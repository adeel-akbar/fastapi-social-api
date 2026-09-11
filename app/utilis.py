from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()

def hash_password(password: str):
    return password_hasher.hash(password)

def verify_password(plain, hashed):
    return password_hasher.verify(plain, hashed)