from models import Alphabet
from models import StarAtom, LetterAtom


class TestAlphabet():
    def test_single_letter(self):
        alph = Alphabet('a')
        assert 'a' in alph.letters


class TestStarAtom():
    def test_single_letter(self):
        alph = Alphabet('a')

        e1 = StarAtom('a', alphabet=alph)
        assert 'a' in e1.value


class TestLetterAtom():
    def test_single_letter(self):
        alph = Alphabet('a')

        e1 = LetterAtom(alphabet=alph, letter='a')
        assert 'a' in e1.value
