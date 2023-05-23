import unittest
import sortall
from sortall import Length, NotEnoughStockItems
from typing import List, Dict


class Test_Single_Length(unittest.TestCase):
    
	def test_for_single_length_and_stock_no_sorting_happens(self)->None:
		lengths:List[int] = [100]
		stock:Dict[int,int] = {100:1}
		sorted_lengths, sorted_stock = sortall.mincutsort(lengths,stock)

		self.assertListEqual(sorted_lengths,[Length(100,0)])
		self.assertListEqual(sorted_stock,[100])

	def test_sum_of_stock_lengths_raises_exception(self)->None:
		with self.assertRaises(NotEnoughStockItems):
			lengths:List[int] = [100]
			stock:Dict[int,int] = {}
			sortall.mincutsort(lengths,stock)


class Test_Two_Lengths(unittest.TestCase):
	
	def test_length_matching_stock_length_is_moved_to_coincide_with_the_stock(self):
		lengths = [100,150]
		stock = {150:2}
		sorted_lengths, sorted_stock = sortall.mincutsort(lengths,stock)
		self.assertListEqual(sorted_lengths,[Length(150,1),Length(100,0)])
		self.assertListEqual(sorted_stock,[150,150])


class Test_Multiple_Lengths(unittest.TestCase):

	def test_one_full_match_of_length_and_stock_and_one_match_of_sum_of_stocks_and_single_length(self):
		lengths = [120,100,250]
		stock = {100:2,150:2}
		sorted_lengths, sorted_stock = sortall.mincutsort(lengths,stock)
		self.assertListEqual(sorted_lengths,[Length(100,1),Length(250,2),Length(120,0)])
		self.assertListEqual(sorted_stock,[100,100,150,150])


if __name__=='__main__':
	unittest.main()