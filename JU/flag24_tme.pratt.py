# TME #3 : certificat de primalité
# ================================

# Difficulté : ****


# But     : produire un certificat de primalité de Pratt pour un entier p premier
#           (a <= p < b).  Un tel certificat pour p est un dictionnaire composé de :
#           - p   : le nombre dont il s'agit de prouver la primalité
#           - g   : un élément d'ordre p-1 modulo p
#           - pm1 : la liste des certificats des facteurs premiers de p-1

#           Si p < 1024, alors il n'est pas nécessaire de fournir g et pm1.
#           (la définition récursive est donc bien fondée).

# a = 19534b5f657686154a5770dd99c15817be459cc9c871498e7e97fcfc77254dcd84efeb85ee41dc6dd3bba0fda079ba2dbedafb73d3cfd65796ac837a157b3bac52b500818a679762534474be94254bf8175a8addb41df63536f878003b0975d94bea68a060b7dcbb043726a64a96d8fe749ce87ac747cd5589afc6ddeb9495e2
# b = a + 2**960

# Format : dictionnaire JSON

#                     certificat : 


                                               
import random
from sympy import factorint
import json

# Définition des fonctions utilisées pour le certificat de primalité de Pratt

def multiplyList(myList):
    """ Multiplie tous les éléments d'une liste entre eux. """
    result = 1
    for x in myList:
        result *= x
    return result

def miller_rabin(n, k):
    """ Test de primalité de Miller-Rabin.
    n: entier à tester.
    k: nombre de tours pour augmenter la précision du test.
    Retourne True si n est probablement premier, sinon False. 
    """
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def bit_size(int):
    """ 
    Calcule la taille en bits d'un entier. 
    """
    return (int.bit_length() + 7) // 8

def find_gen(p, list_div):
    """ 
    Trouve un générateur g pour le nombre premier p.
    Ce générateur g doit être tel que g^(p-1)/q ≠ 1 mod p pour chaque diviseur q de p-1. 
    """
    while True:
        g = random.randrange(2, p-1)
        if all(pow(g, (p-1)//pi, p) != 1 for pi in list_div):
            return g

def rec_cert_pratt(list_div):
    """ 
    Construit récursivement le certificat de Pratt pour les diviseurs de p-1. 
    """
    res = []
    for div in list_div:
        cert_div = {'p': div}
        if div >= 1024:
            diviseur = []
            factors = factorint(div - 1)
            for d, exp in factors.items():
                diviseur.extend([d] * exp)
            cert_div['g'] = find_gen(div, diviseur)
            cert_div['pm1'] = rec_cert_pratt(diviseur)
        res.append(cert_div)
    return res

def main():
    """ 
    Fonction principale qui génère le certificat de primalité de Pratt. 
    """
    
    a = int("19534b5f657686154a5770dd99c15817be459cc9c871498e7e97fcfc77254dcd84efeb85ee41dc6dd3bba0fda079ba2dbedafb73d3cfd65796ac837a157b3bac52b500818a679762534474be94254bf8175a8addb41df63536f878003b0975d94bea68a060b7dcbb043726a64a96d8fe749ce87ac747cd5589afc6ddeb9495e2", 16)
    b = a + 2**960

    liste_pk = [2]
    Q_prime = 2
    c = 20000
    len_b = bit_size(b)
    maxQprim = (b-a) // (c * len_b**2)

    while bit_size(maxQprim) != bit_size(Q_prime):
        pi = random.randrange(2, min(pow(2, 160), pow(2, 8 * (bit_size(maxQprim) - bit_size(Q_prime)))))
        if miller_rabin(pi, 10):
            Q_prime *= pi
            liste_pk.append(pi)

    p_k = random.randrange(a//Q_prime, b//Q_prime)
    while not miller_rabin(p_k, 1) or not miller_rabin(Q_prime*p_k+1, 1):
        p_k = random.randrange(a//Q_prime, b//Q_prime)

    liste_pk.append(p_k)
    p = multiplyList(liste_pk) + 1
    g = find_gen(p, liste_pk)

    cert_pratt = {'p': p, 'g': g, 'pm1': rec_cert_pratt(liste_pk)}

    with open('flag24_tme.pratt.json', 'w') as f:
        json.dump(cert_pratt, f)

    print("Certificat généré et sauvegardé dans flag24_tme.pratt.json")

if __name__ == '__main__':
    main()
