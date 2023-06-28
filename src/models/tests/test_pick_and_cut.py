#   Created by Jiří Strouhal (2023).
#   Written in Python 3.10.10
#   Licensed under the MIT License. See the LICENSE in the project root folder. 
#   Public repository: https://github.com/jiristrouhal/opcut.
#   Use MznStrouhal@gmail.com to contact the author.

import sys
sys.path.append("./src")

import unittest
import models.pick_and_cut as pick_and_cut
from models.pick_and_cut import Raw, Combined_Length, Cutted_Raw


class Test_Single_Length(unittest.TestCase):
    
	def test_single_stock_type_of_the_same_lengths_as_required_length(self):
		lengths = [200]
		stock = [Raw(200,1000)]
		result = pick_and_cut.pickandcut(lengths,stock)
		self.assertListEqual(result.combined_lengths,[Combined_Length(200,[200])])
		self.assertListEqual(result.cutted_stock,[Cutted_Raw(200,[200])])
		self.assertDictEqual(result.order.items,{200:1})
		self.assertEqual(result.order.total_price,1000)
	
	def test_stock_of_fourth_length(self):
		lengths = [200]
		stock = [Raw(50,300)]
		result = pick_and_cut.pickandcut(lengths,stock)
		self.assertListEqual(result.combined_lengths,[Combined_Length(200,[50,50,50,50])])
		self.assertListEqual(
			result.cutted_stock,
			[
				Cutted_Raw(50,[50]), 
				Cutted_Raw(50,[50]),
				Cutted_Raw(50,[50]), 
				Cutted_Raw(50,[50])
			])
		self.assertDictEqual(result.order.items,{50:4})
		self.assertEqual(result.order.total_price,1200)

	def test_some(self):
		lengths = [150,80]
		stock = [Raw(110,2000), Raw(150,2500)]
		result = pick_and_cut.pickandcut(lengths, stock)
		self.assertListEqual(result.cutted_stock, [Cutted_Raw(150,[150]),Cutted_Raw(110,[80,30])])

if __name__=='__main__': unittest.main()