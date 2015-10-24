"""
Defines unittests for kedat.core module.
"""
import os
import unittest
from unittest import TestCase

from .core import Storage, XlSheet
from openpyxl.reader.excel import load_workbook



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


class XlSheetTestCase(TestCase):
    base_dir = os.path.dirname(__file__)
    
    def _get_xlsheet(self, sheet_name='students', row_offset=0):
        filepath = os.path.join(self.base_dir, 'fixtures', 'school.xlsx')
        xsht = XlSheet(filepath, sheet_name, row_offset=row_offset)
        return xsht
    
    def test_can_be_created_using_workbook_filepath(self):
        xsht = self._get_xlsheet()
        self.assertIsNotNone(xsht)
    
    def test_cannot_create_from_non_existing_file(self):
        filepath = '/tmp/schools.xlsx'
        with self.assertRaises(FileNotFoundError):
            XlSheet(filepath, 'students')
    
    def test_can_be_created_using_workbook_object(self):
        filepath = os.path.join(self.base_dir, 'fixtures', 'school.xlsx')
        wb = load_workbook(filepath)
        xsht = XlSheet(wb, 'students')
        self.assertIsNotNone(xsht)
    
    def test_cannot_create_from_non_Workbook_object(self):
        wb = object()
        with self.assertRaises(ValueError):
            XlSheet(wb, 'students')
    
    def test_can_iterate_rows_using_object(self):
        idx = 0
        for row in self._get_xlsheet():
            idx += 1
            self.assertIsNotNone(row)
        self.assertEqual(12, idx)
    
    def test_can_iterate_rows_using_next(self):
        xsht = self._get_xlsheet()
        idx, row = 0, xsht.next()
        try:
            while (row != None):
                idx += 1
                row = xsht.next()
        except:  # catches StopIteration exception throw at end of iteration
            pass
        self.assertEqual(12, idx)
    
    def test_can_iterate_rows_beginning_at_an_offset(self):
        idx = 1
        for row in self._get_xlsheet(row_offset=5):
            idx += 1
        self.assertEqual(8, idx)
    
    def test_can_combine_next_and_object_iteration_for_enumeration(self):
        xsht = self._get_xlsheet()
        for i in range(5):
            row = xsht.next()
        
        for r in xsht:
            i += 1
        self.assertEqual(11, i)
    
    def test_can_reset_iteration_halfway_using_row_offset_attribute(self):
        xsht = self._get_xlsheet()
        for i in range(7):
            row = xsht.next()
        self.assertEqual('sn', row[0])
        
        xsht.row_offset = 0
        for i in range(9):
            row = xsht.next()
        self.assertEqual(2, row[0])
        self.assertEqual('Jane Doe', row[1]) 
    
    def test_can_reset_iteration_calling_reset(self):
        xsht = self._get_xlsheet()
        for i in range(7):
            row = xsht.next()
        self.assertEqual('sn', row[0])
        
        xsht.reset()
        for i in range(9):
            row = xsht.next()
        self.assertEqual(2, row[0])
        self.assertEqual('Jane Doe', row[1])
    
    def test_can_find_headers_using_valid_samples(self):
        xsht = self._get_xlsheet()
        hdr_idx = XlSheet.find_headers(xsht, ['sn', 'name'])
        self.assertEqual(7, hdr_idx)
    
    def test_cant_find_headers_using_invalid_samples(self):
        xsht = self._get_xlsheet()
        hdr_idx = XlSheet.find_headers(xsht, ['sn', 'age'])
        self.assertEqual(-1, hdr_idx)
    
    def test_can_apply_offset_and_find_headers_using_valid_samples(self):
        xsht = self._get_xlsheet( )
        hdr_idx = XlSheet.find_headers(xsht, ['sn', 'name'], row_offset=4)
        self.assertEqual(7, hdr_idx)
    
    def test_can_limit_number_rows_checked_to_find_headers(self):
        xsht = self._get_xlsheet()
        XlSheet.max_row_check = 4
        hdr_idx = XlSheet.find_headers(xsht, ['sn', 'name'])
        self.assertEqual(-1, hdr_idx)
    



if __name__ == '__main__':
    unittest.main()
    