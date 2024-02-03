import subprocess

def sign_msg_pkey(msg, skey, signature_path):
    # Commande pour signer un message avec la clé privée : openssl dgst -sha256 -sign <fichier contenant la clé privée> -out <fichier pour la signature> -hex
    args = ['openssl', 'dgst', '-sha256', '-sign', skey, '-out', signature_path, '-hex']

    # Si le message est une chaîne de caractères, le convertir en utf-8
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    
    # Exécute la commande pour signer le message
    result = subprocess.run(args, input=msg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Vérifie s'il y a des erreurs
    error_message = result.stderr.decode()
    if error_message != '':
        raise Exception(error_message)

# Utilisation de la fonction
upload= "axmen muter toils divan cocks"             # Message à signer
challenge = "towed patsy bulbs snaky nabob"         # Message à signer pour activer l'électricité
skey = "flag3_skey.pem"                             # Fichier contenant la clé privée
signature_path_1 = "flag4_signature_upload.txt"     # Fichier contenant la signature
signature_path_2 = "flag4_signature_challenge.txt"  # Fichier contenant la signature

try:
    sign_msg_pkey(upload, skey, signature_path_1)
    print(f"Signature du message '{upload}' sauvegardée dans '{signature_path_1}'")
except Exception as e:
    print("Une erreur s'est produite lors de la signature:", e)

try:
    sign_msg_pkey(challenge, skey, signature_path_2)
    print(f"Signature du message '{challenge}' sauvegardée dans '{signature_path_2}'")
except Exception as e:
    print("Une erreur s'est produite lors de la signature:", e)



