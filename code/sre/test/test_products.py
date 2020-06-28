from sre.models import StarAtom, LetterAtom
from sre.models import Product

from hypothesis import given
from hypothesis.strategies import characters, lists


class TestProduct():
    @given(lists(characters(min_codepoint=97, max_codepoint=122)))
    def test_star_atom(self, x):
        e1 = StarAtom(letters=x)
        p = Product([e1])
        assert p

    @given(characters(min_codepoint=97, max_codepoint=122))
    def test_letter_atom(self, x):
        e1 = LetterAtom(letter=x)
        p = Product([e1])
        assert p

    @given(lists(characters(min_codepoint=97, max_codepoint=122)),
           characters(min_codepoint=97, max_codepoint=122))
    def test_mixed_atoms(self, x, y):
        e1 = StarAtom(letters=x)
        e2 = LetterAtom(letter=y)

        p = Product([e1, e2])
        assert p
