# >>> conseil digicode
# Le panneau en liège montre un message chiffré par les deux clefs publiques.
# Ce serait sûrement utile de le déchiffrer.  Mais cette fois, aucune clef
# secrète n'est opportunément disponible.


# >>> conseil digicode
# Ceci est cepdendant possible car les deux clefs publiques ont le même N.

# >>> conseil digicode
# La formule magique est : ``CRT dans les exposants''.

# >>> conseil digicode
# En clair, cherchez une relation de Bezout u*e1 + v*e2 == 1.

# >>> conseil digicode
# Après, vous avez c1 == m**e1 mod N et c2 == m**e2 mod N.  Par conséquent,
# c1**u * c2**v == m**(u*e1 + v*e2) == m mod N.  Et boum.


# >>> conseil digicode
# Rappel : m**(-42) == (m**42)**(-1) == (m**(-1))**42 mod N

# >>> conseil digicode
# C'est tout !


from Crypto.PublicKey import RSA
import sympy

def decrypt_shared_n_message(public_key_file1, public_key_file2, ciphertext_hex1, ciphertext_hex2):
    """
    Déchiffre un message à partir de deux clés publiques partageant le même module N
    et de deux ciphertexts, en utilisant l'algorithme du reste chinois.

    paramètres: public_key_file1 (str): Chemin vers le fichier de la première clé publique.
                public_key_file2 (str): Chemin vers le fichier de la deuxième clé publique.
                ciphertext_hex1 (str): Ciphertext associé à la première clé publique, en hexadécimal.
                ciphertext_hex2 (str): Ciphertext associé à la deuxième clé publique, en hexadécimal.
    """
    # Chargement des clés publiques
    with open(public_key_file1, 'r') as f:
        pkey1 = RSA.import_key(f.read())

    with open(public_key_file2, 'r') as f:
        pkey2 = RSA.import_key(f.read())

    # Extraire e et N de chaque clé
    e1, N1 = pkey1.e, pkey1.n
    e2, N2 = pkey2.e, pkey2.n

    # Vérification que N est le même pour les deux clés
    assert N1 == N2, "Les modules des deux clés publiques ne sont pas égaux"

    # Conversion des ciphertexts en entiers
    c1_int = int(ciphertext_hex1, 16)
    c2_int = int(ciphertext_hex2, 16)

    # Calcul de u et v à l'aide de l'extension de l'algorithme d'Euclide
    u, v = sympy.gcdex(e1, e2)[0:2]
    u, v = int(u), int(v)

    # Calcul du message m
    N = N1  # Identique à N2
    m = (pow(c1_int, u, N) * pow(c2_int, v, N)) % N

    # Conversion du message en bytes puis en texte
    m_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
    print(f"Message déchiffré (bytes) : {m_bytes}")

# Utilisation de la fonction
if __name__ == "__main__":
    public_key_file1 = 'flag12_paul29_pkey.pem'
    public_key_file2 = 'flag12_tjacobso_pkey.pem'
    ciphertext_hex1 = "00fed7981a24ae867d9515bd497237e0d3c3d0ab86eba80df936992af5735e4d808e6e25bd5346515bb88878f79776f85465fd6feff6f8e0ca3f333131c186e85e8850903625e067db689c8dcf9222bab3b03a0fae7881edfad1cf7db84520b7de14d2bfd44a9c33472a574f650a2db4cd500510b8cc69e99d754b9f6c59feb8a06521b0bbe93c87a39474b0e12656e31cc2490bd6fed68c34124385c82e68ed21e66115f834368ecfd5832c3d6a88cc460e207835e6329d4ebf7db4df162b0cd3031dcbc3c4ff62f58972dd255e3acc7216037301abd76893c42db6d5be9ecb965cd626be252a4afb8578a7e0cd8efcf1fdaf63b2c6670ff6417745037eb7aa"
    ciphertext_hex2 = "2c67626c9a401e9fdf46e77086c1395681e09f12ed6fad111be2eed27c5e6dc39ff400d64d100c140672bcd2fef981ca7961670e43e2cc894cb3446079895435efff5c3ba3934bca97de18e6de378da934e4fe75991543b2781fccc0da37969f97adde1e65183e3ef80b57afa9f2b9ca86c5941430c4c9db5418087280506f818700466c5771a6022528c415d4b4cd9aa3d0e80fa0f678de46a2de4a649cad064d7cdaa6eb7e3c0cfe757f3207eb57b1964e72dd239d329f6b0908766bf8c20a19857159f89638e9147ceec866e4eade28fdf2e1d62b6d3be97b14815f65cb8dc279d09c17e35d96e6e6eba53b825b0c486fc51e907f14816e6a87817f1328f7"

    decrypt_shared_n_message(public_key_file1, public_key_file2, ciphertext_hex1, ciphertext_hex2)
