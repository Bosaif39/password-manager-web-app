# importing hashlib for getting sha256() hash function
"""


import hashlib
password="C2xZS1$4*"
string = password.encode('utf-8')
sha256 = hashlib.sha256()
sha256.update(string)
string_hash = sha256.hexdigest()
password=string_hash

print(len(password))
"""