# >>> use card
# La porte ne s'ouvre pas. Une lumière rouge est allumée sur le lecteur de badge.
# Le micro-écran LCD affiche "DEVICE DOES NOT CONTAIN A PUBLIC KEY".


# >>> use NFC
# Vous ne pouvez pas faire grand-chose avec, mais vous pourriez essayer
# d'utiliser un AUTRE objet dessus.

# >>> conseil NFC
# Votre carte d'étudiant doit pouvoir être lue par ce dispositif.

# >>> conseil NFC
# Avez-vous lu le memento qui est dans la pièce à côté ?

# >>> conseil NFC
# Il vous faut produire une paire de clefs RSA dont la clef publique, 
# encodée en base64, contient "+++ATRIUM+++".  Sans trop rentrer dans les
# détails, la clef publique contient n et e, plus quelques octets de bourrage
# à cause de la sérialisation asn.1 (c'est assez compliqué).  Il faut donc
# que la "chaîne promotionnelle" apparaisse soit dans n soit dans e quand
# on représente le tout en base64.


# >>> conseil NFC
# Entre n et e, c'est e qui est plus facile à contrôler : en effet on peut
# le **choisir** librement lors de la création de la paire de clefs.  Mais
# attention !  Il doit être impair.


# >>> conseil NFC
# L'encodage en base64 complique le tout (ne pas hésiter à lire la page 
# wikipédia qui correspond).  En effet, chaque paquet de 6 bits est encodé en
# un caractère.  3 octets du départ (24 bits) sont donc représentés par 4
# caractères.  Si la "chaine promotionnelle" ne commence pas à une position
# qui est un multiple de 3 dans la clef de départ, alors elle sera "à cheval"
# sur des caractères ASCII différents, elle et n'apparaîtra pas correctement.
# Une solution potentielle consiste à ajouter un ou deux octets AVANT dans e.


# >>> conseil NFC
# C'est tout !


from Crypto.PublicKey import RSA
import base64

def generate_rsa_keys(base64_string, public_key_file, private_key_file):
    """
    Génère une paire de clés RSA à partir d'une valeur en base64 qui détermine l'exposant public

    paramètres: base64_string (str): Chaîne en base64 à convertir pour l'exposant public.
                public_key_file (str): Chemin où la clé publique sera sauvegardée.
                private_key_file (str): Chemin où la clé privée sera sauvegardée.
    """
    # Décodage de e en base64
    decoded_bytes = base64.b64decode(base64_string)
    print("e (en bytes) : ", decoded_bytes)

    # Conversion en valeur décimale
    decimal_value = int.from_bytes(decoded_bytes, byteorder='big')
    print("e (en décimal) : ", decimal_value)

    # Génération de la paire de clés RSA avec e comme exposant public
    key = RSA.generate(bits=2048, randfunc=None, e=decimal_value)

    # Sauvegarde des clés dans des fichiers  
    with open(private_key_file, 'wb') as f:
        f.write(key.export_key('PEM'))
    with open(public_key_file, 'wb') as f:
        f.write(key.publickey().export_key('PEM'))

# Utilisation de la fonction
if __name__ == "__main__":
    base64_string = "ee+++ATRIUM+++ed"
    public_key_file = "flag11_pkey.pem"
    private_key_file = "flag11_skey.pem"

    generate_rsa_keys(base64_string, public_key_file, private_key_file)
