from cryptography.fernet import Fernet 

global key
key = Fernet.generate_key() 
global f
f = Fernet(key) 

global token

# ---------------------------- ENCRYPTION ------------------------------- #

def encryption(password):
    password=password.encode()
    encrypted_bytes = f.encrypt(password)
    encrypted_bytes=encrypted_bytes.decode('utf-8')
    return encrypted_bytes


# ---------------------------- DECRYPTION ------------------------------- #

def decryption(encrypted_password,f):
    encrypted_password=encrypted_password.encode('utf-8')
    decrypted_bytes = f.decrypt(encrypted_password)
    decrypted_bytes=decrypted_bytes.decode('utf-8')
    return decrypted_bytes

name= "man"
name=encryption(name)
print(name)
name=decryption(name,f)
print(name)

