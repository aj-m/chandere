# import argparse

# from chandere2.core import main
# from chandere2.output import Console

# from tests.dummy_output import FakeOutput


# class FakeParser(object):
#     def __init__(self):
#         self.namespace = argparse.Namespace()

#     def parse_args(self):
#         return self.namespace


# class TestBlackBox:
#     def test_trial_connections(self):
#         self.args = FakeParser()
#         self.stdout = FakeOutput()
#         self.stderr = FakeOutput()
#         self.output = Console(output=self.stdout, error=self.stderr)
#         self.args.namespace.output = "."
#         self.args.namespace.mode = None
#         self.args.namespace.output_format = "ascii"
#         self.args.namespace.filters = []
#         self.args.namespace.ssl = False
#         self.args.namespace.targets = ["/g/"]
#         self.args.namespace.imageboard = "4chan"
#         main(self.args, self.output)
#         # assert ">" in self.stdout.last_received
#         # self.args.namespace.targets = ["/tech/"]
#         # self.args.namespace.imageboard = "8chan"
#         # main(self.args, self.output)
#         # assert ">" in self.stdout.last_received
#         # self.args.namespace.targets = ["/λ/"]
#         # self.args.namespace.imageboard = "lainchan"
#         # main(self.args, self.output)
#         # assert ">" in self.stdout.last_received
