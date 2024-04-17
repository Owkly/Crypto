import subprocess

class OpensslError(Exception):
    pass

def get_signature(message, private_key):
    # Générer la signature
    args = ['openssl', 'dgst', '-sha256', '-sign', private_key, '-out', 'flag14_signature.bin']

    if isinstance(message, str):
        message = message.encode('utf-8')

    result = subprocess.run(args, input=message, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # si un message d'erreur est présent sur stderr, on arrête tout
    # attention, sur stderr on récupère des bytes(), donc on convertit
    error_message = result.stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)
    
def get_signature_of_public_key(public_key, private_key):
    # Générer la signature
    args = ['openssl', 'dgst', '-sha256', '-sign', private_key, '-out', 'flag14_signature.bin', public_key]
    subprocess.run(args)

def verify_signature(message, public_key):
    # Vérifier la signature 
    args = ['openssl', 'dgst', '-sha256', '-verify', public_key, '-signature', 'flag14_signature.bin', message]
    subprocess.run(args)

def create_hex(file):
    # Générer le fichier hex sans sauts de ligne
    with open(file, 'rb') as infile, open('flag14_signature.hex', 'w') as outfile:
        hex_data = infile.read().hex()
        outfile.write(hex_data)


def create_csr(private_key, csr):
    # Générer le fichier csr
    args = ['openssl', 'req', '-new', '-key', private_key, '-out', csr, '-subj', '/CN=Thomas']
    subprocess.run(args)

# Utilisation de la fonction
# challenge ="scarf stony taper parch icers"
pkey = "flag14_my_pkey.pem"
get_signature_of_public_key(pkey, "flag14_romain_skey.pem")
# get_signature(challenge, "private_key.pem")
create_hex("flag14_signature.bin")
# create_csr("private_key.pem", "ma_csr.pem")
