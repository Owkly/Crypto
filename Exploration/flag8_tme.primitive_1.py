from sympy import isprime, nextprime

"""
But     : produire (p, g) avec p premier (a <= p < b) et g d'ordre p-1 modulo p.
          Il faut également fournir la factorisation de p-1.
          p-1 doit être un multiple de q.
"""

def find_p_and_factorization(a, b, q):
    """
    Recherche de p et de la factorisation de (p-1)//q
    tel que (a <= p < b) et (p - 1) soit un multiple de q
    paramètres: a -> borne inférieure
                b -> borne supérieure
                q -> facteur
    """
    # Calcul de l'intervalle pour r
    lower_r = (a - 1) // (2 * q)
    upper_r = (b - 1) // (2 * q)
    # Générer r dans l'intervalle et tester p pour la primalité
    r = nextprime(lower_r)

    i = 0
    while r < upper_r:
        i += 1
        print("Tentative", i)
        p = 2 * q * r + 1
        if isprime(p):
            return p, r
        r = nextprime(r)

def find_generator(p, q, r):
    """
    Recherche d'un générateur g
    paramètres: p -> nombre premier
                q -> facteur
                r -> facteur
    """
    phi = p - 1
    factors = [2, q, r]

    for g in range(2, p):
        if all(pow(g, phi // factor, p) != 1 for factor in factors):
            return g
    return None


if __name__ == "__main__":
    # données
    a_hex = "e1bf40dacd46c02f4f80142bf16a5dce78316f53fb0022f25f753af2ff7255e5ef820ae72bbcb7c1a8c716323aa57162ef0c7d94318c7eaab9ecd66b748127f7026f5e0a34b6d44178d5ec58ecf40a72fa145ebc023ff464777966972cf646d15e59493d9f5ff8ab26bb63d6d5f8d617413434e61c7f34d01050ca6a804688f67340fbc78046bb9772e304479e4e89e00f793d6bd95617a6f64ce4b1cf3a3c6bac7b1adda4cf0ad4a9cbae68cbeeeb48bfabe1f5f0a73589bfa22ea4a14cdef4e541aef75db12202494ca2b6edd760fe63959f1b85edd2ee3a376c9fa17492543c983c8ec20217e0ff93889cc2be35c807be6ba17e3469d5c057335da002e791"
    q_hex = "f11d92ca48f6231885ef109e402dfbf2c5655e02653b6efd0aea6852b53e9afd9bc3bb52727b319c3a1580c36f0dc03b"
    a = int(a_hex, 16)
    b = a + 2**1950
    q = int(q_hex, 16)

    # Recherche de p et de la factorisation de (p-1)//q
    p, r = find_p_and_factorization(a, b, q)
    if p is not None:
        print(f"\nFactorisation de (p-1)/q:\n2, {r}")
    else:
        print("Aucun p valide trouvé dans l'intervalle.")

    # Recherche d'un générateur g
    g = find_generator(p, q, r)
    if g is not None:
        print(f"\nTrouvé g: \n{g}")
    else:
        print("Aucun générateur valide trouvé.")
