import unittest
import sortall
from typing import List, Dict


class Test_Single_Length(unittest.TestCase):
    
	def test_for_single_length_and_stock_no_sorting_happens(self)->None:
		lengths:List[int] = [100]
		stock:Dict[int,int] = {100:1}
		sorted_lengths, sorted_stock = sortall.mincutsort(lengths,stock)
		print(sorted_lengths)
		self.assertListEqual(sorted_lengths,[100])
		self.assertListEqual(sorted_stock,[100])


class Test_Two_Lengths(unittest.TestCase):
	
	def test_one_length_matching_stock_length_is_moved_to_coincide_with_the_stock(self):
		lengths = [100,150]
		stock = {150:2}
		sorted_lengths, sorted_stock = sortall.mincutsort(lengths,stock)
		self.assertListEqual(sorted_lengths,[150,100])
		self.assertListEqual(sorted_stock,[150,150])



if __name__=='__main__':
	unittest.main()