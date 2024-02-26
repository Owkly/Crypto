# >>> conseil laptop
# En résumé, ce laptop effectue (une des étapes) de la signature RSA, mais il
# n'accepte pas forcément de signer tout et n'importe quoi.


# >>> conseil laptop
# Pour commencer, pour obtenir une signature correcte (c.a.d. qui vérifie avec
# la clef publique en utilisant OpenSSL), il faut appliquer soi-même l'encodage
# PKCS#1 v1.5.  Ensuite, la programme va effectuer la dernière étape 
# (l'élévation à la puissance d modulo N, où d est la clef secrète). La spec 
# de la signature RSA PKCS#1 v1.5 se trouve à la bibliothèque.


# >>> conseil laptop
# Une bonne manière d'appréhender le problème, c'est de commencer par faire 
# signer n'importe quoi puis de vérifier que les signatures sont valides.


# >>> conseil laptop
# Conseil général pour la mise au point : essayer d'abord avec une paire de
# clef qu'on a fabriquée soi-même et pour laquelle on connaît tout plutôt que
# d'utiliser le serveur comme une boite noire qui dit ``NON''.


# >>> conseil laptop
# Ensuite, pour faire signer ce qui nous intéresse, on peut exploiter la
# ***malléabilité*** de RSA.


# >>> conseil laptop
# Concrètement :
# - on soumet (M * x**e) mod N, pour un x aléatoire.  Ceci "masque" M au serveur.
# - le serveur renvoie (M * x**e)**d == (M**d) * (x**ed) == x * M**d mod N.
# - il suffit d'éliminer le ``masque'' x (en multipliant par l'inverse de x
#   modulo N) et on obtient M**d mod N, c'est-à-dire la signature voulue.


# >>> conseil laptop
# C'est tout !
