from hashlib import sha256

print(sha256("Conrado".encode("ascii")).hexdigest())
