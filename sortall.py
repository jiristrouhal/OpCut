from typing import List, Dict, Tuple
import dataclasses


@dataclasses.dataclass
class Ordered_Stock:
	length:int
	_count:int

	def take(self)->int: 
		if self._count>0: 
			self._count -= 1
			return self.length
		return 0
		

def mincutsort(lengths:List[int],stock_dict:Dict[int,int])->Tuple[List[int],List[int]]:
	stock:List[Ordered_Stock] = __prepare_stock_for_taking(stock_dict)

	matching_lengths = __pick_lengths_and_stock_of_same_length(lengths,stock)
	sorted_lengths = matching_lengths.copy() + lengths
	sorted_stock = matching_lengths.copy()

	k=0
	while k<len(stock):
		next_item_length = stock[k].take()
		if next_item_length==0: 
			k+=1
			continue
		else:
			sorted_stock.append(next_item_length)

	return sorted_lengths, sorted_stock
	

def __prepare_stock_for_taking(stock:Dict[int,int])->List[Ordered_Stock]:
	ordered_stock:List[Ordered_Stock] = list()
	for length,count in stock.items():
		ordered_stock.append(Ordered_Stock(length,count))
	return ordered_stock


def __pick_lengths_and_stock_of_same_length(
	lengths:List[int],
	stock:List[Ordered_Stock]
	)->List[int]:

	matches:List[int] = list()
	for item in stock:
		if (item.length in lengths) and (item.take()>0): 
			lengths.remove(item.length)
			matches.append(item.length)
	return matches
