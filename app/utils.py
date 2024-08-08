from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # telling passlib to use bcrypt hashing algorithm

#hashes the password
def hash(pwd: str):
    return pwd_context.hash(pwd)
    
#verify the password from user while logging in with the hashed password in DB
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
