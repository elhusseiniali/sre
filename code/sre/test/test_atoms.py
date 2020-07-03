import pytest

from sre.models import Atom
from sre.models import StarAtom, LetterAtom

from hypothesis import given
from hypothesis.strategies import characters, lists


class TestBaseAtom():
    @pytest.mark.xfail(raises=TypeError)
    def test_creation_fails(self):
        """
        This should throw a TypeError exception, because we cannot instantiate
        an abstract class.
        """
        a = Atom()


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

    @given(lists(characters(min_codepoint=97, max_codepoint=122)))
    def test_naive_entailment_success(self, x):
        e1 = StarAtom(letters=x)
        e2 = StarAtom(letters=x)

        assert e1.entails(e2) & e2.entails(e1)


class TestLetterAtom():
    def test_creation(self):
        e1 = LetterAtom(letter='a')
        assert e1

    @given(characters(min_codepoint=97, max_codepoint=122))
    def test_single_letter(self, x):
        e1 = LetterAtom(letter=x)
        assert e1

    @given(characters(min_codepoint=97, max_codepoint=122))
    def test_naive_entailment_success(self, x):
        e1 = LetterAtom(letter=x)
        e2 = LetterAtom(letter=x)

        assert e1.entails(e2) & e2.entails(e1)
