import subprocess
import binascii
import json

class OpensslError(Exception):
    pass

def encrypt(plaintext, passphrase, cipher='aes-128-cbc'):
    pass_arg = 'pass:{}'.format(passphrase)
    args = ['openssl', 'enc', '-' + cipher, '-base64', '-pass', pass_arg, '-pbkdf2']
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    result = subprocess.run(args, input=plaintext, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_message = result.stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)
    return result.stdout.decode()

def encrypt_with_public_key(publicKey, plaintext):
    args = ['openssl', 'pkeyutl', '-encrypt', '-pubin', '-inkey', publicKey]
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    result = subprocess.run(args, input=plaintext, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_message = result.stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)
    hex_encoded = binascii.hexlify(result.stdout).decode()
    return hex_encoded

def hybrid_encryption(message, passphrase, public_key_file):
    # Chiffrer le message avec une clé symétrique
    ciphertext = encrypt(message, passphrase)

    # Chiffrer la passphrase avec la clé publique
    encrypted_session_key = encrypt_with_public_key(public_key_file, passphrase)

    # Rassembler les résultats dans un format JSON
    result = {
        "session-key": encrypted_session_key,
        "ciphertext": ciphertext
    }
    return json.dumps(result, indent=4)

# Exemple d'utilisation
try:
    passphrase = "3729FDJ389393NV3823F"
    message = "test"
    public_key = "flag15.pem"
    
    encrypted_data = hybrid_encryption(message, passphrase, public_key)
    print("Données chiffrées avec succès :")
    print(encrypted_data)
except OpensslError as e:
    print("Erreur lors du chiffrement :", e)
