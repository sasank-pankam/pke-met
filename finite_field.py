from Crypto.Hash import SHA256


class FiniteField:
    def __init__(self, prime):
        """
        Initialize a finite field of prime order.
        :param prime: A prime number defining the field order.
        """
        # if prime <= 1 or not self.is_prime(prime):
        #     raise ValueError("Field order must be a prime number.")

        self.prime = prime

    def add(self, a, b):
        """
        Perform addition in the finite field.
        """
        return (a + b) % self.prime

    def subtract(self, a, b):
        """
        Perform subtraction in the finite field.
        """
        return (a - b) % self.prime

    def multiply(self, a, b):
        """
        Perform multiplication in the finite field.
        """
        return (a * b) % self.prime

    def inverse(self, a):
        """
        Compute the multiplicative inverse of an element in the field.
        """
        if a % self.prime == 0:
            raise ValueError("Zero has no multiplicative inverse.")
        return pow(a, -1, self.prime)

    def divide(self, a, b):
        """
        Perform division in the finite field.
        """
        return (a * self.inverse(b)) % self.prime

    def __contains__(self, value):
        """
        Check if a value belongs to the finite field.
        """
        return 0 <= value < self.prime

    @staticmethod
    def is_prime(n):
        """
        Check if a number is prime.
        """
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def __repr__(self):
        return f"FiniteField(prime={self.prime})"


def hash_to_zp(p):
    def helper(x):
        digest = SHA256.new(x).digest()
        integer = int.from_bytes(digest, byteorder="big")
        return integer % p

    return helper
