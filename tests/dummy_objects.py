class FakeOutput(object):
    def write(self, *args):
        self.last_received = " ".join(args)
