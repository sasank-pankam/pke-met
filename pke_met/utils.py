import numpy as np


def extended_gcd(a, p):
    """Extended Euclidean Algorithm to find inverse of a modulo p."""
    if p == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(p, a % p)
    x = y1
    y = x1 - (a // p) * y1
    return g, x, y


def mod_inverse(a, p):
    """Return the modular inverse of a modulo p."""
    g, x, y = extended_gcd(a, p)
    if g != 1:
        raise ValueError(f"No inverse for {a} modulo {p}")
    return x % p


def gaussian_elimination_mod_p(A, B, p):
    """
    Solves the system of linear equations A * X = B modulo p.
    A is the coefficient matrix, B is the result vector.
    """
    n = len(B)
    augmented_matrix = np.hstack([A, B.reshape(-1, 1)])  # Augment A with B
    for i in range(n):
        # Find pivot row
        if augmented_matrix[i, i] == 0:
            for j in range(i + 1, n):
                if augmented_matrix[j, i] != 0:
                    augmented_matrix[[i, j]] = augmented_matrix[[j, i]]  # Swap rows
                    break

        # Make the pivot element 1 by multiplying by the inverse
        inv = mod_inverse(augmented_matrix[i, i], p)
        augmented_matrix[i] = (augmented_matrix[i] * inv) % p

        # Eliminate below
        for j in range(i + 1, n):
            if augmented_matrix[j, i] != 0:
                factor = augmented_matrix[j, i]
                augmented_matrix[j] = (
                    augmented_matrix[j] - factor * augmented_matrix[i]
                ) % p

    # Back substitution
    X = np.zeros(n)
    for i in range(n - 1, -1, -1):
        X[i] = (augmented_matrix[i, -1] - np.dot(augmented_matrix[i, :-1], X)) % p

    return [int(x) for x in reversed(X)]


def get_coeffient_matrix(*pairs, prime):
    lis = []
    for a in pairs:
        lis.append([pow(a, i, prime) for i in range(len(pairs) - 1, -1, -1)])
    return lis
