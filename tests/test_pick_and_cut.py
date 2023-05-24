import unittest
import pick_and_cut
from pick_and_cut import Stock, Combined_Length, Cutted_Stock


class Test_Single_Length(unittest.TestCase):
    
	def test_single_stock_type_of_the_same_lengths_as_required_length(self):
		lengths = [200]
		stock = [Stock(200,1000)]
		ordered_stock, combined_lengths, cutted_stock = pick_and_cut.pickandcut(lengths,stock)
		self.assertListEqual(combined_lengths,[Combined_Length(200,[200])])
		self.assertListEqual(cutted_stock,[Cutted_Stock(200,[200])])
		self.assertDictEqual(ordered_stock.items,{200:1})


if __name__=='__main__': unittest.main()