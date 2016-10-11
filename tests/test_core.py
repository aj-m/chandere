import asyncio
import unittest

from chandere2.core import wrap_semaphore


## TODO: Does not test for the existence of a semaphore. <jakob@memeware.net>
class WrapSemaphoreTest(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_wrap_semaphore(self):
        async def dummy_coroutine():
            return True

        semaphore = asyncio.Semaphore(1)
        coroutine = wrap_semaphore(dummy_coroutine(), semaphore)
        self.assertTrue(self.loop.run_until_complete(coroutine))
