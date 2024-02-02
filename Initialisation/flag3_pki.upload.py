import subprocess

def generate_rsa_keypair(key_size, skey_path, pkey_path):
    # Commande pour créer une clé privé : openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048
    gen_skey_args = [
        'openssl', 'genpkey', '-algorithm', 'RSA', '-pkeyopt', f'rsa_keygen_bits:{key_size}'
    ]
    
    # Exécute la commande pour générer la clé privée
    skey_process = subprocess.run(gen_skey_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Vérifier si la commande a réussi
    if skey_process.returncode != 0:
        raise Exception(f"Erreur lors de la génération de la clé privée RSA: {skey_process.stderr.decode()}")
    
    # Sauvegarder la clé privée le fichier spécifié
    with open(skey_path, "wb") as private_key_file:
        private_key_file.write(skey_process.stdout)
    print(f"Clé privée RSA de {key_size} bits générée et sauvegardée dans '{skey_path}'")









    # Commande pour extraire la clé publique à partir de la clé privée : openssl pkey -in <fichier qui contient la skey> -pubout
    gen_pkey_args = [
        'openssl', 'pkey', '-in', skey_path, '-pubout'
    ]
    
    # Exécute la commande pour générer la clé publique
    pkey_process = subprocess.run(gen_pkey_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Vérifier si la commande a réussi
    if pkey_process.returncode != 0:
        raise Exception(f"Erreur lors de l'extraction de la clé publique RSA: {pkey_process.stderr.decode()}")
    
    # Sauvegarder la clé publique dans un fichier
    with open(pkey_path, "wb") as public_key_file:
        public_key_file.write(pkey_process.stdout)
    print(f"Clé publique RSA extraite et sauvegardée dans '{pkey_path}'")


# Utilisation de la fonction
key_size = 2048                     # Taille de la clé en bits
# Les chemins ont été changés mes fichiers de base était "flag3_pkey.pem" et "flag3_skey.pem"
skey_path = "flag3_pkey2.pem"       # Chemin de la clé privée
pkey_path = "flag3_skey2.pem"       # Chemin de la clé publique

try:
    generate_rsa_keypair(key_size, skey_path, pkey_path)
except Exception as e:
    print(f"Une erreur s'est produite: {e}")
