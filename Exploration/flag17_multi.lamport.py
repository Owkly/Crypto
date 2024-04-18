import json
import base64
import textwrap
from hashlib import sha256
from binascii import unhexlify

class LamportPrivateKey:
    def __init__(self, key_elements):
        self.key = key_elements
    
    def _prefix(self):
        return "-----BEGIN LAMPORT PRIVATE KEY-----"
    
    def _suffix(self):
        return "-----END LAMPORT PRIVATE KEY-----"
    
    def dumps(self) -> str:
        # Encode les composants de la clé privée en base64 et les formate dans un format PEM
        payload = base64.b64encode(b''.join(self.key)).decode('utf-8')
        middle = '\n'.join(textwrap.wrap(payload, width=64))
        return f"{self._prefix()}\n{middle}\n{self._suffix()}"
    
    def sign(self, message):
        # Signe un message avec la clé privée Lamport
        sig = b''
        h = int.from_bytes(sha256(message).digest(), byteorder='big')
        for i in range(256):
            b = (h >> i) & 1
            sig += self.key[2 * i + b]
        return sig.hex()

def reconstruct_components(messages, signatures):
    """
    Reconstitue les composants de la clé privée Lamport à partir des messages et des signatures
    """
    components = {}
    for message, signature in zip(messages, signatures):
        signature_bytes = unhexlify(signature)
        hash_digest = sha256(message).digest()
        h = int.from_bytes(hash_digest, byteorder='big')
        for i in range(256):
            bit = (h >> i) & 1
            index = 2 * i + bit
            components[index] = signature_bytes[i*32:(i+1)*32]
    return components

def main():
    # Charger les messages et les signatures depuis le fichier JSON
    file_path = 'flag17.json'
    messages = []
    signatures = []
    
    with open(file_path, 'r') as file:
        data_array = json.load(file)
        for data in data_array:
            messages.append(data["message"].encode()) 
            signatures.append(data["signature"]) # signatures sont déjà des chaînes hexadécimales
    print("Les messages et les signatures ont été chargés avec succès.")

    # Reconstituer les composants de la clé privée à partir des messages et des signatures
    components = reconstruct_components(messages, signatures)

    # Préparer le tableau des éléments de la clé privée
    private_key_elements = [b''] * 512
    for index, component in components.items():
        private_key_elements[index] = component

    # Reconstruire la clé privée Lamport et l'écrire dans un fichier PEM
    lamport_key = LamportPrivateKey(private_key_elements)
    pem_representation = lamport_key.dumps()
    with open('flag17_lamport.pem', 'w') as f:
        f.write(pem_representation)
    print("La clé privée Lamport a été reconstruite avec succès et est stockée dans flag17_lampport.pem")

    # Signe un message avec la clé privée Lamport et écris la signature dans un fichier
    msg = b"quilt bolls apart elfin clave"
    signature_result = lamport_key.sign(msg)
    with open('flag17_signature.txt', 'w') as f:
        f.write(signature_result)
    print("Le message a été signé avec succès et la signature est stockée dans flag17_signature.txt")

if __name__ == "__main__":
    main()
