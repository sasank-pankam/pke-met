import random
from pke_met import PKE_MET_private, PKE_MET_public
from Crypto.Util.number import getPrime

KEY_SIZE = 8


def test():
    prime = getPrime(KEY_SIZE)
    # prime = (
    #     115792089237316195423570985008687907852837564279074904382605163141518161494337
    # )
    print("Prime: ", prime)

    p1 = PKE_MET_private(16, prime)
    p2 = PKE_MET_private(16, prime)
    p3 = PKE_MET_private(16, prime)

    p1.print_info()
    p2.print_info()
    p3.print_info()

    o1 = PKE_MET_public(16, p1.public_key, prime)
    o2 = PKE_MET_public(16, p2.public_key, prime)
    o3 = PKE_MET_public(16, p3.public_key, prime)

    m1 = random.randint(0, prime - 1)
    print(f"Message used for encryption is: {m1} ")
    s = 3
    m2 = 30

    ct1 = o1.Encrypt(m1, s)
    ct2 = o2.Encrypt(m1, s)
    ct3 = o3.Encrypt(m1, s)

    # print(p1.decrypt(ct1, o1))
    # print(p2.decrypt(ct2, o2))
    # print(p3.decrypt(ct3, o3))

    print(p1.test((ct1, p1.aut()), (ct2, p2.aut()), (ct3, p3.aut())))


if __name__ == "__main__":
    test()
