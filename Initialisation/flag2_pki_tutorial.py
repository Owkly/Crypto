import subprocess
import binascii
class OpensslError(Exception):
    pass


def encrypt_pkey(msg, publickey):
	# Commande pour chiffrer un message avec la clé publique : openssl pkeyutl -encrypt -pubin -inkey <fichier contenant la pkey>
    args = ['openssl', 'pkeyutl', '-encrypt', '-pubin', '-inkey', publickey]

    # Vérifier si msg est de type str
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    
    # Exécute la commande pour chiffrer le message
    result = subprocess.run(args, input=msg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Vérifie s'il y a des erreurs
    error_message = result.stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

	# conversion en hexadécimal
    hex_encoded = binascii.hexlify(result.stdout).decode()
    return hex_encoded


# Utilisation de la fonction
msg = "I got it!"                           # Message à chiffrer
publickey = "flag2_pki_tutorial_key.pem"    # Fichier contenant la clé publique
try:
    encrypted = encrypt_pkey(msg, publickey)
    print(encrypted)
except OpensslError as e:
    print("Une erreur s'est produite lors du chiffrement:", e)
