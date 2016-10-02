import unittest

from chandere2.handle_targets import get_threads


## TODO: Improve test. <jakob@memeware.net>
class GetThreadsTest(unittest.TestCase):
    def test_get_threads(self):
        content = [{"threads":[{"no":589254,"last_modified":1473600302}]}]
        self.assertEqual(list(get_threads(content, "g", "4chan")),
                         ["a.4cdn.org/g/thread/589254.json"])
