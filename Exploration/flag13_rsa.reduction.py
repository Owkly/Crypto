# >>> conseil serrure
# Avez-vous fouillé les environs ?  Vous allez trouver quelque chose d'utile.

# Vous pouvez essayer avec la clef perdue par un des deux occupants.  Si ça ne
# marche pas, alors il vous faut réussir à vous faire passer pour l'AUTRE occupant.


# Le ``mémento'' explique que les occupants du même bureau doivent avoir le même N.

# Comme vous avez le d de l'un des deux, vous pouvez factoriser leur N commun.

# (c'est dans les diapos du cours)

# De là, vous pouvez obtenir le d de l'autre.


# username: qharris
# d       : 7932b7688d199e911584c5561788f4893130a9c80aa1d5c4bbaf0280ad2073689486ecdda8989e9f7627b13e8376f76ce54d2849f9942cddc250e470dd8ddc9d4071b0b938ef0ea6b04c8387eed82a4788ef85bff1c1cabf60c51111fced2343c4e8b33ccdc8363f3fd0f0c5fb1ba9206514bc33966914545b1001fdb480a4d209e0da70fa8650d723cd3bd1864dac67ec2cdbbd3d148c32a776f63dd6f576e386eb5b339c976fdfdff58ef987e7a9be2584c579d24b0da7c4e00df914dba684b2ade5aac4bff3ed0bedaf7ad9a7ab4659cf99424fea0e3372e0a00e3993ffbae2a894a2834856e4bfd4b10c89aa4da262654beb582b73c258364dfd47945d19


import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import sympy
import random

def load_public_key_from_file(file_path):
    """
    Charge une clé publique RSA à partir d'un fichier PEM.
    """
    with open(file_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key.public_numbers().e, public_key.public_numbers().n

def puissance_modulo(base, exposant, modulo):
    """
    Exponentiation rapide pour calculer (base^exposant) % modulo.
    """
    resultat = 1
    while exposant > 0:
        if exposant % 2 == 1:
            resultat = (resultat * base) % modulo
        base = (base * base) % modulo
        exposant //= 2
    return resultat

def factor(N, e, d):
    """
    Tente de factoriser N utilisant e et d.
    """
    x = random.randint(2, N-2)  # Choix d'une base aléatoire pour plus de généralité
    ed_minus_1 = e * d - 1
    s = ed_minus_1
    while s % 2 == 0:
        s //= 2
        y = puissance_modulo(x, s, N)
        if y != 1 and y != N - 1:
            p = sympy.gcd(y - 1, N)
            if p != 1 and p != N:
                return p, N // p
    return None, None  # Retourner None si aucun facteur n'est trouvé

def mod_inverse(e, phi_n):
    """
    Calcule l'inverse modulaire de e modulo phi_n.
    """
    return sympy.mod_inverse(e, phi_n)

def rsa_sign(message, d, N):
    # Hasher le message avec SHA-256
    message_hash = hashlib.sha256(message.encode()).digest()
    # Convertir le hash en un entier long
    hash_int = int.from_bytes(message_hash, byteorder='big')
    # Signer le hash avec la clé privée en utilisant l'exponentiation modulaire
    signature_int = pow(hash_int, d, N)
    # Convertir la signature en bytes pour faciliter le stockage ou le transport
    signature = signature_int.to_bytes((signature_int.bit_length() + 7) // 8, byteorder='big')
    return signature.hex()  # Retourner la signature en format hexadécimal

def create_private_key_file(d, N, e, p, q, filename):
    # Calcul des paramètres CRT
    phi_n = (p - 1) * (q - 1)
    d = sympy.mod_inverse(e, phi_n)
    dmp1 = d % (p - 1)
    dmq1 = d % (q - 1)
    iqmp = sympy.mod_inverse(q, p)
    
    private_numbers = rsa.RSAPrivateNumbers(
        p=int(p),
		q=int(q),
		d=int(d),
		dmp1=int(dmp1),
		dmq1=int(dmq1),
		iqmp=int(iqmp),
        public_numbers=rsa.RSAPublicNumbers(e, N)
    ).private_key(default_backend())

    pem = private_numbers.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(filename, 'wb') as f:
        f.write(pem)


def main():
    public_key_file1 = 'flag13_qharris_pkey.pem'
    public_key_file2 = 'flag13_brucevaldez_pkey.pem'
    e1, N = load_public_key_from_file(public_key_file1)
    e2, _ = load_public_key_from_file(public_key_file2)

    # d de qharris
    d1_hex = "7932b7688d199e911584c5561788f4893130a9c80aa1d5c4bbaf0280ad2073689486ecdda8989e9f7627b13e8376f76ce54d2849f9942cddc250e470dd8ddc9d4071b0b938ef0ea6b04c8387eed82a4788ef85bff1c1cabf60c51111fced2343c4e8b33ccdc8363f3fd0f0c5fb1ba9206514bc33966914545b1001fdb480a4d209e0da70fa8650d723cd3bd1864dac67ec2cdbbd3d148c32a776f63dd6f576e386eb5b339c976fdfdff58ef987e7a9be2584c579d24b0da7c4e00df914dba684b2ade5aac4bff3ed0bedaf7ad9a7ab4659cf99424fea0e3372e0a00e3993ffbae2a894a2834856e4bfd4b10c89aa4da262654beb582b73c258364dfd47945d19"
    d1 = int(d1_hex, 16)  # Convertir de hexadécimal à entier

    p, q = factor(N, e1, d1)
    if p and q:
        print("Facteurs trouvés pour N:")
        print(f"p = {p}")
        print(f"q = {q}")
        phi_n = (p - 1) * (q - 1)
        d2 = mod_inverse(e2, phi_n)
        print(f"d2 trouvée : {d2}")
        print(f"d2 en hexadécimal: {hex(d2)}")
        
        # Enregistrer la clé privée dans un fichier PEM
        create_private_key_file(d2, N, e2, p, q, "flag13_skey.pem")
        print("Clé privée enregistrée dans 'flag13_skey.pem'")
  
    else:
        print('Aucun facteur trouvé pour N.')

if __name__ == "__main__":
    main()
