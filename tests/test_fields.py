import unittest

from superspreader.exceptions import ValidationException
from superspreader.fields import BaseField, TimecodeField


class DummyField(BaseField):
    target_type = int


class BaseFieldTestCase(unittest.TestCase):
    def test_required(self):
        test_field = DummyField(source="test")

        with self.assertRaises(ValidationException) as cm:
            test_field(None, "en")

        self.assertEqual(cm.exception.msg, "Field test is required")

        test_field = DummyField(source="test", required=False)
        self.assertEqual(test_field(None, language="en"), None)

        # Reverse case.
        value = test_field(666, "en")
        self.assertEqual(value, 666)

    def test_wrong_type(self):
        test_field = DummyField(source="test")

        with self.assertRaises(ValidationException) as cm:
            test_field("I’m a string", "en")

        self.assertEqual(
            cm.exception.msg, "Field test should be of type int, but it’s of type str"
        )

    def test_timecode_field(self):
        test_field = TimecodeField(source="test")
        timecode_str = "00:13:06,9"
        invalid_timecode_str = "asdf123"

        value = test_field(timecode_str, language="en")
        self.assertEqual(value, 786.9)

        with self.assertRaises(ValidationException) as cm:
            test_field(invalid_timecode_str, language="en")

        self.assertEqual(cm.exception.msg, "Field test has an invalid format: asdf123")
