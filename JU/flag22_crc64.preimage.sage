# Définition de l'environnement et des variables
q = x^64 + x^4 + x^3 + x + 1  # Polynôme irréductible pour GF(2^64)
F = GF(2)['x']  
Q = F(q)  					  # Convertir q en polynôme dans F



# Conversion de la valeur hexadécimale en séquence de bits
hashpwd_hex = "62e995e65d8c054d"
hashpwd_int = int.from_bytes(bytes.fromhex(hashpwd_hex), byteorder='big')
hashpwd_bin = bin(hashpwd_int)[2:].zfill(64)  # Binaire avec remplissage pour 64 bits



# Création du polynôme S(x) à partir de la séquence binaire
s_x = " + ".join([f"x^{i}" for i, bit in enumerate(reversed(hashpwd_bin)) if bit == '1'])
S = F(s_x)



# Calcul de l'inverse de (x^4 + x^3 + x + 1) modulo Q(x)
Poly = F(x^4 + x^3 + x + 1)
I = Poly.inverse_mod(Q)



# Calcul de P(x) comme l'inverse de Q multiplié par S
P = I * S



# Conversion de P(x) en chaîne binaire et ensuite en hexadécimal
coef_list = [int(coef) for coef in P.list()]
binary_str = ''.join(str(bit) for bit in coef_list[::-1])
int_value = int(binary_str, 2)
hex_value = hex(int_value)[2:].zfill(16)  # Assurez-vous que la chaîne hexadécimale a 16 caractères



# Afficher le résultat final
print("USER : MKT01")
print(f"Resulting Hex value: {hex_value}")
