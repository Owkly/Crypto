import random
from sympy import isprime,  primerange


"""
	a, b, q donnés
 
	But: produire (p, g) avec p premier (a <= p < b)
			et g d'ordre q modulo p


>>> conseil #1
Pour que g puisse être d'ordre q, il faut que p-1 soit un multiple de q.
Il faut donc fabriquer p en vérifiant que
        1 + q*(nombre aléatoire pair de la bonne taille)
est bien un nombre premier.


>>> conseil #1
Pour trouver g, ce qu'il ne faut PAS faire, c'est essayer des valeurs aléatoires.
Ça n'a aucune chance de marcher.  Mais il y a un moyen simple de produire des 
nombres qui sont d'ordre q, s'ils sont différents de 1.


>>> conseil #1
Le truc consiste à choisir un nombre x aléatoirement, puis à calculer
        g := x ** ((p-1) // q)     [modulo p]
Si g == 1, recommencer (c'est très improbable).
Sinon, on a :
        g ** q == x ** (p-1)       [modulo p]
               == 1                (d'après le petit théorème de Fermat)
"""



# Trouver p premier entre [a, b) tel que p - 1 soit un multiple de q
def generate_p(a, b, q):
    # Trouver le premier nombre >= a qui est congruent à 1 modulo q
    start = a + ((q - (a - 1) % q) % q)

    # Et on parcours les nombres de ce point de départ en sautant de q en q
    for p in range(start, b, q):
        if isprime(p):
            return p

# Trouver g d'ordre q modulo p
def generate_g(p, q):
    while True:
        x = random.randint(2, p - 2)
        g = pow(x, (p - 1) // q, p)
        if g != 1:
            return g


if __name__ == "__main__":
    # Convertir les chaînes hexadécimales en entiers
    a_hex = "a0a64ff1f77fbe373def145d423ca0bee489c935be910910e8307928dcfcc8430710681bd8f9b01535f11aa5af864c65fac2a39da810c48597e841538dc239efc0e69c5853c97a3112d0d5469d2cb870aa87a8682af0edec559aac957cd4fa8420c03dd5ac3e77e31d20f0f3f2e8307d645b8c911d261ead8d251adbf4cd91cc46b2533e11f18debf6fbe4ae2f24c15bb63725307f53a3094114818e3caf356d9c1e8be32447c2586d64fe81d57d09d0957507593e643cf0eafd4313b76dbe2098f156d761d770bb30d63f2ba5b3be1f7a3e72745293b89f77aebffb2e80c52bad9abe050254b194e2d85c383b84de11a3d97372d583507a8f10dbd186fbab05"
    a = int(a_hex, 16)
    b = a + 2**1950
    q = int("fd882a1e0a2b273de5b2b94774a2ab8931c7922eb55c53e4b825accfd7fa71d3", 16)

    # Générer p
    p = generate_p(a, b, q)
    assert a <= p < b, f"Erreur: p ({p}) n'est pas dans l'intervalle [a, b)"
    assert (
        p - 1) % q == 0, f"Erreur: p ({p}) - 1 n'est pas un multiple de q ({q})"

    # Générer g
    g = generate_g(p, q)
    assert pow(g, q, p) == 1, "Erreur: g**q == 1 mod p"

    print(f"p premier tel que (a <= p < b) et (p - 1) soit un multiple de q: \n{p}")
    print(f"g tel que g**q == 1 mod p: \n{g}")
