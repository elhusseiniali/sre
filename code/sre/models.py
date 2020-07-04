from abc import ABC, abstractmethod

from sre import ALLOWED_MESSAGES


class Atom(ABC):
    """
    Base (Abstract) Atom class.
    """
    def __init__(self, *messages):
        if messages:
            self.messages = set(str(message) for message in messages)
        else:
            self.messages = set()

    @abstractmethod
    def __repr__(self):
        pass

    def contains(self, atom):
        """
        This is the symmetric function to Entailment as defined in Lemma 4.1.
        in [ACBJ04].
        Input:
            Some atom
        Output:
            True if input atom is a subset of (self) atom.
            False otherwise.
        """
        if not isinstance(atom, Atom):
            raise TypeError("You can only check if an atom"
                            " contains another atom!")
        return set(atom.messages).issubset(set(self.messages))


class StarAtom(Atom):
    """
    A star atom is an atom of the form (p1 + ... + pn)*
    """
    def __new__(cls, *messages):
        """
        Only create an atom if all messages are valid.
        If no messages are passed, create an atom with
        the empty set (i.e. the language with one word,
        the empty sequence).
        """
        if messages:
            for message in messages:
                if not message:
                    raise TypeError("You can't pass an empty string!")

                if not ALLOWED_MESSAGES.match(message):
                    raise ValueError("Message has to start with a lower-case "
                                     "letter, and it can be followed by "
                                     "a number.")
        return super().__new__(cls)

    def __repr__(self):
        return (f"StarAtom with {self.messages}")


class LetterAtom(Atom):
    """
    A letter-atom is an atom of the form a+Ɛ.
    """

    def __new__(cls, *messages):
        """
        Only create an atom if it is made from a single
        allowed message.
        A message must be passed, because a LetterAtom
        takes messages as arguments (as opposed to a sequence).
        """
        if not messages:
            raise TypeError("You have to pass a message!")

        if not messages[0]:
            raise TypeError("You can't pass an empty string!")

        if len(messages) > 1:
            raise TypeError("You can only pass a single message!")

        if not isinstance(messages[0], str):
            raise TypeError("You can only pass a string!")

        if not ALLOWED_MESSAGES.match(messages[0]):
            raise ValueError("You can only pass an allowed message!"
                             + " See docs for help.")

        return super().__new__(cls)

    def __repr__(self):
        return(f"LetterAtom with {self.messages}")


class Product():
    """
    A product is a concatenation (a list) of atoms.
    """
    def __init__(self, *atoms):
        """
        TODO:
            - Make immutable
        """
        self.messages = list(atoms)

    def __new__(cls, *atoms):
        """
        Only create a product from valid atoms.
        """
        for atom in atoms:
            if (not isinstance(atom, Atom)
               and not isinstance(atom, Product)):
                raise TypeError("You need to pass a valid atom!")

        return super().__new__(cls)

    def __repr__(self):
        return("Product with:\n"
               f"{self.messages}")


class SRE():
    """
    An SRE is a set of products.
    """
    def __init__(self, products):
        """
        TODO:
            - Make immutable
        """
        self.messages = set(products)

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
                f"{self.messages}")
