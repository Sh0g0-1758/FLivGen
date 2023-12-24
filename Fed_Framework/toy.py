import numpy as np
from numpy.polynomial import polynomial as poly

pt = 29
size = 2
t = 100
modulus = 2**4

import numpy as np
from numpy.polynomial import polynomial as poly

def polymul(x, y, modulus, poly_mod):
    """Add two polynoms
    Args:
        x, y: two polynoms to be added.
        modulus: coefficient modulus.
        poly_mod: polynomial modulus.
    Returns:
        A polynomial in Z_modulus[X]/(poly_mod).
    """
    return np.int64(
        np.round(poly.polydiv(poly.polymul(x, y) % modulus, poly_mod)[1] % modulus)
    )


def polyadd(x, y, modulus, poly_mod):
    """Multiply two polynoms
    Args:
        x, y: two polynoms to be multiplied.
        modulus: coefficient modulus.
        poly_mod: polynomial modulus.print(b)
print(a)
print(sk)
    Returns:
        A polynomial in Z_modulus[X]/(poly_mod).
    """
    return np.int64(
        np.round(poly.polydiv(poly.polyadd(x, y) % modulus, poly_mod)[1] % modulus)
    )

def gen_binary_poly(size):
    """Generates a polynomial with coeffecients in [0, 1]
    Args:
        size: number of coeffcients, size-1 being the degree of the
            polynomial.
    Returns:
        array of coefficients with the coeff[i] being 
        the coeff of x ^ i.
    """
    return np.random.randint(0, 2, size, dtype=np.int64)


def gen_uniform_poly(size, modulus):
    """Generates a polynomial with coeffecients being integers in Z_modulus
    Args:
        size: number of coeffcients, size-1 being the degree of the
            polynomial.
    Returns:
        array of coefficients with the coeff[i] being 
        the coeff of x ^ i.
    """
    return np.random.randint(0, modulus, size, dtype=np.int64)


def gen_normal_poly(size):
    """Generates a polynomial with coeffecients in a normal distribution
    of mean 0 and a standard deviation of 2, then discretize it.
    Args:
        size: number of coeffcients, size-1 being the degree of the
            polynomial.
    Returns:
        array of coefficients with the coeff[i] being 
        the coeff of x ^ i.
    """
    return np.int64(np.random.normal(0, 2, size=size))

def keygen(size, modulus, poly_mod):
    """Generate a public and secret keys
    Args:
        size: size of the polynoms for the public and secret keys.
        modulus: coefficient modulus.
        poly_mod: polynomial modulus.
    Returns:
        Public and secret key.
    """
    print("###############################")
    print("size: ", size)
    print("modulus: ", modulus)
    print("poly_mod: ", poly_mod)
    sk = gen_binary_poly(size)
    a = gen_uniform_poly(size, modulus)
    e = gen_normal_poly(size)
    print("###############################")
    """
    ###############################
    size:  2
    modulus:  100
    poly_mod:  [1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1]
    ###############################
    sk:  [0 1]
    a:  [68  6]
    e:  [4 0]
    ###############################
    b:  [96 32 94]
    [-68 -6] # -68 - 6x
    [0 1] # x
    [0 -68 -6] # -68x - 6x^2
    [4 0] # 4
    [-4 -68 -6] # -4 -68x -6x^2
    after modulous
    [96 32 94] # 96 + 32x + 94x^2
    """
    print("sk: ", sk)
    print("a: ", a)
    print("e: ", e)
    print("###############################")
    b = polyadd(polymul(-a, sk, modulus, poly_mod), -e, modulus, poly_mod)
    print("b: ", b)
    return (b, a), sk

pt = np.array([1] + [0] * (modulus - 2) + [1], dtype=np.int64)
((b,a),sk) = (keygen(size, t, pt))