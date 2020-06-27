from abc import ABC, abstractmethod


class Atom(ABC):
    """
    Base (Abstract) Atom class.
    """

    @abstractmethod
    def print(self):
        pass


class StarAtom(Atom):
    """
    A star atom is an atom of the form (p1 + ... + pn)*
    """
    def __init__(self, letters):
        super().__init__()
        self.value = set(letters)

    def __new__(cls, letters):
        """
        Only create an atom if all letters are alphanumeric.
        TODO:
            - Add better check than the placeholder
        """
        for letter in letters:
            if letter == '%':
                raise ValueError("Can only be alphanumeric.")
        return super().__new__(cls)

    def print(self):
        print(self.value)


class LetterAtom(Atom):
    """
    A letter-atom is an atom of the form a+Ɛ.
    """
    def __init__(self, letter):
        super().__init__()
        self.value = str(letter)

    def __new__(cls, letter):
        """
        Only create an atom if it is made from a single letter.
        """
        if not len(letter) == 1:
            raise TypeError("This is a letter atom."
                            + " You can only have one letter!!")

        return super().__new__(cls)

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
