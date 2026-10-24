"""Offline tests for the public reconstructed example (no physical plug needed)."""

import unittest
from examples.local_switch_check import relay_state


class RelayStateTests(unittest.TestCase):
    def test_on(self):
        self.assertTrue(relay_state({"dps": {"1": True, "2": 0}}))

    def test_off(self):
        self.assertFalse(relay_state({"dps": {"1": False}}))

    def test_missing_state(self):
        with self.assertRaises(ValueError):
            relay_state({"Error": "connection failed"})

    def test_wrong_type(self):
        with self.assertRaises(ValueError):
            relay_state({"dps": {"1": "false"}})


if __name__ == "__main__":
    unittest.main()
