#   Created by Jiří Strouhal (2023).
#   Written in Python 3.10.10
#   Licensed under the MIT License. See the LICENSE in the project root folder. 
#   Public repository: https://github.com/jiristrouhal/opcut.
#   Use MznStrouhal@gmail.com to contact the author.


import sys 
sys.path.insert(1,".")

import unittest
import validate_input as vi


class Test_Valid_Raw_Pieces_Input(unittest.TestCase):

    # A valid raw piece has format (#integer_length, #integer_price)
    # for example (450, 1200)

    # Multiple types are separated by semicolons, e.g.
    # (450, 6000); (780, 10000); (40, 800)

    # Extra spaces between and inside brackets are ignored
    # e.g. (  700,   8000)  ;   (300, 4000) is valid

    def test_empty_input_is_valid(self):
        self.assertTrue(vi.is_raw_valid(""))
        self.assertTrue(vi.is_raw_valid("  "))
        self.assertTrue(vi.is_raw_valid("\n"))
        self.assertTrue(vi.is_raw_valid("\t"))

    def test_single_correct_raw_piece_type_is_valid(self):
        self.assertTrue(vi.is_raw_valid("(125,1200)"))
        self.assertTrue(vi.is_raw_valid(" (125  ,  1200 ) "))

    def test_empty_or_incomplete_parenteses_are_invalid(self):
        self.assertFalse(vi.is_raw_valid("()"))
        self.assertFalse(vi.is_raw_valid("("))
        self.assertFalse(vi.is_raw_valid(")"))

    def test_item_with_missing_price_is_invalid(self):
        self.assertFalse(vi.is_raw_valid("(450)"))

    def test_item_containing_additional_numerical_values_is_invalid(self):
        self.assertFalse(vi.is_raw_valid("(125, 1200, 10)"))

    def test_two_valid_items_separated_with_semicolon_are_valid(self):
        self.assertTrue(vi.is_raw_valid("(450,1000); (900,2000)"))

    def test_two_items_separated_by_multiple_semicolons_are_valid(self):
        self.assertTrue(vi.is_raw_valid("(450,1000);;;;;;; (900,2000)"))

    def test_two_items_not_separated_with_semicolon_are_invalid(self):
        self.assertFalse(vi.is_raw_valid("(450,1000)(900,2000)"))
        self.assertFalse(vi.is_raw_valid("(450,1000) (900,2000)"))

    def test_input_containing_only_semicolons_is_valid(self):
        # This is basically an empty input
        self.assertTrue(vi.is_raw_valid(";"))
        self.assertTrue(vi.is_raw_valid(";;"))
        self.assertTrue(vi.is_raw_valid("  ;  ;; "))

    def test_adding_semicolons_to_valid_input_keeps_its_validity(self):
        # This is basically an empty input
        self.assertTrue(vi.is_raw_valid("(450,1000); (900,2000);"))
        self.assertTrue(vi.is_raw_valid("(450,1000); (900,2000);;;;;;"))


if __name__=="__main__":
    unittest.main()