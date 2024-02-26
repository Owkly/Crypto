import subprocess

def generate_csr(key_file, output_csr_file, subject_name):
    """
    Génère un CSR à l'aide d'OpenSSL

    paramètres: key_file (str): Chemin vers le fichier de la clé privée.
                output_csr_file (str): Chemin où le CSR généré sera sauvegardé.
                subject_name (str): identité associée à cette clef publique ("subject")
    """
    # Construction de la commande OpenSSL
    command = [
        'openssl', 'req', '-new', '-key', key_file,
        '-out', output_csr_file, '-subj', f'/CN={subject_name}', '-batch'
    ]
    
    # Exécution de la commande
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"CSR généré avec succès et sauvegardé dans {output_csr_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la génération du CSR: {e.stderr.decode()}")

# Utilisation de la fonction
if __name__ == "__main__":
    key_file = "flag10_skey.pem"
    output_csr_file = "flag10_csr.pem"
    subject_name = "Yannick"

    generate_csr(key_file, output_csr_file, subject_name)
