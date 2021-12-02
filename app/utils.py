from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_Password(Password : str):
    return pwd_context.hash(Password)


def verify(plainPassword :str,hashed_Password : str):
    return pwd_context.verify(plainPassword,hashed_Password)    


  