from hashlib import sha256
from random import randint

def HASH(a, b, c):
    hash=sha256()
    hash.update(str(a).encode())
    hash.update(str(b).encode())
    hash.update(str(c).encode())
    return int(hash.hexdigest(),16)

def convert_message_to_int(M):
    return int(sha256(M.encode()).hexdigest(), 16)

def gen_public_sig(X, M):

    a = 2 # Generator
    p = 2695139 # Large Prime Number

    x = convert_message_to_int(X)

    m = convert_message_to_int(M)

    y = pow(a, x, p)
    r = randint(1, p - 1)

    t1 = pow(m, x, p)
    t2 = pow(m, r, p)
    t3 = pow(a, r, p)
    c = HASH(t1, t2, t3)

    s = (c * x) + r

    tuple = (y, s, t1, t2, t3)
    
    return tuple

# verify the 
def verify(t):

    y, s, t1, t2, t3 = t

    a = 2  # Generator
    p = 2695139 # Large Prime Number

    c = HASH(t1, t2, t3)

    if (pow(a, s, p) == (pow(y, c, p) * t3) % p):
        return True
    return False