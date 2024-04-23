# [SUDO]>>> conseil ZRR
# Vous pouvez obtenir des indications avec cette commande.

# Sans argument, cette commande vous suggérera une tâche à accomplir.

# Avec le nom d'un objet en argument, la commande vous donnera des conseils de plus en
# plus précis pour vous aider à acquérir ou à utiliser l'objet en question.

# Si vous avez bien compris, vous pouvez ré-essayer.

# [SUDO]>>> conseil ZRR
# Avez-vous trouvé la description de son fonctionnement ?

# [SUDO]>>> conseil ZRR
# Il y a un programme de recherche de collision quelque part sur le campus.

# [SUDO]>>> conseil ZRR
# OK, on ne va pas vous décourager ; il est caché au bâtiment Atrium.

# [SUDO]>>> conseil ZRR
# Pour s'en sortir, il faut absolument visualiser le principe général de
# fonctionnement de la fonction de hachage : la fonction de compression
# traite les blocs de message les uns après les autres.  Plus précisément,
# le message à hacher s'écrit M = M_0 || M_1 || M_2 || ... et on pose :
#     h[-1]  = IV
#     h[i+1] = F(h[i], M_i)
# La dernière valeur h[] produite est l'empreinte du message M.  Dans ces
# indications, on note :
#     [h_1] ---X----> [h_2]
# pour indiquer que, partant de l'état interne h_1, le fait de traiter la séquence
# de blocs X aboutit à un nouvel état interne h_2.


# [SUDO]>>> conseil ZRR
# Le programme de recherche de collision fonctionne de la façon suivante :
# - Il lit un "fichier préfixe" (éventuellement vide), dont la taille doit être
#   un multiple de la taille des blocs.

# - Le préfixe est haché, ce qui aboutit à une valeur de l'état interne h_prefix:
#       [IV] ---Prefix---> [h_prefix]

# - À partir de là, un algorithme de recherche de collision est lancé. Cet
#   algorithme produit deux séquences de deux blocs chacunes, (A_0, A_1) et
#   (B_0, B_1), avec la propriété suivante :
#       h_prefix ---A_0---> ??? ---A_1---> h_coll
#       h_prefix ---B_0---> ??? ---B_1---> h_coll
# Du coup, on a la collision :
#     MD5(prefixe || A) == MD5(prefixe || B).
# Notez que l'utilitaire n'inclut pas automatiquement le prefixe dans les
# deux fichiers qu'il produit.


# [SUDO]>>> conseil ZRR
# Pour mettre son nom d'utilisateur au début, il suffit de produire un préfixe
# (de la bonne taille) qui commence par son nom d'utilisateur, et qui finisse
# par n'importe quoi.


# [SUDO]>>> conseil ZRR
# Pour mettre "h4ckm0d3" à la fin, ce n'est pas beaucoup plus compliqué.  L'astuce,
# c'est qu'une fois qu'on a deux messages qui collisionnent, on peut les recycler
# en rajoutant ce qu'on veut après.  En effet, on a :
#     [IV] ---Prefix---> [h_prefix] ---A_0---> ??? ---A_1---> [h_coll]
#     [IV] ---Prefix---> [h_prefix] ---B_0---> ??? ---B_1---> [h_coll]

# Comme, de façon bien commode, les chaines : (Prefix || A) et (Prefix || B) ont
# une taille qui est un multiple de la taille du bloc, tout ce qu'on pourrait
# rajouter après va aller dans un nouveau bloc, et ne va donc pas perturber la
# collision :
#     [IV] ---Prefix---> [h_prefix] ---A---> [h_coll] ---Suffix---> [h_suffix]
#     [IV] ---Prefix---> [h_prefix] ---B---> [h_coll] ---Suffix---> [h_suffix]
# Notez que le mécanisme de padding va entrer en action dans le suffixe, mais
# que ça n'est pas un problème.


