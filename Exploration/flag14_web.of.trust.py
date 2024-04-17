import subprocess
import binascii
import json
import os

def sym_encrypt(plaintext, passphrase, cipher='aes-128-cbc'):
    """Chiffre un message avec une clé symétrique."""
    
    pass_arg = f'pass:{passphrase}'
    args = ['openssl', 'enc', '-' + cipher, '-base64', '-pass', pass_arg, '-pbkdf2']
    
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    result = subprocess.run(args, input=plaintext, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_message = result.stderr.decode()
    
    if error_message != '':
        raise Exception(f"Erreur lors du chiffrement symétrique : {error_message}")
    return result.stdout.decode()

def rsa_encrypt(publicKeyFile, plaintext):
    """Chiffre un message avec une clé publique."""
    
    args = ['openssl', 'pkeyutl', '-encrypt', '-pubin', '-inkey', publicKeyFile]
    
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    result = subprocess.run(args, input=plaintext, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_message = result.stderr.decode()
    
    if error_message != '':
        raise Exception(f"Erreur lors du chiffrement RSA : {error_message}")
    
    ciphertext_hex = binascii.hexlify(result.stdout).decode()
    return ciphertext_hex

def full_hybrid_encryption(message, passphrase, publicKeyFile):
    """Effectue un chiffrement hybride complet du message."""
    
    ciphertext = sym_encrypt(message, passphrase)
    encrypted_session_key = rsa_encrypt(publicKeyFile, passphrase)
    # session key en hexadécimal et ciphertext en base64
    encrypted_data = json.dumps({
        "session-key": encrypted_session_key,
        "ciphertext": ciphertext
    })
    return encrypted_data

def main():
    message = "Test"
    sym_key = binascii.hexlify(os.urandom(16)).decode('utf-8')
    path_to_public_key = 'flag14_robot_key.pem'
    encrypted_data = full_hybrid_encryption(message, sym_key, path_to_public_key)
    print(encrypted_data)

if __name__ == '__main__':
    main()
