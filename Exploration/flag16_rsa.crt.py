# >>> conseil distributeur de friandises et de gadgets
# Il y a une commande ADMIN, qui demande un mot de passe.  Vous avez ce mot
# de passe, mais chiffré par trois clef publiques différentes.  Commencez
# par récupérer puis examiner les trois clefs publiques.  Qu'on-t-elle de
# spécial ?

# En utilisant le théorème des restes chinois (CRT), il est possible de 
# calculer l'entier m**3 (PAS modulo n).  Partant de là, récupérer m consiste
# à calculer une racine cubique.  (m est l'encodage PKCS#1 v1.5 du mot de
# passe, donc il y a du charabia au début et le mot de passe à la fin).

# Calculer la racine cubique d'un nombre aussi grand (environ 2000 chiffres)
# ne peut pas se faire avec les fonctions usuelles qui travaillent sur des
# flottants avec seulement 64 bits de précision (soit ça va échouer, soit le
# résultat sera faux).  À la place, on peut utiliser la méthode de Newton,
# (cf. Wikipédia) pour le calcul des racines n-ièmes, en effectuant les 
# opérations sur des entiers (donc en faisant des divisions euclidiennes
# tout le temps).

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from sympy import root
from sympy.ntheory.modular import crt

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

def main():
    # Charger les modules et les exposants des clés publiques
    n_julia27, e_julia27 = load_public_key_from_file('flag16_julia27_pkey.pem')
    n_thomasprice, e_thomasprice = load_public_key_from_file('flag16_thomasprice_pkey.pem')
    n_bbrown, e_bbrown = load_public_key_from_file('flag16_bbrown_pkey.pem')

    # Messages chiffrés convertis en entiers
    c_julia27 = int("a2fcd7054cc107e20a9f03ececa6f2ef734af8c07f2e84222a77a2060d7f4081e6a56a00e626995dd389316a7ceafe9f874e0e4fbe93d3d02ec2a16ab13bbc260ac9995c3357dbd38910798dbf67704f73c52ff447a9c5070803e44f1b171cb5236e7e939618704c40104d617b89410bb3fd9481f647053d5c02249719148f39decbd9f1bd5f5b7865aba92afcfd63a39d6240158a435abd002744cd4f14af4237151c7ddc1d15586355176d74f8dbbcfa86b8f9c5d4661f2d9d4bf27f5d5f2e8e167f27a14959507a3c0535650d90ab6754318627c03c1be8048f6fd95f9bc87230384ce476b5a0f3ab23d9e09adc8a83c845f813f62f095fb875f41596bb22", 16)
    c_thomasprice = int("2da917be953f2c66e0b15166213a4ee92a98a611f190fb3e31109f7c8b1a334dd895f21ea793c90ee5b54bcf6c8f87c3feb5f165f59bddd6877158d1374c116df8326d73f67acbee0e392e3e17ec716ba549a933258bcd6833077ee6f93f1277a2809780be30a4a7e350ad78158516a8c7ce9cdf90779ed70a972aaa54b2e423b1ab82f7c755ba04cd4d729547673f6270dd961934904b50d659199c76ea96f0d7c5ad1c87d26688f4e6711f32508021c161790fdad53a292ee431955ccbd2116b7d2e467b274571a06c37156d459e8326ddcf5b386ba49ac94c3ec78fe7b2561869440aac6814434115d3fe3e65d4d0319b8505fe7158a36d0d659629e274d3", 16)
    c_bbrown = int("509bc86f143f25c4a44bfadd4b241fac2ee33f1af3ceb93bce81bc938f8e9d5ee4e53bfcc31d4a81f5d5f42a7c7be80c3169d1d7efe6441be41ec21446eef2a84c2aa14b92341473d358acb70f0e772f54fa3dc7c8f1cced72ba103c35414c36921c62db21a53b9101478f09c69336f68cdb4491f8857912598a989160296eedb94ec87e672e74c709fb6f57c5f3ee7c7661ca3348751eacdf88cf649b0062f3caba2245e6b105c402a38a310b613b5b433c08bb56478c31eed27cb02f72416f45965e3b8f19ee19cca8828c702c44b40b3d0e24d13f527387fd30a8b226dabc6f5a117d0e09cc95fd312d6a70d14b47877ec97f8a672085c0a4d8479e51b361", 16)

    # Utiliser CRT pour trouver M = m^3
    M = crt([n_julia27, n_thomasprice, n_bbrown], [c_julia27, c_thomasprice, c_bbrown])[0]

    # Calculer la racine cubique de M
    m = root(M, 3)

    message_original = int(m).to_bytes((int(m).bit_length() + 7) // 8, 'big')
    print("Mot de passe déchiffré:", message_original)

if __name__ == "__main__":
    main()
