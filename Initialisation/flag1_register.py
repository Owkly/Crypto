import subprocess

def decrypt_sym_key(msg_enc, passphrase, cipher='aes-128-cbc'):
    """
    Déchiffre un message avec une clé symétrique
    paramètres: msg_enc -> message chiffré
                passphrase -> clé symétrique
                cipher -> algorithme de chiffrement (par défaut: aes-128-cbc)
    """
    # Commande pour déchiffrer un message avec une clé symétrique : openssl enc -d -base64 -aes-128-cbc -pbkdf2 -pass pass:<symkey> -in <message chiffré>
    args = ['openssl', 'enc', '-d', '-base64', '-' + cipher, '-pbkdf2', '-pass', 'pass:' + passphrase]

    # Si le message est une chaîne de caractères, le convertir en utf-8
    if isinstance(msg_enc, str):
        msg_enc = msg_enc.encode('utf-8')
        
    # Exécute la commande pour déchiffrer le message
    result = subprocess.run(args, input=msg_enc,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Vérifie s'il y a des erreurs
    if result.stderr:
        error_message = result.stderr.decode()
        raise Exception(f"Erreur lors du déchiffrement : {error_message}")

    return result.stdout.decode()



if __name__ == "__main__":
    encrypted = """U2FsdGVkX1/51wqD7PnMSuRkwL8czQ1S/AznUxY9Z+K2tN2o5LBv1C2cM2fDGGD9
    hQym6B/W3VH0TNEn7dU2Xg=="""     # Message chiffré
    symkey = "ISECR0XX"             # clé symétrique

    try:
        decrypted = decrypt_sym_key(encrypted, symkey)
        print(decrypted)
    except Exception as e:
        print(e)