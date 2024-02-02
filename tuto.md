# Lancement du jeu

# Tutoriel
```bash
telnet m1.tme-crypto.fr 1337
```

## TOME I

```bash
>>> lire chaîne de caractères
```

```
Une chaine de caractère est une séquence de caractères.  La façon dont
ces caractères sont représentés par des séquences de bits est decrite
par un système d'encodage.  Il en existe de nombreux, et ils sont bien
sûr tous incompatibles entre eux.  Certains ne permettent pas de
représenter tous les caractères.  Par exemple, l'encodage ISO-8859-1
(a.k.a.  latin-1) code les caractères sur un octet.  Il est bien adapté
au monde occidental, mais ne contient pas les signes asiatiques, par
exemple.  Le KOI8-R, lui, permet de représenter les caractères
cyrilliques, etc.

Le système unicode permet de représenter la plupart des caractères connus,
mais il n'est pas très compact (4 octets par caractères).  Représenter des
chaines de caractères comme des séquences de caractères unicode offre
l'avantage de faire disparaître tous ces ennuyeux problèmes d'encodage. C'est
le choix des concepteurs de Python.  Dans ce langage, une chaine de
caractère (un objet de type "str") est représentée en mémoire dans le système
unicode.

Il existe aussi en python un autre type de chaine, les objets de type
"bytes".  Il s'agit d'une simple séquence d'octets, comparable aux
tableaux de type char qu'on a dans le langage C.

>>> type("toto")
<class 'str'>

>>> type(bytes([0, 1, 2]))
<class 'bytes'>

Tout ceci a deux conséquences.


A) Traitement du texte
----------------------

Les programmeurs doivent se soucier de ces problèmes d'encodage
lorsqu'ils doivent transformer des chaines de caractères en séquences
d'octets, par exemple pour les écrire dans un fichier, les envoyer sur
le réseau, ou les transmettre à un autre programme (comme openssl...).
Par défaut dans UGLIX, les chaines unicodes sont encodées en UTF-8
lors de leur conversion en séquences d'octets.

Les chaines unicodes ont une méthode "encode", qui prend en argument
un encodage (la valeur par défaut est "utf-8").

>>> 'toto'.encode()
b'toto'

>>> 'aïlle'.encode()
b'a\xc3\xaflle'

Quand ils sont affichés, les objets de type byte sont préfixés par la
lettre 'b'.  Ils possèdent, eux, une méthode "decode", qui prend
aussi en argument un encodage (utf8 par défaut).

>>> b'\xc3\xa0 V\xc3\xa4\xc3\xafn\xc3\xb6'.decode()
'à Väïnö'

Une situation où l'encodage apparaît explicitement concerne l'utilisation de
OpenSSL.  Il est nécessaire d'encoder les chaines de caractères unicode avant
de les envoyer à openssl (lors du chiffrement), et il est nécessaire de les
décoder en sortie de openssl (lors du déchiffrement) pour récupérer de
l'unicode.


B) Traitement des données binaires
----------------------------------

Il est parfois nécessaire d'envoyer ou de recevoir des requêtes
contenant des données binaires, qui ne sont pas interprétables comme
des chaines de caractères (il y a en effet des séquences d'octets qui
sont des encodages invalides en UTF-8, et qui sont donc rejetées lors
du décodage).  Par exemple :

>>> s = bytes([5*i*i & 0xff for i in range(10)])
>>> s.decode()
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb4 in position 6: invalid start byte

Dans ce cas-là, il faudrait transmettre des objets de type bytes().  Le
petit problème, c'est que les bytes() ne sont pas forcément affichables 
sur un terminal conçu principalement pour afficher des caractères ASCII.
Pour contourner cette difficulté, il faut encoder les bytes() en
quelque chose qui soit du texte acceptable, pour en faire une str().
Dans UGLIX, on utilise généralement à cette fin deux encodages : en base64
(les séquences d'octets sont découpées en paquets de 6 bits, et chaque
paquet est converti en une lettre) ou bien en hexadécimal.

Pour ceci, on fait appel aux fonctions b64encode et b64decode du
module base64.  Voici un exemple

>>> import base64
>>> base64.b64encode(s)
b'AAUULVB9tPVAlQ=='

Notez qu'on récupère des "bytes".  Mais ceux-là, on peut les convertir
en texte sans douleur.

>>> b'AAUULVB9tPVAlQ=='.decode()
'AAUULVB9tPVAlQ=='

Les objets de type "bytes" ont une méthode .hex() qui fait
ce que son nom indique :

>>> s.hex()
'0005142d507db4f54095'

De plus, on peut convertir la représentation hexadécimale en bytes()
avec la "méthode de classe" bytes.fromhex() :

>>> bytes.fromhex('deadbeef')
b'\xde\xad\xbe\xef'


base64 : 6 bits par caractère ce qui permet de représenter 64 caractères


bytes = 1 octet = 8 bits
Unicode principe de faire correspondre un caractère à un nombre (id unique)

UTF-8 : encodage de caractères unicode en séquence d'octets (8 bits)
UTF-16 : encodage de caractères unicode en séquence de 16 bits
UTF-24 : encodage de caractères unicode en séquence de 24 bits
UTF-32 : encodage de caractères unicode en séquence de 32 bits

python : "str" = unicode
		 "char" = byte
C :      "char" = byte
```


