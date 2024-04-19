import json
import binascii
from cryptography.hazmat.primitives.asymmetric import padding, ec
from cryptography.hazmat.primitives import hashes
from cryptography.x509 import load_pem_x509_certificate
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend

def load_transactions(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['batch']['transactions']

def verify_transaction(transaction):
    try:
        # Chargement des certificats
        card_cert = load_pem_x509_certificate(transaction['card']['certificate'].encode(), default_backend())
        bank_cert = load_pem_x509_certificate(transaction['card']['bank']['certificate'].encode(), default_backend())

        # Vérification de la signature de la carte
        card_cert.public_key().verify(
            binascii.unhexlify(transaction['signature']),
            transaction['data'].encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )

        # Charger le certificat CA
        with open("flag19_ca.pem", "rb") as f:
            ca_cert = load_pem_x509_certificate(f.read(), default_backend())

        # Vérification de la chaîne de certificats
        ca_cert.public_key().verify(
            bank_cert.signature,
            bank_cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            bank_cert.signature_hash_algorithm,
        )

        bank_cert.public_key().verify(
            card_cert.signature,
            card_cert.tbs_certificate_bytes
        )

        # Vérification des données contenues dans la transaction
        if transaction['card']['number'] not in transaction['data'] or transaction['card']['bank']['name'] not in transaction['data']:
            return 0

        return 1

    except Exception as e:
        print("Une erreur s'est produite lors de la vérification :", e)
        return 0

def main():
    transactions = load_transactions('flag19_transaction.json')
    results = [verify_transaction(tx) for tx in transactions]
    print("\nRésultats des vérifications des transactions :\n", results)

if __name__ == "__main__":
    main()