# >>> use card
# La porte ne s'ouvre pas. Une lumière rouge est allumée sur le lecteur de badge.
# Le micro-écran LCD affiche "DEVICE DOES NOT CONTAIN A PUBLIC KEY".


# >>> use NFC
# Vous ne pouvez pas faire grand-chose avec, mais vous pourriez essayer
# d'utiliser un AUTRE objet dessus.

# >>> conseil NFC
# Votre carte d'étudiant doit pouvoir être lue par ce dispositif.

# >>> conseil NFC
# Avez-vous lu le memento qui est dans la pièce à côté ?

# >>> conseil NFC
# Il vous faut produire une paire de clefs RSA dont la clef publique, 
# encodée en base64, contient "+++ATRIUM+++".  Sans trop rentrer dans les
# détails, la clef publique contient n et e, plus quelques octets de bourrage
# à cause de la sérialisation asn.1 (c'est assez compliqué).  Il faut donc
# que la "chaîne promotionnelle" apparaisse soit dans n soit dans e quand
# on représente le tout en base64.


# >>> conseil NFC
# Entre n et e, c'est e qui est plus facile à contrôler : en effet on peut
# le **choisir** librement lors de la création de la paire de clefs.  Mais
# attention !  Il doit être impair.


# >>> conseil NFC
# L'encodage en base64 complique le tout (ne pas hésiter à lire la page 
# wikipédia qui correspond).  En effet, chaque paquet de 6 bits est encodé en
# un caractère.  3 octets du départ (24 bits) sont donc représentés par 4
# caractères.  Si la "chaine promotionnelle" ne commence pas à une position
# qui est un multiple de 3 dans la clef de départ, alors elle sera "à cheval"
# sur des caractères ASCII différents, elle et n'apparaîtra pas correctement.
# Une solution potentielle consiste à ajouter un ou deux octets AVANT dans e.


# >>> conseil NFC
# C'est tout !


from Crypto.PublicKey import RSA
import base64

base64_string = "ee+++ATRIUM+++ed"

decoded_bytes = base64.b64decode(base64_string)
print(decoded_bytes)

decimal_value = int.from_bytes(decoded_bytes, byteorder='big')
print(decimal_value)

key = RSA.generate(bits=2048, randfunc=None, e=decimal_value)
# je sauvegarde les fichiers
with open('flag11_pkey.pem', 'wb') as f:
    f.write(key.publickey().export_key('PEM'))

with open('flag11_skey.pem', 'wb') as f:
    f.write(key.export_key('PEM'))