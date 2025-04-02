import math
import numpy as np
import textwrap

from Crypto.Hash import BLAKE2b
import random
from cyclic_group import CyclicGroup
from finite_field import FiniteField, hash_to_zp
from utils import gaussian_elimination_mod_p, get_coeffient_matrix


class PKE_MET_Base:
    def __init__(self, lamda, prime, generator=None) -> None:
        self.prime = prime
        self.l = math.ceil(math.log2(prime))
        self.zp = FiniteField(prime)
        self.group = CyclicGroup.new(prime, generator)
        self.H1 = lambda x: BLAKE2b.new(data=x, digest_bits=2 * self.l).digest()
        self.H2 = lambda x: BLAKE2b.new(data=x, digest_bits=lamda).digest()
        self.H3 = hash_to_zp(prime)

    def keygen(self):
        x = random.randint(0, self.prime - 1)
        y = random.randint(0, self.prime - 1)
        self.secret_key = (x, y)
        self.public_key = self.group.element(x), self.group.element(y)

    def concat(self, *a):
        lis = list(map(lambda x: format(x, f"0{self.l}b"), a))
        return "".join(lis)

    def get_func_f(self, message, s):
        m_con_s = self.concat(message, s)
        inp = m_con_s
        co_effs = []
        for _ in range(s):
            dig = self.H3(int(inp, 2).to_bytes(16))
            co_effs.append(dig)
            inp += self.concat(dig)

        def f(x):
            return (
                sum(
                    map(
                        lambda a: a[1] * self.group.exponentiate(x, a[0]),
                        enumerate(co_effs),
                    )
                )
                % self.group.order
            )

        return co_effs, f

    def Encrypt(self, message: int, s: int):
        X, Y = self.public_key
        if not (message < self.prime):
            raise ValueError(f"{message=} must be and int and < {self.prime}")
        if not s < self.prime:
            raise ValueError(f"{s=} must be and int and < {self.prime}")

        co_effs, f = self.get_func_f(message, s)

        A = random.randint(0, self.prime - 1)
        r1 = random.randint(0, self.prime - 1)
        r2 = random.randint(0, self.prime - 1)

        c1 = self.group.element(r1)

        c2 = int.from_bytes(self.H1(self.group.exponentiate(X, r1).to_bytes())) ^ int(
            self.concat(message, r1), 2
        )
        c3 = self.group.element(r2)
        c4 = int.from_bytes(self.H1(self.group.exponentiate(Y, r2).to_bytes())) ^ int(
            self.concat(A, f(A)), 2
        )
        final_c = self.concat(
            s, c1, c2, c3, c4, self.group.exponentiate(Y, r2), *co_effs
        )
        c5 = int.from_bytes(self.H2(int(final_c, 2).to_bytes(16)))

        return s, c1, c2, c3, c4, c5

    def test(self, *cts_pairs):
        cts, tkts = zip(*cts_pairs)
        t = len(tkts)
        if any(ct[0] - t for ct in cts):
            raise ValueError(f"all s's must be equal to {t}")

        pairs = []
        for ct, tkt in zip(cts, tkts):
            s, _, _, c3, c4, _ = ct
            temp = c4 ^ int.from_bytes(
                self.H1(self.group.exponentiate(c3, tkt).to_bytes())
            )
            temp = format(temp, f"0{2 * self.l}b")
            A_i, f_i_A_i = temp[: len(temp) // 2], temp[len(temp) // 2 :]
            A_i = int(A_i, 2)
            f_i_A_i = int(f_i_A_i, 2)
            pairs.append((A_i, f_i_A_i))
        # error in this functions solutions
        a_s, f_a_s = zip(*pairs)
        A = np.array(get_coeffient_matrix(*a_s, prime=self.prime))
        B = np.array(f_a_s)
        co_effs = gaussian_elimination_mod_p(A, B, self.prime)

        def check_for_c5(inp):
            ct, tkt = inp
            t, c1, c2, c3, c4, c5 = ct
            rhs_final = int(
                self.concat(
                    t, c1, c2, c3, c4, self.group.exponentiate(c3, tkt), *co_effs
                ),
                2,
            ).to_bytes(16)
            rhs = int.from_bytes(self.H2(rhs_final))

            return rhs == c5

        return all(map(check_for_c5, zip(cts, tkts)))

    def print_info(self):
        print(
            textwrap.dedent(f"""
        -------Info------------
        Secret key : {self.secret_key}
        Public key : {self.public_key}
        prime      : {self.prime}
        Generator  : {self.group.generator}

        """)
        )


class PKE_MET_private(PKE_MET_Base):
    def __init__(self, lamda, prime, generator=None) -> None:
        super().__init__(lamda, prime, generator)
        self.keygen()

    def aut(self):
        return self.secret_key[1]

    def decrypt(self, ct, other):
        s, c1, c2, c3, c4, c5 = ct
        x, y = self.secret_key

        temp = c2 ^ int.from_bytes(self.H1(self.group.exponentiate(c1, x).to_bytes()))
        temp = format(temp, f"0{2 * self.l}b")
        m_d, r_d = temp[: len(temp) // 2], temp[len(temp) // 2 :]
        m_d = int(m_d, 2)
        r_d = int(r_d, 2)

        co_effs, f_d = self.get_func_f(m_d, s)

        g_po_r_d = self.group.element(r_d)
        if not g_po_r_d == c1:
            raise ValueError("decryption failed! possible mismatch of private key")

        temp = c4 ^ int.from_bytes(self.H1(self.group.exponentiate(c3, y).to_bytes()))
        temp = format(temp, f"0{2 * self.l}b")
        A_d, f_of_A_d = temp[: len(temp) // 2], temp[len(temp) // 2 :]
        A_d = int(A_d, 2)
        f_of_A_d = int(f_of_A_d, 2)

        if not f_of_A_d == f_d(A_d):
            raise ValueError("decryption failed! possible mismatch of private key")

        final_c = self.concat(
            s, c1, c2, c3, c4, self.group.exponentiate(c3, y), *co_effs
        )
        c5_d = int.from_bytes(self.H2(int(final_c, 2).to_bytes(16)))

        if not c5 == c5_d:
            raise ValueError("decryption failed! possible mismatch of private key")

        return m_d


class PKE_MET_public(PKE_MET_Base):
    def __init__(self, lamda, public_key, prime, generator=None) -> None:
        super().__init__(lamda, prime, generator)
        self.public_key = public_key