## TOME II

```bash
>>> lire chiffrement symétrique
```

```
CHIFFREMENT SYMÉTRIQUE
======================

L'essentiel des tâches de chiffrement peut être réalisé avec la
bibliothèque OpenSSL (la version 1.0 est requise au minimum).

La plupart du temps, les utilisateurs d'UGLIX chiffrent leurs fichiers
avec un mécanisme à clef secrète et en utilisant un mot de passe.
OpenSSL se débrouille pour convertir ce mot de passe en une clef
secrète et un vecteur d'initialisation. De l'aléa est généralement
introduit dans ce processus.

Pour augmenter la portabilité, les utilisateurs d'UGLIX stockent
généralement les fichiers chiffrés en les encodant en base64.

Enfin, par défaut, les utilisateurs d'UGLIX sont invités à utiliser
l'AES-128 en mode CBC pour chiffrer leurs données.

Vous êtes invités à vous reporter à la documentation plus détaillée de
OpenSSL, en particulier en exécutant "man openssl", "openssl enc
help", ou bien en consultant la page du mode d'emploi de openssl
dédiée au chiffrement symétrique ("man openssl-enc").

Déchiffrer le fichier "foo" en utilisant le mot de passe "bar" peut
logiquement s'accomplir par la commande :

openssl enc -d -base64 -aes-128-cbc -pbkdf2 -pass pass:"bar" -in foo

Il est très pratique de pouvoir invoquer openssl depuis des programmes.
Pour cette raison, un autre script open-source est mis à la disposition
de la communauté. On le trouve dans le guide intitulé "script d'exemple".

Vous êtes invité à l'adapter à tous vos besoins.

    ⚠      Il existe plusieurs versions de OpenSSL. Ce serveur UGLIX utilise
   ⚠ ⚠     "OpenSSL 1.1.1d  10 Sep 2019". N'hésitez pas à vérifier avec la 
  ⚠ | ⚠    commande "openssl version". Il FAUT une version supérieure à 1.1.1 !
 ⚠  o  ⚠   Si vous avez la 1.1.0 (ou plus ancienne), l'option -pbkdf2 ne sera
⚠⚠⚠⚠⚠⚠⚠⚠⚠  pas reconnue.
    |      
    |      Attention, sur les versions récentes de MacOS, "openssl" est en fait
    |      LibreSSL (un fork). Et il est partiellement incompatible !

```


## Tome III

```bash
>>> lire chiffrement symétrique
```
[security engine] power.on:136:1|40294b7ff0ae55ea647d882de452b3de93b5226d6eff895f7abc1abcba5b89df


La plupart du temps, les utilisateurs d'UGLIX chiffrent leurs fichiers
avec un mécanisme à clef secrète et en utilisant un mot de passe.
OpenSSL se débrouille pour convertir ce mot de passe en une clef
secrète et un vecteur d'initialisation. De l'aléa est généralement
introduit dans ce processus.

Pour augmenter la portabilité, les utilisateurs d'UGLIX stockent
généralement les fichiers chiffrés en les encodant en base64.

