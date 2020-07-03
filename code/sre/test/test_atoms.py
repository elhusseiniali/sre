import pytest

from sre.models import Atom
from sre.models import StarAtom, LetterAtom

from hypothesis import given
from hypothesis.strategies import from_regex, lists

import yaml

config = yaml.safe_load(open('sre/config.yml'))
PATTERN = config['allowed_messages']['pattern']


class TestBaseAtom():
    @pytest.mark.xfail(raises=TypeError)
    def test_creation_fails(self):
        """
        This should throw a TypeError exception, because we cannot instantiate
        an abstract class.
        """
        a = Atom()
        a()


class TestStarAtom():
    def test_creation(self):
        e1 = StarAtom('a', 'b', 'c')
        assert e1

    def test_list_creation(self):
        # Use * if passing a list
        e1 = StarAtom(*['a', 'b', 'c'])
        assert e1

    @given(from_regex(PATTERN, fullmatch=True))
    def test_single_letter(self, x):
        e1 = StarAtom(x)
        assert e1

    @given(lists(from_regex(PATTERN, fullmatch=True)))
    def test_list_of_letters(self, x):
        e1 = StarAtom(*x)
        assert e1

    @given(lists(from_regex(PATTERN, fullmatch=True)))
    def test_naive_entailment_success(self, x):
        e1 = StarAtom(*x)
        e2 = StarAtom(*x)

        assert e1.entails(e2) & e2.entails(e1)


class TestLetterAtom():
    def test_creation(self):
        e1 = LetterAtom(message='a')
        assert e1

    @given(from_regex(PATTERN, fullmatch=True))
    def test_single_letter(self, x):
        e1 = LetterAtom(message=x)
        assert e1

    @given(from_regex(PATTERN, fullmatch=True))
    def test_naive_entailment_success(self, x):
        e1 = LetterAtom(message=x)
        e2 = LetterAtom(message=x)

        assert e1.entails(e2) & e2.entails(e1)
