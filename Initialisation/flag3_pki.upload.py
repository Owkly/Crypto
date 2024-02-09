import subprocess

def generate_skey(key_size, skey_path):
    """
    Génère une clé privée RSA
    paramètres: key_size -> taille de la clé en bits
                skey_path -> chemin du fichier pour sauvegarder la clé privée
    """
    # Génère une clé privée RSA de la taille spécifiée
    gen_skey_args = ['openssl', 'genpkey', '-algorithm', 'RSA', '-pkeyopt', f'rsa_keygen_bits:{key_size}']
    skey_process = subprocess.run(gen_skey_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Vérifie s'il y a des erreurs
    if skey_process.returncode != 0:
        raise Exception(f"Erreur lors de la génération de la clé privée RSA: {skey_process.stderr.decode()}")
    
    # Sauvegarde la clé privée dans un fichier
    with open(skey_path, "wb") as private_key_file:
        private_key_file.write(skey_process.stdout)
    print(f"Clé privée RSA de {key_size} bits générée et sauvegardée dans '{skey_path}'")



def extract_pkey(skey_path, pkey_path):
    """
    Extrait la clé publique RSA à partir de la clé privée
    paramètres: skey_path -> chemin du fichier contenant la clé privée
                pkey_path -> chemin du fichier pour sauvegarder la clé publique
    """
    # Extrait la clé publique RSA à partir de la clé privée
    gen_pkey_args = ['openssl', 'pkey', '-in', skey_path, '-pubout']
    pkey_process = subprocess.run(gen_pkey_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Vérifie s'il y a des erreurs
    if pkey_process.returncode != 0:
        raise Exception(f"Erreur lors de l'extraction de la clé publique RSA: {pkey_process.stderr.decode()}")
    
    # Sauvegarde la clé publique dans un fichier
    with open(pkey_path, "wb") as public_key_file:
        public_key_file.write(pkey_process.stdout)
    print(f"Clé publique RSA extraite et sauvegardée dans '{pkey_path}'")



if __name__ == "__main__":
    # Paramètres de la clé
    key_size = 2048                     # Taille de la clé en bits
    skey_path = "flag3_skey.pem"        # Chemin de la clé privée
    pkey_path = "flag3_pkey.pem"        # Chemin de la clé publique

    try:
        generate_skey(key_size, skey_path)
        extract_pkey(skey_path, pkey_path)
    except Exception as e:
        print(f"Une erreur s'est produite: {e}")