# [SUDO]>>> conseil ZRR
# La partie un peu plus délicate consiste à produire non pas DEUX fichiers qui
# collisionnent, mais QUATRE.  Pour cela, il faut utiliser la technique suivante,
# inventée par Antoine Joux en 2004.  Partant d'une valeur de l'état interne
# quelconque (disons h_0), on trouve une première collision :
#     [h_0] ---A---> [h_1]
#     [h_0] ---B---> [h_1]
# Puis, partant de h_1, on trouve une deuxième collision :
#     [h_1] ---C---> [h_2]
#     [h_1] ---D---> [h_2]
# On a donc :
#     [h_0] ---A---> [h_1] ---C---> [h_2]
#     [h_0] ---A---> [h_1] ---D---> [h_2]
#     [h_0] ---B---> [h_1] ---C---> [h_2]
#     [h_0] ---B---> [h_1] ---D---> [h_2]
# Partant de l'état interne h_0, on a obtenu 4 séquences de 4 blocs qui
# aboutissent au même état interne h_2 : AC, AD, BC, BD.

# Concrètement, h_0 est l'état interne obtenu après avoir traité le préfixe.
# Pour que l'utilitaire de recherche de collision cherche une collision à partir
# de h_1, il faut lui donner un nouveau préfixe qui aboutisse à h_1. On peut lui
# donner, par exemple, (Prefix || A).  Une fois qu'on a obtenu la 4-collision,
# on peut rajouter "h4ckm0d3" à la fin des 4 messages qui collisionnent.


import binascii


def custom_md5_padding(message):
    """
    Ajoute un padding personnalisé à un message MD5.
    """
    # Convertir le message en bytes
    if isinstance(message, str):
        message = message.encode('ascii')

    # Longueur originale du message en bits
    original_bit_len = len(message) * 8

    # Ajouter le bit '1' à la fin du message
    message += b'\x80'

    # Ajouter des bits '0' (sous forme de bytes '\x00') jusqu'à atteindre une longueur multiple de 64 octets - 8 octets pour la longueur
    while (len(message) + 8) % 64 != 0:
        message += b'\x00'

    # Ajouter la longueur du message original sous forme de 64 bits (big-endian pour l'exemple)
    message += original_bit_len.to_bytes(8, 'big')

    # Convertir le message paddé en une représentation hexadécimale
    hex_representation = message.hex()

    # Remplacer '00' par 'f' pour simuler votre exemple (sauf pour les 8 derniers octets représentant la longueur)
    hex_representation = hex_representation[:-16] + \
        hex_representation[-16:].replace('00', 'f')

    return hex_representation


def write_prefix_file(message, file_path):
    """
    Écrit le message dans le fichier spécifié avec un padding MD5 personnalisé.
    """
    padded_hex = custom_md5_padding(message)
    with open(file_path, 'w') as f:
        f.write(message + padded_hex[len(message)*2:])


def binary_to_hex(file_path):
    """
    Lit les données binaires d'un fichier et les convertit en hexadécimal.
    """
    with open(file_path, 'rb') as f:
        binary_data = f.read()
    return binascii.hexlify(binary_data)


def read_file(file_path):
    with open(file_path, 'r') as f:
        prefixe = f.read()
    return prefixe


def construct_keys(prefixe, suffix, key1, key2, key3, key4):
    """
    Construit des clés en concaténant le préfixe, les parties de la clé et le suffixe.
    """
    # Convertit les données hexadécimales en chaînes de caractères
    key1 = key1.decode('utf-8')
    key2 = key2.decode('utf-8')
    key3 = key3.decode('utf-8')
    key4 = key4.decode('utf-8')

    # Affiche les clés construites
    print(prefixe + key1 + key3 + suffix)
    print(prefixe + key1 + key4 + suffix)
    print(prefixe + key2 + key3 + suffix)
    print(prefixe + key2 + key4 + suffix)


def main():
    """
    Fonction principale.
    """
    # Écriture du préfixe dans le fichier
    prefix_message = "Yannick"
    prefix_file_path = 'prefixe'
    write_prefix_file(prefix_message, prefix_file_path)

    # Construction du suffixe
    suffix = "h4ckm0d3"
    suffix_hex = suffix.encode('utf-8').hex()

    # Lecture des clés depuis les fichiers binaires
    key1 = binary_to_hex('key1')
    key2 = binary_to_hex('key2')
    key3 = binary_to_hex('key3')
    key4 = binary_to_hex('key4')

    # Construction et affichage des clés
    prefixe = read_file(prefix_file_path).encode('utf-8').hex()
    construct_keys(prefixe, suffix_hex, key1, key2, key3, key4)


if __name__ == "__main__":
    main()
