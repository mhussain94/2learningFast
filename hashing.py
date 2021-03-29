#class to hash passwords
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #passlib context to create and verify hash passwords

class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password) #generating hashpasswords by using the user input

