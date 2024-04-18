import hashlib
import binascii
import subprocess

def key_expansion(seed: bytes) -> bytes:
    """
    Renvoie 256 bits pseudo-aléatoires à partir de seed.
    """
    state = seed
    output = b''
    for i in range(8):
        state = hashlib.sha256(state).digest()
        output += state[:4]
    return output

def find_key(ivv):
    """
    Trouve la clé pour un vecteur d'initialisation donné.
    """
    for a in range(256):
        for b in range(256):
            key_material = key_expansion(bytes([a, b]))
            K = key_material[0:16]
            IV = key_material[16:32]
            IVVV = binascii.hexlify(IV).decode()
            if IVVV == ivv:
                print("K trouvé :", binascii.hexlify(K).decode())
                return binascii.hexlify(K).decode(), IVVV
    return None, None

def decrypt(key, iv, encrypted_data):
    """
    Déchiffre un fichier chiffré avec la clé key et le vecteur d'initialisation iv.
    """
    args = [
        'openssl', 'enc', '-d', '-aes-128-cbc', '-K', key, '-base64',
        '-iv', iv, '-in', encrypted_data, '-out', 'flag15_decrypted.txt'
    ]
    subprocess.run(args, check=True)

def main():
    ivv = "373e56779ddd54a68ff7179197b14481"
    encrypted = "flag15_encrypted.txt"
    key, iv = find_key(ivv)

    if key and iv:
        decrypt(key, iv, encrypted)
    else:
        print("La clé n'a pas pu être trouvée.")

if __name__ == '__main__':
    main()
