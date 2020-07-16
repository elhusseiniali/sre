class Iterator():
    """An iterator to allow us to iterate
    over the data structures.
    """
    def __init__(self, source):
        self.source = source
        self.count = 0

    def __next__(self):
        if self.count >= len(self.source):
            raise StopIteration

        self.count += 1
        return list(self.source)[self.count - 1]
