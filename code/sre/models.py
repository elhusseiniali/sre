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
        """This is the symmetric function to Entailment as defined in Lemma 4.1.
        in [ACBJ04].


        Parameters
        ----------
        atom : [type]
            [description]

        Returns
        -------
        [bool]
            True: if input atom is a subset of (self) atom.
            False: otherwise. (A StarAtom cannot be contained in a LetterAtom.)

        Raises
        ------
        TypeError:
            if anything other than an atom is passed.
        """
        if not isinstance(atom, Atom):
            raise TypeError("You can only check if an atom"
                            " contains another atom!")
        if (isinstance(self, LetterAtom)
           and isinstance(atom, StarAtom)):
            return atom.messages == set()
        else:
            return set(atom.messages).issubset(set(self.messages))

    def __eq__(self, other):
        """
        Semantic equality.
        """
        if isinstance(self, type(other)):
            return self.messages == other.messages
        return False


class StarAtom(Atom):
    """
    A star atom is an atom of the form (p1 + ... + pn)*

    Usage
    -----
        messages: (two options)
            i. either StarAtom(message1, message2, etc...)
            ii. or StarAtom(set/list/tuple_of_messages)
            Check test cases for examples.
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
                if message is None:
                    raise TypeError("You can't pass None!")

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
        """Only create an atom if it is made from a single
        allowed message.

        Returns
        -------
        [LetterAtom]
            A LetterAtom from the message passed to the constructor.

        Raises
        ------
        TypeError:
            if no message is passed: because a LetterAtom takes
            messages as arguments (as opposed to a sequence of messages).
        TypeError:
            if None is passed.
        TypeError:
            if more than one message is passed.
        TypeError:
            if anything other than a string is passed.
        ValueError:
            if a bad (not allowed) message is passed.
        """
        if not messages:
            raise TypeError("You have to pass a message!")

        if messages[0] is None:
            raise TypeError("You can't pass None!")

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
    def __init__(self, *objects):
        """
        TODO:
            - Make immutable
        """
        self.objects = []
        for object in objects:
            if isinstance(object, Product):
                for item in object.objects:
                    self.objects.append(item)
            else:
                self.objects.append(object)

    def contains(self, product):
        """This is the symmetric of the entailment
            function for products from [ACBJ04].
            Run-time is linear (Lemma 4.2).
            Function definition retrieved from Proof
            of Lemma 4.2.

        Parameters
        ----------
        product : A valid product or atom.
            If an atom is passed, it is changed to a product.

        Returns
        -------
        [bool]
            True: if self contains input product.
            False: otherwise.

        Raises
        ------
        TypeError:
            if anything other than a product or atom is passed.
        """
        if not isinstance(product, Product):
            if isinstance(product, Atom):
                product = Product(product)
            else:
                raise TypeError("You can only pass a product or an atom!")

        if not product.objects:
            # p contains epsilon
            return True
        elif not self.objects:
            # epsilon does not contain anything
            return False

        e1 = product.objects[0]
        e2 = self.objects[0]

        if not len(self.objects) > 1:
            p2 = Product()
        else:
            p2 = Product(*self.objects[1:])

        if not len(product.objects) > 1:
            p1 = Product()
        else:
            p1 = Product(*product.objects[1:])

        if (not e2.contains(e1)) and p2.contains(product):
            return True
        elif (isinstance(e1, LetterAtom) and e1.contains(e2)
              and p2.contains(p1)):
            return True
        elif (isinstance(e2, StarAtom) and e2.contains(e1)
              and self.contains(p1)):
            return True
        else:
            return False

    def __new__(cls, *objects):
        """
        Only create a product from valid atoms or products.
        """
        for object in objects:
            if (not isinstance(object, Atom)
               and not isinstance(object, Product)):
                raise TypeError("You need to pass a valid atom or product!")

        return super().__new__(cls)

    def __eq__(self, other):
        """
        Structural equality.
        """
        if isinstance(self, type(other)):
            return self.objects == other.objects
        return False

    def __repr__(self):
        return("Product with:\n"
               f"{self.objects}")


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
