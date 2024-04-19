# >>> conseil laptop
# En résumé, ce laptop effectue (une des étapes) de la signature RSA, mais il
# n'accepte pas forcément de signer tout et n'importe quoi.

# Pour commencer, pour obtenir une signature correcte (c.a.d. qui vérifie avec
# la clef publique en utilisant OpenSSL), il faut appliquer soi-même l'encodage
# PKCS#1 v1.5.  Ensuite, la programme va effectuer la dernière étape 
# (l'élévation à la puissance d modulo N, où d est la clef secrète). La spec 
# de la signature RSA PKCS#1 v1.5 se trouve à la bibliothèque.


# Une bonne manière d'appréhender le problème, c'est de commencer par faire 
# signer n'importe quoi puis de vérifier que les signatures sont valides.

# Conseil général pour la mise au point : essayer d'abord avec une paire de
# clef qu'on a fabriquée soi-même et pour laquelle on connaît tout plutôt que
# d'utiliser le serveur comme une boite noire qui dit ``NON''.

# Ensuite, pour faire signer ce qui nous intéresse, on peut exploiter la
# ***malléabilité*** de RSA.

# Concrètement :
# - on soumet (M * x**e) mod N, pour un x aléatoire.  Ceci "masque" M au serveur.
# - le serveur renvoie (M * x**e)**d == (M**d) * (x**ed) == x * M**d mod N.
# - il suffit d'éliminer le ``masque'' x (en multipliant par l'inverse de x
#   modulo N) et on obtient M**d mod N, c'est-à-dire la signature voulue.



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





from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from Crypto.Util.number import inverse

def load_public_key_from_file(file_path):
    """
    Charge une clé publique RSA à partir d'un fichier PEM.
    """
    with open(file_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key.public_numbers().n, public_key.public_numbers().e

def simulate_signature(m_encoded: int, e: int, n: int, x: int):
    masked_message = (m_encoded * pow(x, e, n)) % n
    return masked_message


def main():
    # Chemin vers la clé publique RSA
    public_key_path = "flag18_director_pkey.pem"
    n, e = load_public_key_from_file(public_key_path)

    # Message à signer
    M = b"I, the lab director, hereby grant Yannick permission to take the BiblioDrone-NG."
    k = (n.bit_length() + 7) // 8  # Calcul de la longueur de la clé en octets

    # Encodage du message
    m = emsa_pkcs1_encode(M, k)
    m_int = os2ip(m)  # Convertir le message encodé en entier

    # Masquage du message
    x = 2  # Choix arbitraire de x
    masked_message = (m_int * pow(x, e, n)) % n
    print(f"Masked message (hex): \n{hex(masked_message)}")
    # il faut envoyer sans le 0x

    # Signature du message masqué reçue
    received_signature = int("bd246f0d66a841db07415bbb978e8774e604327e0645810c15b021ee2fe5209a48ad03ea89ac36b36f224a17f803cbe6f124220658797818995aa57799bc827442ecf4aa477dafb755b6016ff3bdbe7307379554495747b79f52ec807a07254561d0f001a1b8293908dcc2b01a5c815c2a009eb67db26acdac97d99b07fc923e9c0340ec26a2cc8b8e52ec4b9c33f19dfb65376555d9c573e3295fba42488cde3e5763d583d27dddc499a94629dbb6859df02b637e1006dcb2c4e20e5b2624fde0d1d198f4b3a4dde1f9669579172a6487d25029d9a18302cdba5b86c3b01ee18f3627d7d96a7c9e96ae160985ccff2e8c119d2e40436251c7725ddae8c77653",16)

    # Démasquage de la signature
    tmp = (received_signature) * (inverse(x, n)) % n
    original_signature = hex(tmp)
    print(f"Original signature (hex):\n{original_signature}")
    # il faut envoyer sans le 0x

if __name__ == "__main__":
    main()