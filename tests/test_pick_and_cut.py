import unittest
import pick_and_cut
from pick_and_cut import Stock, Combined_Length, Cutted_Stock


class Test_Single_Length(unittest.TestCase):
    
	def test_single_stock_type_of_the_same_lengths_as_required_length(self):
		lengths = [200]
		stock = [Stock(200,1000)]
		result = pick_and_cut.pickandcut(lengths,stock)
		self.assertListEqual(result.combined_lengths,[Combined_Length(200,[200])])
		self.assertListEqual(result.cutted_stock,[Cutted_Stock(200,[200])])
		self.assertDictEqual(result.order.items,{200:1})
		self.assertEqual(result.order.total_price,1000)
	
	def test_stock_of_fourth_length(self):
		lengths = [200]
		stock = [Stock(50,300)]
		result = pick_and_cut.pickandcut(lengths,stock)
		self.assertListEqual(result.combined_lengths,[Combined_Length(200,[50,50,50,50])])
		self.assertListEqual(
			result.cutted_stock,
			[
				Cutted_Stock(50,[50]), 
				Cutted_Stock(50,[50]),
				Cutted_Stock(50,[50]), 
				Cutted_Stock(50,[50])
			])
		self.assertDictEqual(result.order.items,{50:4})
		self.assertEqual(result.order.total_price,1200)


if __name__=='__main__': unittest.main()