"""
Defines unittests for kedat.core module.
"""
import unittest
from unittest import TestCase
from .core import Storage



class StorageTestCase(TestCase):
    
    def test_is_instance_of_dict(self):
        s = Storage()
        self.assertIsInstance(s, dict)
    
    def test_can_access_element_using_dot_notation(self):
        foo = Storage()
        foo['bar'] = 'baz-qux-norf'
        self.assertEqual('baz-qux-norf', foo.bar)
    
    def test_can_set_element_using_dot_notation(self):
        foo = Storage()
        foo.bar = 'baz-qux-norf'
        self.assertEqual('baz-qux-norf', foo['bar'])
    
    def test_access_using_unknown_member_returns_None(self):
        foo = Storage()
        self.assertIsNone(foo.bar)
    
    def test_access_using_unknown_key_returns_None(self):
        foo = Storage()
        self.assertIsNone(foo['bar'])



if __name__ == '__main__':
    unittest.main()
    