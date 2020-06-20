from abc import ABC, abstractmethod


class Alphabet():
    """
    An alphabet is just a set of letters.
    """
    def __init__(self, *args):
        """
        TODO:
            - Check letters before object creation
        """
        self.letters = set(args)

    def has_letter(self, letter):
        """
        Input:
            Letter
        Output:
            True if letter is in the alphabet.
            False otherwise.
        """
        return letter in self.letters

    def print(self):
        print(self.letters)


class Atom(ABC):
    """
    Base Atom class.
    """
    def __init__(self, alphabet):
        self.alphabet = alphabet

    @abstractmethod
    def print(self):
        pass


class StarAtom(Atom):
    """
    A star atom is an atom of the form (p1 + ... + pn)*
    """
    def __init__(self, *args, alphabet):
        """
        TODO:
            - Check that args are in alphabet.letters
        """
        super().__init__(alphabet)
        self.value = set(args)

    def print(self):
        print(self.value)


class LetterAtom(Atom):
    """
    A letter-atom is an atom of the form a+Ɛ
    """
    def __init__(self, alphabet, letter):
        """
        TODO:
            - Check that letter is in alphabet.letters
        """
        super().__init__(alphabet)
        self.value = letter

    def print(self):
        print(self.value)


class Product():
    """
    A product is a concatenation (a list) of atoms.
    """
    def __init__(self, *args):
        """
        TODO:
            - Check that args are atoms
            - Make immutable
        """
        self.value = list(args)


class SRE():
    """
    An SRE is a set of products.
    """
    def __init__(self, *args):
        """
        TODO:
            - Check that args are products
            - Make immutable
        """
        self.value = set(args)
