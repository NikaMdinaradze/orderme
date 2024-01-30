from passlib.context import CryptContext


def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashing(password):
    return pwd_cxt.hash(password)


def verify(plain_password, hashed_password):
    return pwd_cxt.verify(plain_password, hashed_password)
