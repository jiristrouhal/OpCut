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


if __name__=="__main__":
    unittest.main()