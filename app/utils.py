from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # telling passlib to use bcrypt hashing algorithm


def hash(pwd: str):
    return pwd_context.hash(pwd)
