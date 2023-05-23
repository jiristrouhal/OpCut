import unittest
import sortall
from typing import List, Dict


class Test_Single_Length(unittest.TestCase):
    
	def test_for_single_length_and_stock_no_sorting_happens(self)->None:
		lengths:List[int] = [100]
		stock:Dict[int,int] = {100:1}
		sorted_lenghts, sorted_stock = sortall.mincutsort(lengths,stock)
		self.assertListEqual(lengths,sorted_lenghts)
		self.assertListEqual(sorted_stock,[100])




if __name__=='__main__':
	unittest.main()