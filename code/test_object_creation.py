from models import Alphabet


class TestAlphabet():
    def test_single_letter(self):
        alph = Alphabet('a')
        assert 'a' in alph.letters
