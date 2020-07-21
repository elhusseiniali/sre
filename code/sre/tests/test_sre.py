from sre.models import StarAtom, LetterAtom
from sre.models import Product
from sre.models import SRE

from sre import ALLOWED_MESSAGES

from hypothesis import given
from hypothesis.strategies import from_regex, sets

import pytest


class TestCreation():
    def test_simple_creation(self):
        """Check that we can plainly create an SRE from atoms
        or from products.
        """
        e1 = StarAtom("start", "stop")
        e2 = LetterAtom("reset")
        e3 = StarAtom("help")

        p1 = Product(e1, e2)
        p2 = Product(e3)

        s1 = SRE(p1, p2)
        s2 = SRE(e1, e2, e3)
        assert s1
        assert s2

    def test_empty_creation(self):
        """Check that we can create an SRe from the empty StarAtom
        or from the empty Product, or from Product(StarAtom()).
        """
        e1 = StarAtom()
        p1 = Product(e1)
        p2 = Product()

        s1 = SRE(p1, p2)

        assert s1

    @pytest.mark.xfail(raises=TypeError)
    def test_bad_creation(self):
        """Check that creation fails with some non-atom/non-product.
        """
        s1 = SRE(1, 2, 3)
        assert not s1


class TestEntailment():
    def test_naive_containment(self):
        """Check that two SREs made of the same products contain each other.
        Also check that an SRE made from a product made of one atom,
        contains an SRE made of the atom directly.
        """
        e1 = StarAtom("start")
        p1 = Product(e1)

        s0 = SRE()
        s1 = SRE(p1)
        s2 = SRE(p1)
        s3 = SRE(e1)

        assert s1.contains(s2)
        assert s2.contains(s1)
        assert s1.contains(s0)
        assert s2.contains(s0)
        assert not s0.contains(s1)
        assert not s0.contains(s2)
        assert s3.contains(s1)
        assert s1.contains(s3)

        @given(sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=0),
               sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=0))
        def test_general_containment_success(self, x, y):
            """Check that a bigger SRE contains a smaller one.

            Parameters
            ----------
            x, y : [set]
                sets of allowed messages.
            """
            z = set.union(x, y)
            e1 = StarAtom(*x)
            e2 = StarAtom(*z)

            s1 = SRE(e1)
            s2 = SRE(e2)

            assert s2.contains(s1)

        @given(sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=0,
               max_size=2),
               sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=3))
        def test_containment_failure(self, x, y):
            """Check that a smaller SRE does not contain a larger one.

            Parameters
            ----------
            x, y : [set]
                sets of allowed messages.
            """
            z = set.union(x, y)
            e1 = StarAtom(*x)
            e2 = StarAtom(*z)

            s1 = SRE(e1)
            s2 = SRE(e2)

            assert not s1.contains(s2)
