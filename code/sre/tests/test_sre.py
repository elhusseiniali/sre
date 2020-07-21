from sre.models import StarAtom, LetterAtom
from sre.models import Product
from sre.models import SRE


class TestCreation():
    def test_simple_atoms(self):
        e1 = StarAtom("start", "stop")
        e2 = LetterAtom("reset")
        e3 = StarAtom("help")

        p1 = Product(e1, e2)
        p2 = Product(e3)

        s1 = SRE(p1, p2)
        assert s1

    def test_empty_creation(self):
        e1 = StarAtom()
        p1 = Product(e1)
        p2 = Product()

        s1 = SRE(p1, p2)

        assert s1


class TestContainment():
    def test_naive_containment(self):
        e1 = StarAtom("start")
        p1 = Product(e1)

        s0 = SRE()
        s1 = SRE(p1)
        s2 = SRE(p1)

        assert s1.contains(s2)
        assert s2.contains(s1)
        assert s1.contains(s0)
        assert s2.contains(s0)
        assert not s0.contains(s1)
        assert not s0.contains(s2)
