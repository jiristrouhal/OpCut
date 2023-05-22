import dataclasses
from typing import List, Dict


@dataclasses.dataclass(frozen=True)
class Stock:
	length:int
	price:int




class Picked:
	_cost:int = 0
	_items:Dict[int,int] = dict()
	@property
	def cost(self)->int: return self._cost
	@property
	def items(self)->Dict[int,int]: return self._items

	def pick_stock(self,stock:Stock)->None: 
		self._cost+=stock.price
		if stock.length not in self._items: 
			self._items[stock.length] = 1
		else: self._items[stock.length] += 1
	

def ecopick(lengths:List[int],available_stock:List[Stock])->Picked:
	if len(lengths)==0 or len(available_stock)==0: return Picked()
	return _ecopick(lengths,available_stock)


def _ecopick(lengths:List[int],available_stock:List[Stock])->Picked:
	remaining_length = sum(lengths)
	picked = Picked()
	while remaining_length>0:
		remaining_length-=available_stock[0].length
		picked.pick_stock(available_stock[0])
	return picked


