from abc import ABC, abstractmethod

from sre import ALLOWED_MESSAGES


class Atom(ABC):
    """
    Base (Abstract) Atom class.
    """

    @abstractmethod
    def __repr__(self):
        pass

    def entails(self, atom):
        """
        Input:
            Some atom
        Output:
            True if current atom (self) is a subset of input atom.
            False otherwise.
        """
        if not isinstance(atom, Atom):
            raise TypeError("You can only check if an atom"
                            " entails another atom!")
        return set(self.value).issubset(set(atom.value))


class StarAtom(Atom):
    """
    A star atom is an atom of the form (p1 + ... + pn)*
    """
    def __init__(self, *messages):
        super().__init__()
        self.value = set(str(message) for message in messages)

    def __new__(cls, *messages):
        """
        Only create an atom if all messages are alphanumeric.
        TODO:
            - Add better check than the placeholder
        """
        for message in messages:
            if not ALLOWED_MESSAGES.match(message):
                raise ValueError("Message has to start with a lower-case "
                                 "letter, and it can be followed by "
                                 "a number.")
        return super().__new__(cls)

    def __repr__(self):
        return (f"StarAtom with {self.value}")


class LetterAtom(Atom):
    """
    A letter-atom is an atom of the form a+Ɛ.
    """
    def __init__(self, message):
        super().__init__()
        self.value = set(str(message))

    def __new__(cls, message):
        """
        Only create an atom if it is made from a single message.
        """
        if not ALLOWED_MESSAGES.match(message):
            raise TypeError("This is a letter atom."
                            + " You can only have one message!!")

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

        return super().__new__(cls)

    def __repr__(self):
        return ("SRE made with:\n"
                f"{self.value}")
