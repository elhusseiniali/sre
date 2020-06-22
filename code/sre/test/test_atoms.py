from sre.models import StarAtom, LetterAtom

from hypothesis import given
from hypothesis.strategies import characters, lists


class TestStarAtom():
    def test_creation(self):
        e1 = StarAtom(letters='a')
        assert e1

    @given(characters(min_codepoint=97, max_codepoint=122))
    def test_single_letter(self, x):
        e1 = StarAtom(letters=x)
        assert e1

    @given(lists(characters(min_codepoint=97, max_codepoint=122)))
    def test_list_of_letters(self, x):
        e1 = StarAtom(letters=x)
        assert e1


class TestLetterAtom():
    def test_creation(self):
        e1 = LetterAtom(letter='a')
        assert e1

    @given(characters(min_codepoint=97, max_codepoint=122))
    def test_single_letter(self, x):
        e1 = LetterAtom(letter=x)
        assert e1
