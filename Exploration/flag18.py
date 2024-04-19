import subprocess

def generate_csr(private_key, csr, subject):
    # Générer le CSR
    args = ['openssl', 'req', '-new', '-key', private_key, '-batch', '-subj', subject, '-out', csr]
    subprocess.run(args)

private_key = "flag18_my_skey.pem"
csr_file = "flag18_csr_pkey.pem"
subject = "/CN=Yannick"
# generate csr
generate_csr(private_key, csr_file, subject)