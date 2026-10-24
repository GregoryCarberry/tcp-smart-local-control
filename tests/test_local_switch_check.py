"""Offline tests for the reconstructed status/toggle example.

These tests do not contact devices, inspect memory or use real keys.
"""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "examples" / "local_switch_check.py"
spec = importlib.util.spec_from_file_location("local_switch_check", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RelayStateTests(unittest.TestCase):
    def test_true(self):
        self.assertIs(module.relay_state({"dps": {"1": True}}), True)

    def test_false(self):
        self.assertIs(module.relay_state({"dps": {"1": False}}), False)

    def test_missing_relay(self):
        with self.assertRaises(ValueError):
            module.relay_state({"dps": {"2": 0}})

    def test_non_boolean_relay(self):
        with self.assertRaises(ValueError):
            module.relay_state({"dps": {"1": 1}})

    def test_error_result(self):
        with self.assertRaises(ValueError):
            module.relay_state({"Error": "unavailable"})


if __name__ == "__main__":
    unittest.main()
