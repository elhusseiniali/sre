from sre.models import StarAtom, LetterAtom
from sre.models import Product

from sre import ALLOWED_MESSAGES

from hypothesis import given
from hypothesis.strategies import from_regex, lists


class TestProduct():
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

    @given(lists(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=1),
           from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_two_mixed_atoms(self, x, y):
        e1 = StarAtom(*x)
        e2 = LetterAtom(y)

        p = Product(e1, e2)
        assert p


'''Some suggestions for more entailment tests:
Main interest is that it includes negative tests and non-trivial positive tests.
Also it illustrates the different ways one can call a constructor.
ea=LetterAtom('a')
eb=LetterAtom('b')
zs=StarAtom([])
as=StarAtom(['a'])
bs=StarAtom(['b'])
abs=StarAtom(['a','b'])
ep=Product()
assert ea.contains(zs)
assert ea.contains(ep)
assert not ea.contains(as)
assert as.contains(ea)
assert as.contains(zs)
assert as.contains(ep)
assert not as.contains(bs)
assert not as.contains(abs)
assert not ep.contains(ea)
assert not ep.contains(as)
assert not ep.contains(abs)
assert not ep.contains(Product(ea,ea))
assert ep.contains(ep)
assert ep.contains(zs)
assert ep.contains(Product(zs))
assert ep.contains(Product(zs,zs))
assert ea.contains(zs)
assert ea.contains(Product(zs,ep,ea,zs))
assert not ea.contains(as)
assert as.contains(Product(ea,as))
assert as.contains(Product(ea,ep,zs,ea,as))
assert abs.contains(Product(ea,bs,as,bs))
assert not as.contains(Product(ea,abs,eb))
'''
