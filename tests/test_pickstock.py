import unittest
import pickstock
from pickstock import Stock


class Test_Single_Length(unittest.TestCase):
    
	def test_single_stock_available(self):
		lengths = [100]
		available_stock = [available_stock(100,1000)]
		picked = pickstock.ecopick(lengths,available_stock)
		self.assertListEqual(picked.items,[100])
		self.assertEqual(picked.cost,1000)


if __name__=='__main__':
    unittest.main()