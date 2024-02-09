import random
from sympy import isprime

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


def generate_p(a, b, q):
    """
    Trouver p premier tel que (a <= p < b) et (p - 1) soit un multiple de q
    paramètres: a -> borne inférieure
                b -> borne supérieure
                q -> facteur
    """
    # On recherche le premier nombre multiple de q dans l'intervalle [a, b) et le définir comme point de départ
    r = (a - 1) % q
    if r != 0:
        step = q - r
    else:
        step = 0
    start = a + step

    # Et on parcours les nombres dans l'intervalle [a, b) par pas de q à partir de ce point de départ jusqu'à trouver un nombre premier
    for p in range(start, b, q):
        if isprime(p):
            return p


def generate_g(p, q):
    """
    Trouver g d'ordre q modulo p
    (g**q == 1 mod p)
    paramètres: p -> nombre premier
                q -> facteur
    """
    while True:
        x = random.randint(2, p - 2)
        g = pow(x, (p - 1) // q, p)
        if g != 1:
            return g


if __name__ == "__main__":
    # Convertir les chaînes hexadécimales en entiers
    a_hex = "616bb89a84d090555827fad97e08aa9877dc4effd0190b1871659b0a040f3a32d00b217a3b9b63705de954cbaf1cc52741332b5dd778cfdf09af2598d462554cda2da4c9ef4bde92676a85efb4862ca6950ab969ae09dc0cbf8b5a366a19f28794aa95bc777a2c49df456863c28a852f4653875d2f71388884cd82211a1c008ef04c3101250c974700b342a5a48f3c4503570431d698980c38fd456cd482ac8ea6daa3ada601557f95d9222987914ac88a5c725f956c73d3aab8a04703d5875e5266e4a8aaccda93b92a4b8709bb672687140e592dadfa880c5397993c83d8833f4179016b7f4c92f566c08fdd898d4d8707b4bd77de369a11cffa59941aaf4e"
    a = int(a_hex, 16)
    b = a + 2**1950
    q = int("9fb0ea7e13fd9340cfb9fa7ce8f1f8ab5094d4e47fc850af19ab7d50b389775f", 16)

    # Générer p
    p = generate_p(a, b, q)
    assert a <= p < b, f"Erreur: p ({p}) n'est pas dans l'intervalle [a, b)"
    assert (p - 1) % q == 0, f"Erreur: p ({p}) - 1 n'est pas un multiple de q ({q})"

    # Générer g
    g = generate_g(p, q)
    assert pow(g, q, p) == 1, "Erreur: g**q == 1 mod p"

    print(f"p premier tel que (a <= p < b) et (p - 1) soit un multiple de q: \n{p}")
    print(f"g tel que g**q == 1 mod p: \n{g}")
