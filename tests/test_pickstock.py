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
		self.assertEqual(picked.total_length,100)

	def test_single_stock_available_and_two_items_needed(self):
		lengths = [100]
		available_stock = [Stock(50,500)]
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertDictEqual(picked.items,{50:2})
		self.assertEqual(picked.cost,1000)

	def test_single_stock_available_and_two_items_needed_with_small_waste(self):
		lengths = [100]
		available_stock = [Stock(60,600)]
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertDictEqual(picked.items,{60:2})
		self.assertEqual(picked.cost,1200)

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

	def test_from_two_equally_costly_options_select_the_one_with_less_items_with_zero_waste(self):
		lengths = [100]
		available_stock = [Stock(50,500), Stock(100,1000)]
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertDictEqual(picked.items,{100:1})

	def test_from_two_equally_costly_options_select_the_one_with_less_items_with_nonzero_waste(self):
		lengths = [100]
		available_stock = [Stock(60,600), Stock(120,1200)]
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertDictEqual(picked.items,{120:1})

	def test_nonpositive_length_raises_exception(self):
		lengths = [-100]
		stock = [Stock(50, 500)]
		with self.assertRaises(ValueError):
			pickstock.ecopick(lengths,stock)
		lengths = [0]
		with self.assertRaises(ValueError):
			pickstock.ecopick(lengths,stock)

	def test_nonpositive_stock_length_or_stock_cost_raises_exception(self):
		with self.assertRaises(ValueError): Stock(-50, 500)
		with self.assertRaises(ValueError): Stock(0, 500)
		with self.assertRaises(ValueError): Stock(50, -500)
		with self.assertRaises(ValueError): Stock(50, 0)


import random
N_OF_RANDOM_TESTS = 50
class Test_Multiple_Lengths(unittest.TestCase):

	def test_single_stock_type_of_same_lengths_as_required_lengths(self):
		lengths = [100,100]
		available_stock = [Stock(100,1000)]
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertDictEqual(picked.items,{100:2})
		self.assertEqual(picked.cost,2000)

	def test_no_stock_available_yields_empty_pick(self):
		lengths = [100,100]
		available_stock = []
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertDictEqual(picked.items,{})
		self.assertEqual(picked.cost,0)

	def test_two_available_stock_types_with_equal_price_per_unit_length(self):
		lengths = [100,100,100]
		available_stock = [Stock(400,4000),Stock(500,5000)]
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertDictEqual(picked.items,{400:1})

	def test_from_two_equally_costly_options_select_the_one_with_less_items(self):
		lengths = [100,100,100]
		available_stock = [Stock(50,500), Stock(100,1000)]
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertEqual(picked.total_length,300)
		self.assertDictEqual(picked.items,{100:3})

	def test_from_equally_costly_options_select_the_one_with_larger_waste(self):
		lengths = [100,100,100]
		available_stock = [Stock(150,1500), Stock(170,1500), Stock(160,1500), Stock(155,1500)]
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertEqual(picked.total_length,340)
		self.assertDictEqual(picked.items,{170:2})

	def test_randomly(self):
		for _ in range(N_OF_RANDOM_TESTS):
			lengths = [random.randint(1,100) for _ in range(random.randint(1,10))]
			stock = [Stock(random.randint(1,200),random.randint(1,2000)) for _ in range(random.randint(1,6))]
			picked = pickstock.ecopick(lengths,stock)
			self.assertTrue(picked.total_length>=sum(lengths))

if __name__=='__main__':
    unittest.main()