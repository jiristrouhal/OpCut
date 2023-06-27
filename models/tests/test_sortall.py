import sys
sys.path.insert(1,'D:/Users/MznSt/Desktop/BestCut/models')

import unittest
import sortall
from sortall import Length, NotEnoughRawItems, Ordered_Raw
from typing import List, Dict


class Test_Single_Length(unittest.TestCase):
    
	def test_for_single_length_and_stock_no_sorting_happens(self)->None:
		lengths:List[int] = [100]
		stock:Dict[int,int] = {100:1}
		sorted_lengths, sorted_stock = sortall.mincutsort(lengths,stock)

		self.assertListEqual(sorted_lengths,[Length(100,0)])
		self.assertListEqual(sorted_stock,[100])

	def test_sum_of_stock_lengths_raises_exception(self)->None:
		with self.assertRaises(NotEnoughRawItems):
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

	def test_all_lengths_equal(self):
		lengths = [100,100,100]
		stock = {110:3}
		sorted_lengths, sorted_stock = sortall.mincutsort(lengths,stock)
		self.assertListEqual(sorted_lengths,[Length(100,2),Length(100,1),Length(100,0)])
		self.assertListEqual(sorted_stock,[110,110,110])

	def test_one_full_match_of_length_and_stock_and_one_match_of_sum_of_stocks_and_single_length(self):
		lengths = [120,100,250]
		stock = {100:2,150:2}
		sorted_lengths, sorted_stock = sortall.mincutsort(lengths,stock)
		self.assertListEqual(sorted_lengths,[Length(100,1),Length(250,2),Length(120,0)])
		self.assertListEqual(sorted_stock,[100,100,150,150])

	def test_shorted_stock_than_lengths(self):
		lengths = [100,100,100]
		stock = {95:4}
		sorted_lengths, sorted_stock = sortall.mincutsort(lengths,stock)
		self.assertListEqual(sorted_lengths,[Length(100,2),Length(100,1),Length(100,0)])
		self.assertListEqual(sorted_stock,[95,95,95,95])

	def test_prefer_longer_distance_between_ends_even_they_dont_match(self):
		lengths = [105,95]
		stock = {90:1,110:1}
		sorted_lengths, sorted_stock = sortall.mincutsort(lengths,stock)
		self.assertListEqual(sorted_lengths,[Length(95,1),Length(105,0)])
		self.assertListEqual(sorted_stock, [110,90])


class Test_Sorting_Nonmatchinch_Lengths_And_Raw(unittest.TestCase):

	def test_single_length_and_stock_are_not_sorted(self):
		lengths = [Length(101,0)]
		stock = [Ordered_Raw(120,1)]
		sorted_lengths, sorted_stock = sortall._sort_remaining_stock_and_lengths(lengths,stock)
		self.assertListEqual(sorted_lengths, [Length(101,0)])
		self.assertListEqual(sorted_stock,[120])

	def test_two_lengths_with_single_stock_are_not_sorted(self):
		lengths = [Length(50,0), Length(70,1)]
		stock = [Ordered_Raw(130,1)]
		sorted_lengths, sorted_stock = sortall._sort_remaining_stock_and_lengths(lengths,stock)
		self.assertListEqual(sorted_lengths, [Length(50,0), Length(70,1)])
		self.assertListEqual(sorted_stock,[130])

	def test_two_lengths_with_two_stock_are_sorted_to_maximize_distance_between_ends(self):
		lengths = [Length(50,0), Length(70,1)]
		stock = [Ordered_Raw(65,1), Ordered_Raw(55,1)]
		sorted_lengths, sorted_stock = sortall._sort_remaining_stock_and_lengths(lengths,stock)
		self.assertListEqual(sorted_lengths, [Length(50,0), Length(70,1)])
		self.assertListEqual(sorted_stock,[65,55])


class Test_Unpacking_Ordered_Raw_To_Raw_Length_List(unittest.TestCase):

	def test_unpack_single_type_stock(self)->None:
		stock = [Ordered_Raw(100,2)]
		s_int = sortall._unpack_remaining_stock(stock)
		self.assertListEqual(s_int,[100,100])

	def test_unpack_two_types_of_stock(self)->None:
		stock = [Ordered_Raw(100,2), Ordered_Raw(200,1)]
		s_int = sortall._unpack_remaining_stock(stock)
		self.assertListEqual(s_int,[100,100,200])

	def test_upacking_stock_of_zero_count_leads_to_empty_list(self)->None:
		stock = [Ordered_Raw(100,0)]
		s_int = sortall._unpack_remaining_stock(stock)
		self.assertListEqual(s_int,[])


if __name__=='__main__':
	unittest.main()