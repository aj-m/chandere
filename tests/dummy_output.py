class FakeOutput(object):
    # Not yet.
    #
    # def __init__(self):
    #     self.last_received = []

    def write(self, *args):
        self.last_received = " ".join(args)
