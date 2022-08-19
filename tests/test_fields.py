import unittest

from superspreader.exceptions import ValidationException
from superspreader.fields import BaseField


class TestField(BaseField):
    target_type = int


class BaseFieldTestCase(unittest.TestCase):
    def test_required(self):
        test_field = TestField(source="test")

        with self.assertRaises(ValidationException) as cm:
            test_field(None, "en")

        self.assertEqual(cm.exception.msg, "Field test is required")

        # Reverse case.
        value = test_field(666, "en")
        self.assertEqual(value, 666)

    def test_wrong_type(self):
        test_field = TestField(source="test")

        with self.assertRaises(ValidationException) as cm:
            test_field("I’m a string", "en")

        self.assertEqual(
            cm.exception.msg, "Field test should be of type int, but it’s of type str"
        )
