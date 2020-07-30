from abc import ABC, abstractmethod

from sre import ALLOWED_MESSAGES
from sre.iterators import Iterator


class Atom(ABC):
    """
    Base (Abstract) Atom class.
    """
    def __init__(self, *messages):
        if messages:
            self.messages = frozenset(str(message) for message in messages)
        else:
            self.messages = frozenset()

    def contains(self, atom):
        """This is the symmetric function to Entailment as defined in Lemma 4.1.
        in [ACBJ04].


        Parameters
        ----------
        atom : [LetterAtom, StarAtom]
            any valid Atom.

        Returns
        -------
        [bool]
            True: if *atom* is a subset of *self*.
            False: otherwise.

        Note
        -----
        (A StarAtom cannot be contained in a LetterAtom.)

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
            return atom.messages == frozenset()
        else:
            return set(atom).issubset(set(self))

    @abstractmethod
    def absorbs(self, other):
        """e1 absorbs e2 iff e1.e2 is equivalent to e1
        iff e2.e1 is equivalent to e1

        Parameters
        ----------
        other : [Atom]
            any valid Atom

        Returns
        -------
        [bool]
            True if self absorbs other.
            False otherwise.
        """
        raise NotImplementedError

    def __eq__(self, other):
        """
        Semantic equality:
            Two atoms are equal iff they have the same messages
            (and are of the same type).
        """
        if isinstance(self, type(other)):
            return self.messages == other.messages
        return False

    def __hash__(self):
        return hash(self.messages)

    def __iter__(self):
        return Iterator(self.messages)

    def __next__(self):
        return Iterator.__next__(self.messages)

    def __len__(self):
        """The number of messages in an atom.
        Usage:
        -------
        len(e1)

        Returns
        -------
        [int]
        """
        return len(self.messages)

    @abstractmethod
    def __repr__(self):
        pass


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

    def absorbs(self, other):
        """Absorption test for StarAtom.

        Parameters
        ----------
        other : [Atom]
            any valid Atom

        Returns
        -------
        [bool]
            True if self absorbs other.
            False otherwise.
        """
        if not isinstance(other, Atom):
            raise TypeError("An atom can only absorb another atom!")

        for message in other:
            if not any(first == message for first in self):
                return False
        return True

    def __repr__(self):
        return (f"StarAtom with {set(self.messages)}")


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
            -   if no message is passed: because a LetterAtom
                takes messages as arguments (as opposed to a
                sequence of messages).
            -   if None is passed.
            -   if more than one message is passed.
            -   if anything other than a string is passed.
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

    def absorbs(self, other):
        """A letter atom can only absorb ∅*.

        Returns
        -------
        [bool]
            False if other is StarAtom() (i.e. ∅*)
            True otherwise
        """
        if not isinstance(other, Atom):
            raise TypeError("An atom can only absorb another atom!")

        return not bool(other)

    def __repr__(self):
        return(f"LetterAtom with {set(self.messages)}")


class Product():
    """A product is a concatenation (a list) of atoms.

    If another product is passed, decompose it into
    atoms and use the atoms to build the product.

    Note: atoms stored in a tuple because tuples are
          immutable.
    """
    def __init__(self, *objects):
        self.atoms = []

        for object in objects:
            if isinstance(object, Product):
                for item in object.atoms:
                    self.atoms.append(item)
            else:
                self.atoms.append(object)

        self.atoms = tuple(self.atoms)

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

        if self == product:
            # if both products are structurally equal
            return True

        if self.messages() == product.messages():
            return True

        if not product.atoms:
            # product is epsilon
            # self always contains epsilon
            return True
        elif not self.atoms:
            # epsilon does not contain anything
            return False

        e1 = product.atoms[0]
        e2 = self.atoms[0]

        if not len(self.atoms) > 1:
            p2 = Product()
        else:
            p2 = Product(*self.atoms[1:])

        if not len(product.atoms) > 1:
            p1 = Product()
        else:
            p1 = Product(*product.atoms[1:])

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

    def messages(self):
        """Return a list of all messages.

        Returns
        -------
        [list]
            A list of sets (of messages in StarAtoms)
            and strings (messages from LetterAtoms).
        """
        messages = []

        for atom in self:
            if isinstance(atom, StarAtom):
                if atom.messages:
                    messages.append(set(atom.messages))
            elif isinstance(atom, LetterAtom):
                messages.append(*atom.messages)

        return messages

    def is_normal(self):
        """Check if a product is normal, as per definition 5.2.
        Change made: a normal product does not have empty atoms inside.

        Returns
        -------
        [bool]
            True if self is normal, False otherwise.
        """
        for i in range(len(self) - 1):
            if(
                Product(self.atoms[i],
                        self.atoms[i+1]).contains(Product(self.atoms[i]))
               or
                Product(self.atoms[i]).contains(Product(self.atoms[i],
                                                        self.atoms[i+1]))
               or
                not self.atoms[i]
               ):
                return False
        return True

    def normalize(self):
        """Normalize a product (Definition 5.2. in [ACBJ04]).
        Change made: a normal product does not have empty atoms inside.
        self is modified.
        """
        discard = []
        for i in range(len(self) - 1):
            if Product(self.atoms[i],
                       self.atoms[i+1]).contains(Product(self.atoms[i])):
                discard.append(i)
            elif Product(self.atoms[i]).contains(Product(self.atoms[i],
                                                         self.atoms[i+1])):
                discard.append(i+1)
            elif not self.atoms[i]:
                discard.append(i)

        atoms = list(self.atoms)
        for index in sorted(discard, reverse=True):
            del atoms[index]

        return SRE(*atoms)

    def __new__(cls, *messages):
        """
        Only create a product from valid atoms or products.
        """
        for message in messages:
            if (not isinstance(message, Atom)
               and not isinstance(message, Product)):
                raise TypeError("You need to pass a valid atom or product!")

        return super().__new__(cls)

    def __eq__(self, other):
        """
        Structural equality:
            Two products are equal iff they have the same structure.
        """
        if isinstance(self, type(other)):
            return self.atoms == other.atoms

        return False

    def __hash__(self):
        return hash(self.atoms)

    def __iter__(self):
        return Iterator(self.atoms)

    def __next__(self):
        return Iterator.__next__(self.atoms)

    def __len__(self):
        """The number of atoms in a product.
        Usage:
        -------
        len(11)

        Returns
        -------
        [int]
        """
        return len(self.atoms)

    def __repr__(self):
        return("Product with:\n"
               f"{list(self.atoms)}")


class SRE():
    """
    An SRE is a set of products.
    """
    def __init__(self, *products):
        self.products = []
        for product in products:
            if isinstance(product, Atom):
                self.products.append(Product(product))
            else:
                self.products.append(product)

        self.products = frozenset(self.products)

    def contains(self, other):
        """
        An SRE s1 contains an SRE s2 iff every product
        in s2 is contained in some product in s1.

        Parameters
        ----------
        other : [SRE]
            any valid SRE.

        Returns
        -------
        [bool]
            True: if self contains input SRE.
            False: otherwise.
        """
        for second in other:
            if not any(first.contains(second) for first in self):
                return False
        return True

    def is_normal(self):
        """An SRE is normal iff no two products contain each other, and
        all products are normal.
        (Definition 5.3.)
        Returns
        -------
        [bool]
            True if self is normal, False otherwise.
        """
        products = list(self.products)
        for i in range(len(self)):
            if not products[i].is_normal():
                return False

            for j in range(len(self)):
                if i != j:
                    if products[i].contains(products[j]):
                        return False
                    elif products[j].contains(products[i]):
                        return False
        return True

    def normalize(self):
        """Normalize self.
        """
        products = list(self.products)
        discard = []
        for i in range(len(self)):
            if not products[i].is_normal():
                products[i].normalize()

            for j in range(len(self)):
                if i != j:
                    if products[i].contains(products[j]):
                        discard.append(j)
                    elif products[j].contains(products[i]):
                        discard.append(i)
        discard = set(discard)

        for index in sorted(discard, reverse=True):
            del products[index]

        return SRE(*products)

    def messages(self):
        """
        Returns
        -------
        [set]
            All messages in an SRE.
        """
        messages = []
        for product in self:
            for atom in product:
                messages.extend(atom.messages)
        return set(messages)

    def __new__(cls, *products):
        """
        Only create an SRE from valid products or atoms.
        """
        for product in products:
            if not isinstance(product, Product):
                if not isinstance(product, Atom):
                    raise TypeError("You need to pass a valid product"
                                    " or atom!")

        return super().__new__(cls)

    def __hash__(self):
        return hash(self.products)

    def __iter__(self):
        return Iterator(self.products)

    def __next__(self):
        return Iterator.__next__(self.products)

    def __len__(self):
        """The number of products in an SRE.
        Usage
        -------
        len(s1)

        Returns
        -------
        [int]
        """
        return len(self.products)

    def __repr__(self):
        return ("SRE made with:\n"
                f"{set(self.products)}")
