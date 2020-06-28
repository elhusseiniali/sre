from abc import ABC, abstractmethod


class Atom(ABC):
    """
    Base (Abstract) Atom class.
    """

    @abstractmethod
    def __repr__(self):
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

    def __repr__(self):
        return (f"StarAtom with {self.value}")


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

    def __repr__(self):
        return(f"LetterAtom with {self.value}")


class Product():
    """
    A product is a concatenation (a list) of atoms.
    """
    def __init__(self, atoms):
        """
        TODO:
            - Make immutable
        """
        self.value = list(atoms)

    def __new__(cls, atoms):
        """
        Only create a product from valid atoms.
        """
        for atom in atoms:
            if not isinstance(atom, Atom):
                raise TypeError("You need to pass a valid atom!")

        return super().__new__(cls)

    def __repr__(self):
        return("Product with:\n"
               f"{self.value}")


class SRE():
    """
    An SRE is a set of products.
    """
    def __init__(self, products):
        """
        TODO:
            - Make immutable
        """
        self.value = set(products)

    def __new__(cls, products):
        """
        Only create an SRE from valid products.
        """
        for product in products:
            if not isinstance(product, Product):
                raise TypeError("You need to pass a valid product!")

    def __repr__(self):
        return ("SRE made with:\n"
                f"{self.value}")
