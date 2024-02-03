# Lancement du jeu

# Tutoriel
```bash
telnet m1.tme-crypto.fr 1337
```

## TOME I

```
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

```
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

```
>>> lire tome III
```

```
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

```
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

```
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

```
>>> lire sript d'exemple
```

```py
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

```
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

## Symétrique : chiffrement déchiffrement avec clé symétrique

### Déchiffrement avec clé symétrique

```bash
openssl enc -d -base64 -aes-128-cbc -pbkdf2 -pass pass:"bar" -in foo
```

### Chiffrement avec clé symétrique

```bash
openssl enc -aes-128-cbc -pbkdf2 -salt -base64 -pass pass:"bar" -in <fichier à chiffrer> -out <fichier chiffré>
```

## Génération de paire clé (privé/publique)

privée:
```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:1024 # ou autre taille de clé ici 1024 bits
```
publique:
```bash
openssl pkey -in <fichier contenant la clef secrète> -pubout
```

## Asymétrique : chiffrement avec clé publique et déchiffrement avec clé privée

### Chiffrement avec clé publique

```bash
openssl pkeyutl -encrypt -hexdump -pubin -inkey <clef publique> -in <message en clair> -out <le message chiffré>
```

### Déchiffrement avec clé privé

```bash
openssl pkeyutl -decrypt -hexdump -inkey <clef privée> -in <message chiffré> -out <message déchiffré>
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





