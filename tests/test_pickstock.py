import unittest
import pickstock
from pickstock import Stock


class Test_Single_Length(unittest.TestCase):
    
	def test_single_stock_available(self):
		lengths = [100]
		available_stock = [Stock(100,1000)]
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertDictEqual(picked.items,{100:1})
		self.assertEqual(picked.cost,1000)

	def test_no_stock_provided(self):
		lengths = [100]
		empty_stock = []
		picked = pickstock.ecopick(lengths,empty_stock) 
		self.assertDictEqual(picked.items, {})
		self.assertEqual(picked.cost,0)

	def test_no_lengths_required(self):
		lengths = []
		available_stock = [Stock(20, 1500), Stock(40, 300)]
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertDictEqual(picked.items, {})
		self.assertEqual(picked.cost,0)

	def test_two_available_stock_types_with_equal_price_per_unit_length(self):
		lengths = [100]
		available_stock = [Stock(120,1200), Stock(150,1500)]
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertDictEqual(picked.items,{120:1})
		self.assertEqual(picked.cost,1200)


if __name__=='__main__':
    unittest.main()