Enfin, par défaut, les utilisateurs d'UGLIX sont invités à utiliser
l'AES-128 en mode CBC pour chiffrer leurs données.

Vous êtes invités à vous reporter à la documentation plus détaillée de
OpenSSL, en particulier en exécutant "man openssl", "openssl enc
help", ou bien en consultant la page du mode d'emploi de openssl
dédiée au chiffrement symétrique ("man openssl-enc").

Déchiffrer le fichier "foo" en utilisant le mot de passe "bar" peut
logiquement s'accomplir par la commande :

openssl enc -d -base64 -aes-128-cbc -pbkdf2 -pass pass:"bar" -in foo

Il est très pratique de pouvoir invoquer openssl depuis des programmes.
Pour cette raison, un autre script open-source est mis à la disposition
de la communauté. On le trouve dans le guide intitulé "script d'exemple".

Vous êtes invité à l'adapter à tous vos besoins.

    ⚠      Il existe plusieurs versions de OpenSSL. Ce serveur UGLIX utilise
   ⚠ ⚠     "OpenSSL 1.1.1d  10 Sep 2019". N'hésitez pas à vérifier avec la 
  ⚠ | ⚠    commande "openssl version". Il FAUT une version supérieure à 1.1.1 !
 ⚠  o  ⚠   Si vous avez la 1.1.0 (ou plus ancienne), l'option -pbkdf2 ne sera
⚠⚠⚠⚠⚠⚠⚠⚠⚠  pas reconnue.
    |      
    |      Attention, sur les versions récentes de MacOS, "openssl" est en fait
    |      LibreSSL (un fork). Et il est partiellement incompatible !

>>> lire tome III
GÉNÉRATION D'UNE PAIRE DE CLEFS
===============================

Openssl permet de générer des paires de clefs, avec la commande : 

    openssl genpkey <options>

Encore une fois, vous êtes encouragés à consulter "man genpkey" et 
la documentation de openssl.  Par défaut, le résultat est envoyé sur
la sortie standard.  Le résultat contient la paire de clefs, au format
PEM (c'est de l'ASCII) propre à openssl et un peu pénible à décoder à
la main. 

Par exemple, pour générer une paire de clefs RSA de 1024 bits :

    openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:1024


Une commande permet d'extraire la clef publique uniquement, pour la
communiquer à des tiers : 

    openssl pkey -in <fichier contenant la clef secrète> -pubout

```

## Tome IV

```bash 
>>> lire chiffrement à clef publique
```

```
>>> lire chiffrement à clef publique
CHIFFREMENT À CLEF PUBLIQUE
===========================

Openssl permet d'effectuer du chiffrement/déchiffrement asymétrique, avec
l'algorithme RSA.  Vous êtes invité à consulter la page de manuel
correspondante (man openssl-pkeyutl). 

L'usage d'openssl pour effectuer des opérations de (dé)chiffrement asymétrique
a deux limitations :

1) Le message clair DOIT être plus court que la clef.  Si ce n'est pas le cas,
   l'opération échoue avec un message "Public Key operation error, data too 
   large for key size".  Avec une clef de 2000 bits, vous avez droit à environ
   1800 bits de message.  C'est une limitation de l'algorithme lui-même.

2) Openssl ne prévoit pas d'encoder le résultat de l'opération de chiffrement
   en base64.  Par contre il y a une option pour l'encodage en... hexadécimal.

La commande essentielle pour le chiffrement :

   openssl pkeyutl -encrypt -hexdump -pubin -inkey <fichier contenant la clef publique>

