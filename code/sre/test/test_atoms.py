import pytest

from sre.models import Atom
from sre.models import StarAtom, LetterAtom

from hypothesis import given
from hypothesis.strategies import from_regex, lists, sets

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

    def test_empty_create(self):
        e1 = StarAtom()
        assert e1

    @pytest.mark.xfail(raises=TypeError)
    def test_empty_string_create(self):
        e1 = StarAtom("")
        e1

    def test_list_creation(self):
        # Use * if passing a list, set, or tuple
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

        assert e1.contains(e2) & e2.contains(e1)

    @given(lists(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=1))
    def test_empty_entailment_success(self, x):
        e1 = StarAtom(*x)
        e2 = StarAtom()

        assert e1.contains(e2)

    @given(lists(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=1))
    def test_empty_entailment_failure(self, x):
        e1 = StarAtom(*x)
        e2 = StarAtom()

        assert not e2.contains(e1)

    @given(sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=1),
           sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=1))
    def test_entailment_success(self, x, y):
        """
        Input:
            x, y: lists of allowed messages

        e1 = StarAtom(x)
        e2 = StarAtom(x UNION y)

        Output:
            True (e2 contains e1)
        """
        z = set.union(x, y)
        e1 = StarAtom(*x)
        e2 = StarAtom(*z)

        assert e2.contains(e1)

    @given(sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=1),
           sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=2))
    def test_entailment_failure(self, x, y):
        """
        Input:
            x, y: lists of allowed messages

        e1 = StarAtom(x)
        e2 = StarAtom(x UNION y)

        Output:
            False (e1 does not contain e2)
        """
        z = set.union(x, y)
        e1 = StarAtom(*x)
        e2 = StarAtom(*z)

        assert not e1.contains(e2)


class TestLetterAtom():
    def test_creation(self):
        e1 = LetterAtom('a')
        assert e1

    @pytest.mark.xfail(raises=TypeError)
    def test_empty_create(self):
        e1 = LetterAtom()
        assert e1

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

        assert e1.contains(e2) & e2.contains(e1)
