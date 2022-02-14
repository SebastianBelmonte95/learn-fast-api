from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    """This function hashes a string (password) and returns the encoded string"""
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    """This function verifiers that the hgashed plain password matches with the hashed password in our DB"""
    return pwd_context.verify(plain_password, hashed_password)
