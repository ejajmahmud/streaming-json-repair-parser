"""Tests for Streaming JSON Repair Parser."""
import unittest
from streaming_json_repair_parser.core import StreamingJSONRepair


class TestStreamingJSONRepair(unittest.TestCase):
    def setUp(self):
        self.repair = StreamingJSONRepair()

    def test_closes_nested_array_and_string(self):
        obj = self.repair.parse_partial('{"tool": "grep", "paths": ["a.py", "b.p')
        self.assertEqual(obj, {"tool": "grep", "paths": ["a.py", "b.p"]})

    def test_fills_dangling_colon_with_null(self):
        obj = self.repair.parse_partial('{"a": 1, "b":')
        self.assertEqual(obj, {"a": 1, "b": None})

    def test_drops_incomplete_key_before_colon(self):
        obj = self.repair.parse_partial('{"a": 1, "incomp')
        self.assertEqual(obj, {"a": 1})

    def test_handles_escaped_quotes_inside_string(self):
        obj = self.repair.parse_partial(r'{"msg": "say \"hi')
        self.assertEqual(obj, {"msg": 'say "hi'})
