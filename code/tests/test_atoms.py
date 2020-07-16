import pytest

from sre.models import Atom
from sre.models import StarAtom, LetterAtom

from hypothesis import given
from hypothesis.strategies import from_regex, lists, sets

from sre import ALLOWED_MESSAGES


class TestCreation():
    @pytest.mark.xfail(raises=TypeError)
    def test_base_creation_fails(self):
        """
        Check that we cannot instantiate the base Atom class.
        This should throw a TypeError exception, because we
        cannot instantiate an abstract class.
        """
        a = Atom()
        a

    def test_LetterAtom_creation(self):
        """
        Check that we can create a LetterAtom with a single message.
        """
        e1 = LetterAtom('a')
        assert e1

    @pytest.mark.xfail(raises=TypeError)
    def test_LetterAtom_empty_create(self):
        """
        Check that we cannot create a LetterAtom without passing a message.
        """
        LetterAtom()

    @pytest.mark.xfail(raises=ValueError)
    def test_LetterAtom_empty_string_create(self):
        """
        Check that we cannot create a LetterAtom with an empty string.
        """
        LetterAtom("")

    @given(from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_LetterAtom_single_letter(self, x):
        """
        Check that we can create a LetterAtom using an allowed message.
        """
        e1 = LetterAtom(x)
        assert e1

    @given(from_regex("[0-9]+", fullmatch=True))
    @pytest.mark.xfail(raises=ValueError)
    def test_LetterAtom_create_with_bad_message(self, x):
        """
        Check that LetterAtom creation fails with a forbidden message.
        The pattern should be changed if ALLOWED_MESSAGES is changed.
        """
        LetterAtom(x)

    @given(lists(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=2))
    @pytest.mark.xfail(raises=TypeError)
    def test_LetterAtom_more_than_one_good_message(self, x):
        """
        Check that LetterAtom creation fails when more than one allowed
        message is passed.
        """
        LetterAtom(*x)

    @given(lists(from_regex("[0-9]+", fullmatch=True), min_size=2))
    @pytest.mark.xfail(raises=TypeError)
    def test_LetterAtom_more_than_one_bad_message(self, x):
        """
        Check that LetterAtom creation fails when more than one bad message
        is passed.
        """
        LetterAtom(*x)

    def test_StarAtom_creation(self):
        """
        Check that we can create an object of type StarAtom.
        """
        e1 = StarAtom('a', 'b', 'c')
        assert e1

    def test_StarAtom_empty_create(self):
        """
        Check that we can create an object of type StarAtom
        without passing any messages (i.e. it is a language
        over the empty sequence of messages).
        """
        e1 = StarAtom()
        assert len(e1) == 0

    @pytest.mark.xfail(raises=ValueError)
    def test_StarAtom_empty_string_create_fail(self):
        """
        Check that we cannot create an object of type StarAtom
        using an empty string.
        """
        e1 = StarAtom("")
        e1

    def test_StarAtom_list_creation(self):
        """
        Check that you can create a StarAtom
        using a list (or a set, or a tuple).
        """
        # Use * if passing a list, set, or tuple
        e1 = StarAtom(*['a', 'b', 'c'])
        assert e1

    @given(from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_StarAtom_single_message(self, x):
        """
        Check that you can create a StarAtom using any allowed message.
        """
        e1 = StarAtom(x)
        assert e1

    @given(lists(from_regex("[0-9]+", fullmatch=True), min_size=0))
    @pytest.mark.xfail(raises=ValueError)
    def test_StarAtom_creation_failure(self, x):
        """
        Check that creation fails with a forbidden message.
        The pattern should be changed if ALLOWED_MESSAGES is changed.
        """
        e1 = StarAtom(*x)
        e1

    @given(lists(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=0))
    def test_StarAtom_list_of_letters(self, x):
        """
        Check that you can create a StarAtom using a list of allowed messages.
        """
        e1 = StarAtom(*x)
        assert e1 is not None


class TestEntailment():
    """Entailment between Atoms is defined in Lemma 4.1. of [ACBJ04].
    Here we test the symmetric function, Atom.contains().
    """
    @given(lists(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=0))
    def test_StarAtom_naive_entailment_success(self, x):
        """
        Check that two StarAtoms, made from the same messages,
        contain each other.
        """
        e1 = StarAtom(*x)
        e2 = StarAtom(*x)

        assert e1.contains(e2) & e2.contains(e1)

    @given(lists(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=0))
    def test_StarAtom_empty_entailment_success(self, x):
        """
        Check that a StarAtom made with non-empty allowed messages contains
        the StarAtom made with the empty sequence.
        """
        e1 = StarAtom(*x)
        e2 = StarAtom()

        assert e1.contains(e2)

    @given(lists(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=1))
    def test_StarAtom_empty_entailment_failure(self, x):
        """
        Check that the empty StarAtom does not contain a non-empty StarAtom.
        """
        e1 = StarAtom(*x)
        e2 = StarAtom()

        assert not e2.contains(e1)

    @given(sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=0),
           sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=0))
    def test_StarAtom_entailment_success(self, x, y):
        """
        Input:
            x, y: sets of allowed messages

        e1 = StarAtom(x)
        e2 = StarAtom(x UNION y)

        Output:
            True (e2 contains e1)
        """
        z = set.union(x, y)
        e1 = StarAtom(*x)
        e2 = StarAtom(*z)

        assert e2.contains(e1)

    @given(sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=0,
                max_size=2),
           sets(from_regex(ALLOWED_MESSAGES, fullmatch=True), min_size=3))
    def test_StarAtom_entailment_failure(self, x, y):
        """
        Input:
            x, y: sets of allowed messages

        e1 = StarAtom(x)
        e2 = StarAtom(x UNION y)

        Output:
            False (e1 does not contain e2)

        Note:
            Size constraints used to make sure the sets aren't identical.
        """
        z = set.union(x, y)
        e1 = StarAtom(*x)
        e2 = StarAtom(*z)

        assert not e1.contains(e2)

    @given(from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_LetterAtom_naive_entailment_success(self, x):
        """
        Check that two LetterAtoms made with the same message
        entail each other.
        """
        e1 = LetterAtom(x)
        e2 = LetterAtom(x)

        assert e1.contains(e2) & e2.contains(e1)

    @given(from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_Mixed_containment_failure(self, x):
        """
        Check that a LetterAtom cannot contain a StarAtom,
        and that a StarAtom contains a LetterAtom (when they're
        made from the same message).
        """
        e1 = LetterAtom(x)
        e2 = StarAtom(x)

        assert not e1.contains(e2)
        assert e2.contains(e1)

    @given(from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_empty_star_in_letter(self, x):
        """
        Check that the empty StarAtom is in an arbitrary LetterAtom.
        """
        e1 = LetterAtom(x)
        e2 = StarAtom()

        assert e1.contains(e2)


class TestAbsorption():
    @given(from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_LetterAtom_absorption(self, x):
        """
        Check that a LetterAtom does not absorb itself, it does
        not absorb another LetterAtom made from the same message,
        but only absorbs an empty StarAtom.
        """
        e1 = LetterAtom(x)
        e2 = LetterAtom(x)
        e3 = StarAtom()

        assert not e1.absorbs(e1)
        assert not e1.absorbs(e2)
        assert e1.absorbs(e3)

    @given(from_regex(ALLOWED_MESSAGES, fullmatch=True),
           from_regex(ALLOWED_MESSAGES, fullmatch=True))
    def test_StarAtom_absorption(self, x, y):
        """Check that a StarAtom absorbs a LetterAtom made of the same
        message, and that it is absorbed by a StarAtom made of (at least)
        the same message.
        """
        e1 = StarAtom(x)
        e2 = LetterAtom(x)
        e3 = StarAtom(x, y)

        assert e1.absorbs(e2)
        assert e3.absorbs(e1)
