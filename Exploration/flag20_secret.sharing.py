# >>> conseil spécification du journal des évènements

# Ceci affirme qu'avec 9 flags, on peut fabriquer une "firmware update key",
# puis qu'avec 17 flags on peut en fabriquer une autre, etc.

# Il faut donc implanter la reconstruction de partage de secret de Shamir.

# Cela peut se faire de deux manières : soit avec les polynômes interpolateurs
# de Lagrange, soit en résolvant un système linéaire.  Dans les deux cas,
# l'utilisation d'un logiciel de calcul formel (comme SageMath) est fortement
# recommandée.  Il n'y a pas beaucoup de bibliothèques python capable de faire
# le job directement.








# ensemble des flags obtenus jusqu'à présent (MAC)
flags_mac = [
	"99b75790fbdbdd3d6aac5199f666744ad95939df184fe9d9bae148672833729d",
	"78d578987ec1b855d24acd949d3e539c0e014982e4050cfb0add6e9dea3e40ce",
	"63ce4e0e806c62dbd452054e03666ddb18cfa88833ef4950701dab7cb0fb0fb8",
	"40294b7ff0ae55ea647d882de452b3de93b5226d6eff895f7abc1abcba5b89df",
	"caf41960020e8bcd070c2edc00819e50600ec196bbd91680f6e0d9dda67f8c44",
	"220a64ceae1061053e72c55547379acb7d5b8f0ae5ff4eba87b10b146808eb4d",
	"951f2d9e86f9a4c46b61c325f4b8d9f42e2448f8a725bfede0003865346a92ae",
	"7a555996d42b91dd6204ab9abd23c41f7d2699b89032e5ecb36a57c2e7a614cd",
	"867f790029d943d1c164febbc296af1952766639a3af26bc107da2254a94e50c",
	"0e99697ed1c938d5b9280fc4d5cbcc75ffee7f6e4d419ce7011d31bc776d4c90",
	"c69f45f34f051cf8a8b63b90453be12daed50212019c64f6ff7756e79df239cb",
	"8ea0344f4e71e5b113b200581b70a82cf4f9102f5269901cf3d58b72acfcb687",
	"5ab545ed72ce4ea958a06a954b4aa4fcfcc17b1a357e3d5f4a68a2f37176977a",
	"35cc552dc6e2fcf35d243e61d44fc94150093e0e001b737aa7127a837b423c8c",
	"cb97a5f95ddcd88e51421a831efd86ca8e401613ba896d37626e938beb69a7e3",
	"85d79dc91865aae90a992bf1104005cab0db7f2a020426627129b4684469f586",
	"9fc13dd9e754286d8400c703ba2722e45332a93fbff95c373659412c91f164b5",
	"1d6ecac5a77ce5a6451f1a916915316c801975402b4fcbf5dde8c440aa132bf5",
	"c8ad30faa28983690a3b96f26e2a9b631e328988db0ac4bef62e3a7ff5300a25",
	"940e6ea8d01a14159b3dfeae0a6ae9be1a3a67e4d2fc2a9efeb820b57b8cf279"
]




def hex_to_bin(hex_string):
    # Convertit une chaîne hexadécimale en une chaîne binaire
    bin_string = bin(int(hex_string, 16))[2:].zfill(len(hex_string)*4)
    return bin_string

def extract_X_A_B_from_MAC(mac):
    # Convertit le MAC en binaire
    mac_bin = hex_to_bin(mac)
    # Extrait X, A, et B en utilisant la séquence binaire
    X_bin = mac_bin[0:64]
    A_bin = mac_bin[64:128]
    B_bin = mac_bin[128:192]
    # Convertit les binaires en entiers
    X = int(X_bin, 2)
    A = int(A_bin, 2)
    B = int(B_bin, 2)
    return X, A, B



# Listes pour stocker les valeurs X, A et B extraites
Xs = []
As = []
Bs = []

# Boucle sur les MACs pour extraire X, A et B
for mac in flags_mac:
    X, A, B = extract_X_A_B_from_MAC(mac)
    Xs.append(X)
    As.append(A)
    Bs.append(B)

# Affiche les listes Xs, As et Bs
print("Xs=", Xs)
print("As=", As)
print("Bs=", Bs)
