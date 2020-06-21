from sre.models import Alphabet

from hypothesis import given
from hypothesis.strategies import characters, lists


class TestAlphabet():
    def test_creation(self):
        alph = Alphabet('a')
        assert alph

    @given(characters(min_codepoint=97, max_codepoint=122))
    def test_single_letter(self, x):
        alph = Alphabet(x)

        assert alph.has_letter(x)

    @given(lists(characters(min_codepoint=97, max_codepoint=122)))
    def test_list_of_letters(self, x):
        alph = Alphabet(x)
        assert alph
