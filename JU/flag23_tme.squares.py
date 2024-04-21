def mods(a, n):
    """ Normalise a pour être entre -n/2 et n/2. """
    a = a % n
    if 2 * a > n:
        a -= n
    return a


def powmods(a, r, n):
    """ Réalise l'exponentiation modulaire avec normalisation. """
    out = 1
    while r > 0:
        if (r % 2) == 1:
            r -= 1
            out = mods(out * a, n)
        r //= 2
        a = mods(a * a, n)
    return out


def quos(a, n):
    """ Calcule le quotient de la division de a par n, ajusté par mods. """
    return (a - mods(a, n)) // n


def grem(w, z):
    """ Calcul du reste dans les entiers gaussiens lors de la division de w par z. """
    (w0, w1) = w
    (z0, z1) = z
    n = z0**2 + z1**2
    if n == 0:
        raise ValueError("Division par zéro")
    u0 = quos(w0 * z0 + w1 * z1, n)
    u1 = quos(w1 * z0 - w0 * z1, n)
    return (w0 - z0 * u0 + z1 * u1, w1 - z0 * u1 - z1 * u0)


def ggcd(w, z):
    """ Calcule le plus grand diviseur commun utilisant les entiers gaussiens. """
    while z != (0, 0):
        w, z = z, grem(w, z)
    return w


def root4(p):
    """ Calcule la racine 4-ième de 1 modulo p."""
    if p <= 1:
        return "trop petit"
    if (p % 4) != 1:
        return "pas congruent à 1"
    k = p//4
    j = 2
    while True:
        a = powmods(j, k, p)
        b = mods(a * a, p)
        if b == -1:
            return a
        if b != 1:
            return "pas premier"
        j += 1


def sq2(p):
    """ Décompose un nombre premier p en une somme de deux carrés. """
    a = root4(p)
    return ggcd((p, 0), (a, 1))


def main():
    p_hex = "d4817d5e5087276fb6e758b943f4106be8ef88f428f4942600cccf9bc13b7c8d51f40c6ab889794c9ca6754bd52d5e29ce460b1dcd5e48b025a44c1b99094aad8a8946d22373e06d0493344c0d2443982f0d1144f601b027b654ca213fe579b8cd9d9c19f21f9063a1e03aa124fb296fdbe9a2e43e90054b1bcd522ebdbac549"
    p_int = int(p_hex, 16)
    a, b = sq2(p_int)
    print(f"a = \n{a} \nb = \n{b}\n")


if __name__ == "__main__":
    main()
