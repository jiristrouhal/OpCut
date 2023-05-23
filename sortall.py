from typing import List, Dict, Tuple
import dataclasses


@dataclasses.dataclass
class Ordered_Stock:
	_length:int
	_count:int
	
	def take(self)->int: 
		if self._count>0: 
			self._count -= 1
			return self._length
		return 0
		

def mincutsort(lengths:List[int],stock:Dict[int,int])->Tuple[List[int],List[int]]:
	sorted_lengths:List[int] = lengths.copy()
	ord_stock:List[Ordered_Stock] = __prepare_stock_for_taking(stock)
	sorted_stock:List[int] = list()
	while True:
		added_stock = ord_stock[0].take()
		if added_stock==0: break
		sorted_stock.append(added_stock)
	return sorted_lengths, sorted_stock
	

def __prepare_stock_for_taking(stock:Dict[int,int])->List[Ordered_Stock]:
	ordered_stock:List[Ordered_Stock] = list()
	for length,count in stock.items():
		ordered_stock.append(Ordered_Stock(length,count))
	return ordered_stock