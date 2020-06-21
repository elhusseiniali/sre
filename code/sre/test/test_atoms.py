from sre.models import Alphabet
from sre.models import StarAtom, LetterAtom


class TestStarAtom():
    def test_creation(self):
        alph = Alphabet('a')

        e1 = StarAtom('a', alphabet=alph)
        assert e1


class TestLetterAtom():
    def test_creation(self):
        alph = Alphabet('a')

        e1 = LetterAtom(alphabet=alph, letter='a')
        assert e1
