from hashlib import sha256
from random import randint

def HASH(a, b, c):
    hash=sha256()
    hash.update(str(a).encode())
    hash.update(str(b).encode())
    hash.update(str(c).encode())
    return int(hash.hexdigest(), 16)

def convert_message_to_int(M):
    return int(sha256(M.encode()).hexdigest(), 16)

def gen_public_sig(X, M):

    a = 2 # Generator
    p = 2695139 # Large Prime Number

    x = convert_message_to_int(X)

    m = convert_message_to_int(M)

    x = x+m

    y = pow(a, x, p)
    r = randint(1, p - 1)

    t = pow(a, r, p)
    c = randint(0, 1)

    s = (c * x) + r

    tuple = (y, s, c, t)
    
    return tuple

# verify the 
def verify(tuple):

    y, s, c, t = tuple

    a = 2  # Generator
    p = 2695139 # Large Prime Number

    if (pow(a, s, p) == (pow(y, c, p) * t) % p):
        return True
    return False