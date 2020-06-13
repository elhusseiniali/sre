
class StarAtom():
    """
    A star atom is an atom of the form (p1 + ... + pn)*
    """
    def __init__(self, *args):
        self.value = set(args)


class LetterAtom():
    """
    A letter-atom is an atom of the form a+Ɛ
    """
    def __init__(self, letter):
        self.value = letter


class Product():
    """
    A product is a concatenation (a list) of atoms.
    """
    def __init__(self, *args):
        """
        TODO:
            - Check that args only has atoms
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
            - Check that args only has products
            - Make immutable
        """
        self.value = set(args)
