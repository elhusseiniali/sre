from abc import ABC, abstractmethod


class Alphabet():
    """
    An alphabet is just a set of letters.
    """
    def __init__(self, letters):
        """
        Input:
            letters: list-like. Every letter has to be in the English alphabet.
            Can take a singleton character, or a set of chars.
        """
        self.letters = set(letters)

    def __new__(cls, letters):
        """
        Only create an alphabet if all letters are in
        the English alphabet.
        """
        for letter in letters:
            if not str(letter).isalpha():
                raise TypeError("An alphabet can only have English letter!!")
        return super().__new__(cls)

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
    Base (Abstract) Atom class.
    """
    """
    def __init__(self, alphabet):
        self.alphabet = alphabet
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
        Only create an atom if all letters are in
        the same (valid) alphabet.
        """
        """
        if not isinstance(alphabet, Alphabet):
            raise TypeError("You need to pass an Alphabet object!")

        for letter in letters:
            if not alphabet.has_letter(letter):
                raise ValueError("You can only use letters of the"
                                 + " same alphabet!!")
        """
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
        Only create an atom if all letters are in
        the same (valid) alphabet.
        """
        """
        if not len(letter) == 1:
            raise TypeError("This is a letter atom."
                            + " You can only have one letter!!")
        if not isinstance(alphabet, Alphabet):
            raise TypeError("You need to pass an Alphabet object!")

        if not alphabet.has_letter(letter):
            raise ValueError("You can only use letters of the"
                             + " same alphabet!!")
        """

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
