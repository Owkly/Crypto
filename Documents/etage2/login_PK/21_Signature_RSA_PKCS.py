# RSA PKCS #1 v1.5
# ================

# La signature RSA peut s'implanter de plusieurs manières, mais celle qui est 
# décrite ici (et qui est implantée par OpenSSL) est assez courante.  Il s'agit
# d'appliquer un bourrage qui empêche les attaques triviales par malleabilité.
# Cette procédure est standardisée dans la RFC 3447 :

#       https://www.ietf.org/rfc/rfc3447.txt

# Une implantation open-source se trouve à la fin de ce document

# Pour signer un message M sous une clef (N, d), on applique la procédure 
# suivante :
# 1. [Hachage.]          Calculer : h <-- SHA256(M)
# 2. [Bourrage.]         Assembler le bloc d'octets :

# +------+----------------------------------------------------+----+---------+---+
# | 0001 | FFFFFFFFFFF............................FFFFFFFFFFF | 00 | HASH_ID | h |
# +------+----------------------------------------------------+----+---------+---+

#                        Dont la composition se décompose comme suit :
#                        1. les deux octets 0001
#                        2. un certain nombre d'octets FF (au moins 10)
#                        3. un octet 00
#                        4. une chaine de bits magique qui identifie la fonction
#                           de hachage sha256, et qui vaut :
#                           HASH_ID = 3031300d060960864801650304020105000420
#                        5. l'empreinte du message (32 octets)

#                        Le tout doit faire le même nombre d'octets que le N de la
#                        clef publique --- il faut ajuster le nombre d'octets FF de
#                        bourrage de l'étape b.

# 2. [Exponentiation.]   Voir cette séquence d'octets comme un entier (big-endian),
#                        puis calculer : signature <-- bloc**d % N.

# Pour vérifier une signature, on calcule : bloc <-- signature**e % N, puis on
# vérifie que le bloc a la forme prescrite.


# IMPLANTATION EN PYTHON
# ----------------------

from hashlib import sha256

# Function names respect those in https://www.ietf.org/rfc/rfc3447.txt

# SHA-256
HASH_ID = b'010\r\x06\t`\x86H\x01e\x03\x04\x02\x01\x05\x00\x04 '

def i2osp(x : int, k : int) -> bytes:
    """
    Convert the integer x to a sequence of k bytes
    """
    return x.to_bytes(k, byteorder='big')

def os2ip(x : bytes) -> int:
    """
    Convert the sequence of bytes to an integer
    """
    return int.from_bytes(x, byteorder='big')

def emsa_pkcs1_encode(M : bytes, k : int) -> bytes:
    """
    Encode a message into k bytes for RSA signature
    """
    h = sha256(M)
    T = HASH_ID + h.digest()
    if len(T) + 11 > k:
        raise ValueError("Message Too Long")
    PS = bytes([0xff] * (k - len(T) - 3))
    EM = bytes([0x00, 0x01]) + PS + bytes([0x00]) + T
    return EM

def emsa_pkcs1_decode(EM : bytes, k : int) -> bytes:
    """
    Given an EMSA_PKCS1-encoded message, returns the Hash
    
    >>> x = emsa_pkcs1_encode("toto", 128)
    >>> emsa_pkcs1_decode(x, 128) == sha256("toto".encode()).digest()
    True
    """
    if len(EM) != k:
        raise ValueError("Incorrect Size")
    if EM[:2] != bytes([0x00, 0x01]):
        raise ValueError("Incorrect Header")
    i = 2
    while EM[i] != 0:
        if EM[i] != 0xff:
            raise ValueError("Incorrect Filler")
        i += 1
        if i == k:
            raise ValueError("Only Filler")
    if i < 10:
        raise ValueError("Not enough filler")
    T = EM[i+1:]
    if T[:len(HASH_ID)] != HASH_ID:
        raise ValueError("Bad Hash ID")
    H = T[len(HASH_ID):]
    return H

def key_length(n : int) -> int:
    """
    key length in bytes
    """
    return (n.bit_length() + 7) // 8

def rsa_pkcs_sign(n : int, d : int, M : bytes):
    """
    RSA Signature using PKCS#1 v1.5 encoding
    """
    k = key_length(n)
    EM = emsa_pkcs1_encode(M, k)
    m = os2ip(EM)
    s = pow(m, d, n)
    S = i2osp(s, k)
    return S

def rsa_pkcs_verify(n : int, e : int, M : bytes, S : bytes) -> bool:
    """
    Verify RSA PKCS#1 v1.5 signatures
    """
    k = key_length(n)
    if len(S) != k:
        raise ValueError("Bad length")
    s = os2ip(S)
    m = pow(s, e, n)
    EM = i2osp(m, k)
    H = emsa_pkcs1_decode(EM, k)
    return (H == sha256(M).digest())
