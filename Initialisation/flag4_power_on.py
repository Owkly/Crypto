import subprocess

class OpensslError(Exception):
    pass

def sign_msg_pkey(msg, skey, signature_path):
    # Construit la commande avec les arguments corrects
    args = ['openssl', 'dgst', '-sha256', '-sign', skey, '-out', signature_path, '-hex']

    # Si le message est une chaîne de caractères, le convertir en utf-8
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    
    # Exécute la commande pour signer le message
    result = subprocess.run(args, input=msg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Vérifie s'il y a des erreurs
    error_message = result.stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

# Utilisation de la fonction
upload= "axmen muter toils divan cocks"             # Message à signer
challenge = "towed patsy bulbs snaky nabob"         # Message à signer
skey = "flag3_skey.pem"                             # Fichier contenant la clé privée
signature_path_1 = "flag4_signature_upload.hex"        # Fichier contenant la signature
signature_path_2 = "flag4_signature_challenge.hex"  # Fichier contenant la signature

try:
    sign_msg_pkey(upload, skey, signature_path_1)
    print(f"Signature du message '{upload}' sauvegardée dans '{signature_path_1}'")
except OpensslError as e:
    print("Une erreur s'est produite lors de la signature:", e)

try:
    sign_msg_pkey(challenge, skey, signature_path_2)
    print(f"Signature du message '{challenge}' sauvegardée dans '{signature_path_2}'")
except OpensslError as e:
    print("Une erreur s'est produite lors de la signature:", e)



