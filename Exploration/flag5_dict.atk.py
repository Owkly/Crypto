import sys
import os

# Importe la fonction decrypt_sym_key depuis ./Initialisation/flag1_register.py
current_directory = os.path.dirname(__file__)
initialisation_directory = os.path.join(current_directory, '..', 'Initialisation')
initialisation_directory = os.path.normpath(initialisation_directory)
if initialisation_directory not in sys.path:
    sys.path.append(initialisation_directory)
    
from flag1_register import decrypt_sym_key

if __name__ == "__main__":
    # données du challenge
    encrypted_text = "U2FsdGVkX1+JDJgfeCeSjMJI4KkUMSFQ3Ai2ZyUFIAeyeabQ2JYbfJt66sUKMfur\n"
    expected_result = "snood wafts lusts niece bulgy"

    line_count = 0
    try:
        with open("flag5_words.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line_count += 1
                if line_count % 100 == 0:
                    print(line_count)
                try:
                    # decrypte le texte avec le mot actuel sans le caractère de fin de ligne
                    decrypted = decrypt_sym_key(encrypted_text, line.rstrip()) 
                    if decrypted == expected_result:
                        print("Matching line {}:".format(line_count), line.rstrip())
                        break
                # Erreur lors du déchiffrement
                except Exception as e:
                    continue
    # Erreur lors de l'ouverture du fichier
    except IOError:
        print("File not found or can't be opened")
        
    

