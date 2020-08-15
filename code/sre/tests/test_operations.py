from sre.models import StarAtom, LetterAtom
from sre.models import Product, SRE


class TestSingleOperation():
    def test_single_read(self):
        e1 = StarAtom("start", "stop")
        e2 = LetterAtom("reset")

        p1 = Product(e1, e2)
        p2 = p1.read("reset")

        s1 = SRE(p1)
        s2 = s1.read("reset")

        assert not s2.messages()
        assert not p2.messages()

    def test_empty_read(self):
        p0 = Product()
        s0 = SRE()

        assert not p0.read("test")
        assert not s0.read("test")

    def test_single_write(self):
        e1 = StarAtom("start", "stop")
        p1 = Product(e1)
        p2 = p1.write("test")

        s1 = SRE(p1)
        s2 = s1.write("test")

        assert p2.contains(LetterAtom("test"))
        assert s2.contains(SRE(Product(LetterAtom("test"))))
