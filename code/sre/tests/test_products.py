from sre.models import StarAtom, LetterAtom
from sre.models import Product

from sre import ALLOWED_MESSAGES

from hypothesis import given
from hypothesis.strategies import from_regex, lists, integers, sets

import pytest


class TestCreation():
    @given(lists(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=1))
    def test_star_atom(self, x):
        e1 = StarAtom(*x)

        p = Product(e1)
        assert p

    @given(from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_letter_atom(self, x):
        e1 = LetterAtom(x)

        p = Product(e1)
        assert p

    @given(sets(from_regex(ALLOWED_MESSAGES, fullmatch=True)),
           from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_two_mixed_atoms(self, x, y):
        e1 = StarAtom(*x)
        e2 = LetterAtom(y)

        p = Product(e1, e2)
        assert p

    @given(lists(integers))
    @pytest.mark.xfail(raises=TypeError)
    def test_creation_from_bad_objects(self, x):
        Product(*x)

    @given(sets(from_regex(ALLOWED_MESSAGES, fullmatch=True)),
           sets(from_regex(ALLOWED_MESSAGES, fullmatch=True)))
    def test_create_from_product(self, x, y):
        """
        Check that a product made from products is a list of atoms (and not
        a list of products and atoms).
        """
        e1 = StarAtom(*x)
        e2 = StarAtom(*y)

        p1 = Product(e1)
        p2 = Product(p1, e2)

        assert p2.atoms == tuple([e1, e2])


class TestEntailment():
    @given(sets(from_regex(ALLOWED_MESSAGES, fullmatch=True)))
    def test_containment_naive_success(self, x):
        e1 = StarAtom(*x)
        p1 = Product(e1)
        p2 = Product(e1)

        assert p1.contains(p2)
        assert p2.contains(p1)

    @given(sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=1))
    def test_empty_containment(self, x):
        p0 = Product()
        p1 = Product(StarAtom(*x))

        assert p1.contains(p0)
        assert not p0.contains(p1)

    def test_containment_success(self):
        e1 = StarAtom("start", "stop")
        e2 = StarAtom("start")

        p1 = Product(e1)
        p2 = Product(e2)

        assert p1.contains(p2)

    @given(sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=0),
           sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=0))
    def test_general_containment_success(self, x, y):
        """Check that a bigger product contains a smaller one.

        Parameters
        ----------
        x, y : [set]
            sets of allowed messages.

        e1 = StarAtom(x)
        e2 = StarAtom(x UNION y)
        """
        z = set.union(x, y)
        e1 = StarAtom(*x)
        e2 = StarAtom(*z)

        p1 = Product(e1)
        p2 = Product(e2)

        assert p2.contains(p1)

    @given(sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=0,
           max_size=2),
           sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=3))
    def test_containment_failure(self, x, y):
        z = set.union(x, y)
        e1 = StarAtom(*x)
        e2 = StarAtom(*z)

        p1 = Product(e1)
        p2 = Product(e2)

        assert not p1.contains(p2)

    def test_plain_empty_containment(self):
        """ Check that the empty product and the product made with the empty
        StarAtom contain each other.
        """
        p1 = Product(StarAtom())
        p2 = Product()

        assert p1.contains(p2)
        assert p2.contains(p1)


'''Some suggestions for more entailment tests:
Main interest is that it includes negative tests and non-trivial
positive tests.
Also it illustrates the different ways one can call a constructor.
ea=LetterAtom('a')
eb=LetterAtom('b')
zs=StarAtom()
as=StarAtom('a')
bs=StarAtom('b')
abs=StarAtom('a','b')
ep=Product()
DONE assert ea.contains(zs)
???? assert ea.contains(ep)
DONE assert not ea.contains(as)
DONE assert as.contains(ea)
DONE assert as.contains(zs)
???? assert as.contains(ep)
DONE assert not as.contains(bs)
DONE assert not as.contains(abs)
???? assert not ep.contains(ea)
???? assert not ep.contains(as)
???? assert not ep.contains(abs)
assert not ep.contains(Product(ea,ea))
assert ep.contains(ep)
assert ep.contains(zs)
assert ep.contains(Product(zs))
assert ep.contains(Product(zs,zs))
DONE assert ea.contains(zs)
assert ea.contains(Product(zs,ep,ea,zs))
DONE assert not ea.contains(as)
assert as.contains(Product(ea,as))
assert as.contains(Product(ea,ep,zs,ea,as))
assert abs.contains(Product(ea,bs,as,bs))
assert not as.contains(Product(ea,abs,eb))
'''
