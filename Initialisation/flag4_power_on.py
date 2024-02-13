import subprocess

def sign_msg_skey(msg, skey, signature_path):
    """
    Signe un message avec une clé privée (résultat binaire stockés dans le signature_path)
    paramètres: msg -> message à signer
                skey -> fichier contenant la clé privée
                signature_path -> fichier pour sauvegarder la signature
    """
    
    # Si le message est une chaîne de caractères, le convertir en bytes
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
        
    # Exécute la commande pour signer le message
    args = ['openssl', 'dgst', '-sha256', '-sign', skey, '-out', signature_path]
    result = subprocess.run(args, input=msg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Vérifie s'il y a des erreurs
    error_message = result.stderr.decode()
    if error_message != '':
        raise Exception(error_message)

def verify_signature(msg, signature_path, pubkey_path):
    """
    Vérifie la signature d'un message avec une clé publique
    paramètres: msg -> message à vérifier
                signature_path -> fichier contenant la signature
                pubkey_path -> fichier contenant la clé publique
    """
    # Si le message est une chaîne de caractères, le convertir en bytes
    if isinstance(msg, str):
        msg = msg.encode('utf-8')
    
    # Exécute la commande pour vérifier la signature
    args = ['openssl', 'dgst', '-sha256', '-verify', pubkey_path, '-signature', signature_path]
    result = subprocess.run(args, input=msg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Vérifie s'il y a des erreurs et affiche le résultat
    output_message = result.stdout.decode()
    error_message = result.stderr.decode()
    if "Verified OK" in output_message:
        print("La signature est valide.")
    else:
        print("La signature est invalide.")
        if error_message:
            print("Erreur:", error_message)
            
def display_signature_hex(signature_path):
    """
    Lit une signature depuis un fichier et affiche son contenu en hexadécimal.
    parmaètre : signature_path -> fichier contenant le message signé
    """
    try:
        with open(signature_path, 'rb') as signature_file:
            signature_content = signature_file.read()
            print(f"Contenu de la signature en hexadécimal: \n{signature_content.hex()}\n")
    except Exception as e:
        print(f"Erreur lors de la lecture de la signature: {e}")


if __name__ == "__main__":
    # Messages à signer et à vérifier, et chemins des fichiers
    upload = "axmen muter toils divan cocks"
    challenge = "towed patsy bulbs snaky nabob"
    skey = "flag3_skey.pem"         # chemin clé privée
    pubkey_path = "flag3_pkey.pem"  # chemin clé publique
    signature_path_1 = "flag4_signature_upload.bin"
    signature_path_2 = "flag4_signature_challenge.bin"

    # Signature et vérification du message 'upload'
    try:
        sign_msg_skey(upload, skey, signature_path_1)
        print(f"Signature du message '{upload}' sauvegardée dans '{signature_path_1}'")
        # Afficher la signature en hexadécimal
        display_signature_hex(signature_path_1)
        verify_signature(upload, signature_path_1, pubkey_path)
    except Exception as e:
        print("Une erreur s'est produite lors de la signature ou de la vérification de 'upload':", e)

    # Signature et vérification du message 'challenge'
    try:
        sign_msg_skey(challenge, skey, signature_path_2)
        print(f"Signature du message '{challenge}' sauvegardée dans '{signature_path_2}'")
        # Afficher la signature en hexadécimal
        display_signature_hex(signature_path_2)
        verify_signature(challenge, signature_path_2, pubkey_path)
    except Exception as e:
        print("Une erreur s'est produite lors de la signature ou de la vérification de 'challenge':", e)

