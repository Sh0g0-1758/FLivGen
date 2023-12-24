import numpy as np
from numpy.polynomial import polynomial as poly

pt = 42
size = 2
t = 2**8
modulus = 2**4

x = np.array([pt] + [0] * (size - 1), dtype=np.int64) % t
y = np.random.randint(0, 2, size, dtype=np.int64)
poly_mod = np.array([1] + [0] * (modulus - 1) + [1])


result = np.int64(
        np.round(poly.polydiv(poly.polyadd(x, y) % t, poly_mod)[1] % t)
    )

print(x)
print(y)
print(poly_mod)
print(result)