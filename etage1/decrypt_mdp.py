import subprocess


def decrypt(msg_enc, passphrase, cipher='aes-128-cbc'):
    # openssl enc -d -base64 -aes-128-cbc -pbkdf2 -pass pass:"bar" -in foo
    args = ['openssl', 'enc', '-d', '-base64', '-' + cipher, '-pbkdf2', '-pass', 'pass:' + passphrase]

    # Si msg_enc est de type str, on est obligé de l'encoder en bytes pour pouvoir l'envoyer dans le pipeline vers openssl
    if isinstance(msg_enc, str):
        msg_enc = msg_enc.encode('utf-8')
        
    # Exécute la commande openssl
    result = subprocess.run(args, input=msg_enc,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Vérifie s'il y a des erreurs
    if result.stderr:
        error_message = result.stderr.decode()
        raise Exception(f"Erreur lors du déchiffrement : {error_message}")

    return result.stdout.decode()


try:
    encrypted = """U2FsdGVkX1/GwTarSAt7jGSVkwJ42JirfJJ9livrJM6YdVipNT0DBla0CxpIFPoc
cxFaNUXFfOyMmEc6qdoELw=="""
    key = "ISECR0XX"
    decrypted = decrypt(encrypted, key)
    print("Message déchiffré:", decrypted)
except Exception as e:
    print("Une erreur s'est produite lors du déchiffrement:", e)


