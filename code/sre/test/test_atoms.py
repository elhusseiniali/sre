import pytest

from sre.models import Atom
from sre.models import StarAtom, LetterAtom

from hypothesis import given
from hypothesis.strategies import from_regex, lists

from sre import ALLOWED_MESSAGES


class TestBaseAtom():
    @pytest.mark.xfail(raises=TypeError)
    def test_creation_fails(self):
        """
        This should throw a TypeError exception, because we cannot instantiate
        an abstract class.
        """
        a = Atom()
        a


class TestStarAtom():
    def test_creation(self):
        e1 = StarAtom('a', 'b', 'c')
        assert e1

    @pytest.mark.xfail(raises=TypeError)
    def test_empty_create(self):
        e1 = StarAtom()
        e1

    @pytest.mark.xfail(raises=TypeError)
    def test_empty_string_create(self):
        e1 = StarAtom("")
        e1

    def test_list_creation(self):
        # Use * if passing a list
        e1 = StarAtom(*['a', 'b', 'c'])
        assert e1

    @given(from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_single_letter(self, x):
        e1 = StarAtom(x)
        assert e1

    @given(lists(from_regex("[0-9]+", fullmatch=True), min_size=1))
    @pytest.mark.xfail(raises=ValueError)
    def test_creation_failure(self, x):
        e1 = StarAtom(*x)
        e1

    @given(lists(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=1))
    def test_list_of_letters(self, x):
        e1 = StarAtom(*x)
        assert e1

    @given(lists(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=1))
    def test_naive_entailment_success(self, x):
        e1 = StarAtom(*x)
        e2 = StarAtom(*x)

        assert e1.entails(e2) & e2.entails(e1)


class TestLetterAtom():
    def test_creation(self):
        e1 = LetterAtom('a')
        assert e1

    @pytest.mark.xfail(raises=TypeError)
    def test_empty_create(self):
        e1 = LetterAtom()
        e1

    @pytest.mark.xfail(raises=TypeError)
    def test_empty_string_create(self):
        e1 = LetterAtom("")
        e1

    @given(from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_single_letter(self, x):
        e1 = LetterAtom(x)
        assert e1

    @given(from_regex("[0-9]+", fullmatch=True))
    @pytest.mark.xfail(raises=ValueError)
    def test_create_with_bad_message(self, x):
        e1 = LetterAtom(x)
        e1

    @given(lists(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=2))
    @pytest.mark.xfail(raises=TypeError)
    def test_create_with_more_than_one_good_message(self, x):
        e1 = LetterAtom(*x)
        e1

    @given(lists(from_regex("[0-9]+", fullmatch=True), min_size=2))
    @pytest.mark.xfail(raises=TypeError)
    def test_create_with_more_than_one_bad_message(self, x):
        e1 = LetterAtom(*x)
        e1

    @given(from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_naive_entailment_success(self, x):
        e1 = LetterAtom(x)
        e2 = LetterAtom(x)

        assert e1.entails(e2) & e2.entails(e1)
