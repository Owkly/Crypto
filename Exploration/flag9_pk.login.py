import sys
import os

# Importe la fonction decrypt_sym_key depuis ./Initialisation/flag1_register.py
current_directory = os.path.dirname(__file__)
initialisation_directory = os.path.join(current_directory, '..', 'Initialisation')
initialisation_directory = os.path.normpath(initialisation_directory)
if initialisation_directory not in sys.path:
    sys.path.append(initialisation_directory)
    
from flag4_power_on import sign_msg_skey, display_signature_hex

if __name__ == "__main__":
    # Signature et vérification du message 'challenge'
    challenge = "paint wooer quack fetes comet"
    skey_path = os.path.join(initialisation_directory, "flag3_skey.pem")
    signature_path = "flag9_signature_challenge.bin"
    try:
        sign_msg_skey(challenge, skey_path, signature_path)
        print(f"Signature du message '{challenge}' sauvegardée dans '{signature_path}'")
        # Afficher la signature en hexadécimal
        display_signature_hex(signature_path)
    except Exception as e:
        print("Une erreur s'est produite lors de la signature ou de la vérification de 'challenge':", e)
