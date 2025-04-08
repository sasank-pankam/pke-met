import random
from pke_met import PKE_MET_private, PKE_MET_public


def test():
    params = PKE_MET_private.setup(16)
    p1 = PKE_MET_private(params)
    p2 = PKE_MET_private(params)
    p3 = PKE_MET_private(params)

    p1.print_info()
    p2.print_info()
    p3.print_info()

    o1 = PKE_MET_public(p1.public_key, params)
    o2 = PKE_MET_public(p2.public_key, params)
    o3 = PKE_MET_public(p3.public_key, params)

    prime = params["prime"]

    m1 = random.randint(0, prime - 1)
    print(f"Message used for encryption is: {m1} ")
    s = 3
    m2 = random.randint(0, prime - 1)
    print(m2)
    m3 = 2

    ct1 = o1.Encrypt(m1, s)
    ct2 = o2.Encrypt(m3, s)
    ct3 = o3.Encrypt(m2, s)

    print(p1.test((ct1, p1.aut()), (ct2, p2.aut()), (ct3, p3.aut())))


if __name__ == "__main__":
    test()