Ceci attend un message sur l'entrée standard, et affichera son chiffrement sur
la sortie standard.  Pour déchiffrer, il faut fournir la clef secrète (et donc
retirer l'option  "-pubin")
```

## Tome V

```bash
>>> lire signature
```
```
SIGNATURES
==========

OpenSSL permet d'effectuer des signatures numériques et d'en vérifier avec
plusieurs algorithmes, dont RSA.
    
La solution la plus courante consiste à utiliser une fonction de hachage
cryptographique, et à signer l'empreinte du document à authentifier.  OpenSSL
peut accomplir ceci automatiquement avec la commande  "openssl dgst".  Vous
êtes invités à consulter la page de manuel correspondante
("man openssl-dgst").  Par défaut, avec une clef RSA, cela produit des
signatures PKCS#1 v1.5.  Voici les exemples les plus pertinents :
    

Production d'une signature
--------------------------

    openssl dgst -sha256 -sign secret_key.pem
    
Ceci attend les données à signer sur l'entrée standard, et envoie la
signature sur la sortie standard.  L'option -hex peut être utile.
    

Vérification d'une signature
----------------------------
    
    openssl dgst -sha256 -verify public_key.pem -signature signature.bin
    
Ceci attend sur l'entrée standard les données dont "signature.bin" contient
une signature.
    
Les signatures sont des données binaires, donc on doit généralement les
encoder, par exemple en hexadecimal avant de pouvoir les transmettre sans
douleur.  L'option -hex ne permet pas de vérifier des signatures données en
hexadécimal.


REMARQUE IMPORTANTE
-------------------
Une signature n'est valide que si les **mêmes** données (prétendument signées)
sont fournies lors de la production et de la vérification de la signature.  Or,
lorsque l'une des deux étapes sont effectuées par un serveur distant, on ne 
contrôle pas forcément les données en question.  Il faut savoir que la **majorité** 
des éditeurs de texte (vi, nano, gedit, kate, emacs, ...) ajoutent un caractère "\n" 
invisible à la fin de tous les fichiers.  Il est généralement impossible de 
l'empêcher, or ceci peut entrainer l'invalidité des signatures.  On peut vérifier
si c'est le cas en faisant passer le fichier à travers le programme "xxd".  Si on
voit apparaître un octet 0x0a à la fin, c'est le "\n" maudit.
    
Une solution potentielle pour écrire un fichier sans caractère excédentaire 
consiste à utiliser un petit programme du type :
>>> # cet exemple est en python
>>> f = open(FILENAME, "w")
>>> f.write("contenu important")   # <--- pas de \n à la fin
>>> f.close()

L'autre solution consiste à écrire une fonction qui invoque directement OpenSSL,
par exemple avec la fonction "subprocess.run()" de la librairie standard de python.

```

## Tome VI

```bash
>>> lire sript d'exemple
```

```
>>> lire sript d'exemple
import subprocess

# ce script suppose qu'il a affaire à OpenSSL v1.1.1
# vérifier avec "openssl version" en cas de doute.
# attention à MacOS, qui fournit à la place LibreSSL.

# en cas de problème, cette exception est déclenchée
class OpensslError(Exception):
    pass

# Il vaut mieux être conscient de la différence entre str() et bytes()

def encrypt(plaintext, passphrase, cipher='aes-128-cbc'):
    """invoke the OpenSSL library (though the openssl executable which must be
       present on your system) to encrypt content using a symmetric cipher.

       The passphrase is an str object (a unicode string)
       The plaintext is str() or bytes()
       The output is bytes()

       # encryption use
       >>> message = "texte avec caractères accentués"
       >>> c = encrypt(message, 'foobar')       
    """
    # prépare les arguments à envoyer à openssl
    pass_arg = 'pass:{}'.format(passphrase)
    args = ['openssl', 'enc', '-' + cipher, '-base64', '-pass', pass_arg, '-pbkdf2']
    
    # si plaintext est de stype str, on est obligé de l'encoder en bytes pour
    # pouvoir l'envoyer dans le pipeline vers openssl
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    
    # ouvre le pipeline vers openssl. envoie plaintext sur le stdin de openssl, récupère stdout et stderr
    #    affiche la commande invoquée
    #    print('debug : {0}'.format(' '.join(args)))
    result = subprocess.run(args, input=plaintext, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # si un message d'erreur est présent sur stderr, on arrête tout
    # attention, sur stderr on récupère des bytes(), donc on convertit
    error_message = result.stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    # OK, openssl a envoyé le chiffré sur stdout, en base64.
    # On récupère des bytes, donc on en fait une chaine unicode
    return result.stdout.decode()

# TODO :
# - implement the decrypt() method
# - write a KeyPair class
# - write a PublicKey class
# - etc.
```

## Rapport d'activité

```bash
>>> lire rapport d'activité
```
```
COMMENT FUIR UNE FLOTTE DE DRONES TUEURS ?
==========================================
M. Latapy, C. Magnien, L. Tabourier (équipe ComplexNetworks, 2022)

Résumé opérationnel
-------------------
- Face à des drones qui utilisent des algorithmes simples, 
  la plupart des fuyards inexpérimentés sont rattrapés
- La compréhension des algorithmes utilisés par les drones 
  augmente les chances de survie
- Un entrainement intensif dans une simulation que nous avons
  construite permet une survie avec probabilité proche de 
                           [--------REDACTED--------]

Remerciements
-------------
Ces travaux ont reçu le soutien financier (défiscalisé) des entreprises 
                           [--------REDACTED--------]
leaders mondiaux de la production de drones militarisés.

[vous sautez une dizaine de pages de blabla]

Retro-conception des algorithmes des drones
-------------------------------------------
- Les drones peuvent aller tout droit et tourner à 90°
- Ils ne peuvent pas faire demi-tour
                           [--------REDACTED--------]
- Les drones visent un emplacement donné, et quand ils ont un
  choix à effectuer, ils minimisent la distance euclidienne
- Les drones de type B se dirigent vers la cible
- Les drones de type P se dirigent 4 intervalles DEVANT la cible
- Les drones de type C visent la cible, sauf si celle-ci est proche. Alors
                           [--------REDACTED--------]
- Les drones de type K implantent l'algorithme suivant: 
                           [--------REDACTED--------]
                           [--------REDACTED--------]
                           [--------REDACTED--------]
- Nous n'avons pas réussi à confirmer l'existence de drones de type
                           [--------REDACTED--------]

[...]

On ne sait jamais, ça pourrait être utile dans le futur proche.
```





























# Commandes

## Asymétrique : chiffrement avec clé publique et déchiffrement avec clé privée

### Chiffrement avec clé publique

```bash
openssl pkeyutl -encrypt -hexdump -pubin -inkey <clef publique> -in <message en clair> -out <le message chiffré>
```

### Déchiffrement avec clé privé

```bash
openssl pkeyutl -decrypt -hexdump -inkey <clef privée> -in <message chiffré> -out <message déchiffré>
```

## Symétrique : chiffrement avec clé symétrique et déchiffrement avec clé symétrique

### Déchiffrement avec clé symétrique

```bash
openssl enc -d -base64 -aes-128-cbc -pbkdf2 -pass pass:"bar" -in foo
```

### Chiffrement avec clé symétrique

```bash
openssl enc -aes-128-cbc -pbkdf2 -salt -base64 -pass pass:"bar" -in <fichier à chiffrer> -out <fichier chiffré>
```

## Génération de paire clé (privé/publique)

```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048
openssl pkey -in <ficher contenant la clé privée> -pubout
```


## Signature


### créer un message signé

```bash
openssl dgst -sha256 -sign secret.key.pem -in <fichier encrypté> // -out <fichier contenant le message signé>
```
### lire le message signé

```bash
openssl dgst -sha256 -verify public.key.pem -signature <fichier contenant le message signé> -in <fichier encrypté> 
```





# Informations

flag 1 :

```bash
POST-IT PASSWORD: ISECR0XX

U2FsdGVkX1/51wqD7PnMSuRkwL8czQ1S/AznUxY9Z+K2tN2o5LBv1C2cM2fDGGD9
hQym6B/W3VH0TNEn7dU2Xg==
```

```bash
ba8d3381-a52f-4bab-bd83-d8c5a5d22227
```

```bash
[security engine] register:136:1|99b75790fbdbdd3d6aac5199f666744ad95939df184fe9d9bae148672833729d
```


flag 2 :

```bash
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvfOQoiH2KNKnDfJZmNAz
bTEY6+2bTDvwrphV7hkuxzOxtVb1hxhgFLdqGmvSdRkeEJjICgSmysVHPbs5A2RT
040U7EIXoxbd0/g1FpjDeEiSsxEZR2Lm/kCkUtU7F/UUUIz37DlxAiCvn5BvnYwf
2NZ2j0hDGCBHMKZj/SJga1KRkghdOZvtS1YwoN1dZpovZpOYRhttk2Nflx9qpiR7
vvW4FSNi8u63DbfaoKMDSWTXweJWLpEfoWfpLGLN16nCy0v7RvqfE0J2dtJLakAP
lbsm8NI0epwTs9CZmBmCbw7a3XauHqwGXcQjYltF0zwzx3fpxWDqN7ayznDB8kNt
mwIDAQAB
-----END PUBLIC KEY-----
```
    
```bash
6f5ed31adbe2f44588c408df5d81cc873cf1cbfee9b63b33fe16575694d51f6f9f5abbdd2c41c0a084ebaf5b180d200b4ef5986bcdbfaba1187975e1890beb40cb8185e86c4949d34a782bd420a4be4fd5d2d0d8c2a24a545532bae60bc2a633a610af15a3bcc1723cc1c5b720746f03321ea75c44cdba95897eb44e6674d10659b8afd061684eaaa133572a953bb610a12c6a4e5f5eec46e35df22ef784da54bc28df2781004e1bb66ddc0ef6ac4adb1913e2cb2de50e9ba64c1bd434fa45a425a48303f510f6850d3f8969e4d8f0b6d6491ffd411c46a55fa8f0b31cb30b19444e4f998bd3ecc15fb7fe1a0c8056747ebcb8553ae7354e344d8bc6becc1c55
```

```bash
[security engine]  pki.tutorial:136:1|78d578987ec1b855d24acd949d3e539c0e014982e4050cfb0add6e9dea3e40ce
```


flag 3 :

```bash
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDmk+IkW+xOkSx2
obubQHLTG+RFgduwSLPWXV2FDVcMus4Jbl6UuviigrzSo7ZQlx5Z2DjRmigOKgjD
c2xVxVh7xdwwnmMrqB+RdZ/yTGLCMYoomuxGX7Oxo+gPc9DMDZHVPVxxMDCalX1i
q4l6pcgO7pVwU9mKbkozJXusLBos1DbQXATz2nmGzihhmtp0psDFs7AdBguFMaY6
H98CTtJTxeraXcG+OLLeqbmplZOnz/HXUbU0P5UMv2wnmtL43JKrU596tMkLkZs1
QM+5TMzfBC3f62Xmmd334HI0kgTIoW7XqcM2CvRuwRMqUhu5HAaFl1tcLr3bcFlx
jazwPaT3AgMBAAECggEAGhNkUi9RGIuDZ0EgGc0ejzBKzu+CHDwElnwFjPv2ubpQ
fbGNIa3JW3uEhh+8iP2mEYwJ1O5llEB9sDjX6hVAzfKQ1bC7z16af1U5iunHi2WV
1cS7brP4+uBp6IF0/faU5PQlBano/TplrShwCj5AUyv5G3RoGCcj3gfhphVwulvo
iQpwAAIy1X2/sWtJrHA6gWoJw3sj6AZBXm0mMhvWWGYkP1G6gw4ItVp4LC72Wm49
/b+4/saXhLDRSqvTFYZcy3SvX4PxwkGm02JFQw/EhcY1ZLKqrFwJAtDxA7t2vl5g
P7WohGuN9NaWWfYsCrteos24Ii7sZ9m864zEfDOA2QKBgQDxlro0QGMpzhMm+sD3
OqZWsT7b6OruEQRb5uYcAnzMBbpIvvBIX+E1pMGZ1YZa0jZOH99I7h5SWFecBW8k
ix1s8iFJL3zA1xGbPAaDyBtravF27XDSWK8Sny6lW84pn7e646bJbHjPBXallsg5
j8tSonmoeOJ3CrRS2GM5Rmt6WQKBgQD0VQG3eIPfWnuU/UKcyjIwlOUvM2+JdSNz
KdhRTIjeWaJmNuxMAaq5Qx9+FdIZwFHU5zWsn6ybEWDI2IITnxuEGHGjpCsElq+G
fe47hhSa7ZR/EC6S0/5U6SneyOTuCs5tx8SWRbVdZ+Pr2zFjtd2DZyvCVL7hW/bF
QRR7ii6PzwKBgQCJXqx4Y5g/QCdRxcmNirLknppgjxtuzQxOeYekq6FsnWEkVjXo
4WP8jbdsEqb344nveF4NaSCisAr483oULGpJ9ZAJvk/Qkzo2q7YEnvdAaCnu9upt
IPJDw3HRotcigegGA8ZlyCEVjkS9uXQWjvYNAcftjPcwu0x3wwUAn1Mj2QKBgGpx
SiEq4JCCc8pRlx6FO95MT5gDmXjRzlLSjQnGBO6RMB3FmaX3J/Az3NlqGjDbxwqw
e4KrwV+A76AwKmLv8uXWXFOFJrSGDQvTeuD1pa5lCEdevlt6/ZbySSpkbM+DZ7EN
0YgB8GQz6WiMAnVE+q7PWJH9p3a4QMZodsrnRSejAoGATboYM7LqBz78Ko9mtmwc
YLTGvzMZJbmuDeOgmkPdYD6exju6HIOkDy1ZDPd4pUQS/R6x+HcDicABbVcsTPFS
ddsKwb4i9dxfSd5i7ubPQLCC+hlfuwrKFv3bISOVcdUg2c8yBDnVzEoIDwA6g3ua
Gsa0X9vt8yh420P0mkhkwtU=
-----END PRIVATE KEY-----
```
    
```bash
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5pPiJFvsTpEsdqG7m0By
0xvkRYHbsEiz1l1dhQ1XDLrOCW5elLr4ooK80qO2UJceWdg40ZooDioIw3NsVcVY
e8XcMJ5jK6gfkXWf8kxiwjGKKJrsRl+zsaPoD3PQzA2R1T1ccTAwmpV9YquJeqXI
Du6VcFPZim5KMyV7rCwaLNQ20FwE89p5hs4oYZradKbAxbOwHQYLhTGmOh/fAk7S
U8Xq2l3Bvjiy3qm5qZWTp8/x11G1ND+VDL9sJ5rS+NySq1OferTJC5GbNUDPuUzM
3wQt3+tl5pnd9+ByNJIEyKFu16nDNgr0bsETKlIbuRwGhZdbXC6923BZcY2s8D2k
9wIDAQAB
-----END PUBLIC KEY-----
```

```bash
[security engine] pki.upload:136:1|63ce4e0e806c62dbd452054e03666ddb18cfa88833ef4950701dab7cb0fb0fb8
```

flag 4 :

```bash
SHA2-256(stdin)= 8d6d32705060bc1014a674e7ee8582e2daa9c77505a7f1b4c5ddab5ec5ff21ed7436bd9f0802da51525d4bc3014bec4f65006da627bcdc46c5d67bbf568182a97ca00185fc86dc2fdbd59da9ff53649c657216c23ae1f26cb5606b076b9b57b1b883ae95d34e0553445424ffef52185df4ffc1e9481075dd4247ce89b1acb5613fb13cce9650d6468979bb4c596bab3db64a63f44a41f3db5da05d63fa7cd5bad13dc54005cc6d977c324b8960a80f7538a91bfe2f632a7a2dcc56ea6942368fdee3a5e50fd94d9cfa6c5e2e797440dfd447f649778827712a7a971d195fd7be1b6b63ff95c77a665547162b09655f2137bc76b4cd1a50dd83b4ac2366ee6342
```

```bash
SHA2-256(stdin)= d58892b2769beaa330b7e7ac442b5064806ed8b8b6871f1fba69e37687f6afffddbd3939bad1600f2a80caf4959e009d6cee189d514ff1fc2e36b681c3f8d1d56a3263bbd2ce1d9a30e2c096c1fb341b4c4ff8f044551016c08cdee6ce9b755e48aee78299d6e10658346d366ff804378ffa628e040aefd8511082f51ccfa9cc01dfa785913962fb5d9f4d43379686263f1219f51e0af3a22b6a888604d2b5db0c6978b6e3356f8bf6134f3d93c33b2c52f10fb2eb84e8e66a32ba6e5d78a7100571996522297e9fb79f123aa8a7b5df49f5ce27f66686801d1397836291b0bcf39c6a3d3dac0cd80047d96f751611016a1f770c705554c8c57f0d2ccdb8c109
```

```bash
[security engine] power.on:136:1|40294b7ff0ae55ea647d882de452b3de93b5226d6eff895f7abc1abcba5b89df
```