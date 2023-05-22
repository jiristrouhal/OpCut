import dataclasses
from typing import List, Dict


@dataclasses.dataclass(frozen=True)
class Stock:
	length:int
	price:int


@dataclasses.dataclass
class Picked:
	_cost:int = 0
	_items:Dict[int,int] = dataclasses.field(default_factory=dict)
	@property
	def cost(self)->int: return self._cost
	@property
	def items(self)->Dict[int,int]: return self._items

	def add_stock(self,stock:Stock)->None: 
		self._cost+=stock.price
		if stock.length not in self._items: 
			self._items[stock.length] = 1
		else: self._items[stock.length] += 1
	

def ecopick(lengths:List[int],available_stock:List[Stock])->Picked:
	if len(lengths)==0 or len(available_stock)==0: 
		return Picked()
	return _pick_to_cover_with_minimum_cost(sum(lengths),available_stock)


_memo:Dict[int,Picked] = dict()
def _pick_to_cover_with_minimum_cost(l:int,stock:List[Stock])->Picked:
	global _memo
	_memo = dict()
	picked = _pick_for_sublength(l,stock)
	return picked


def _pick_for_sublength(length:int,stock:List[Stock])->Picked:
	if length<=0: return Picked()

	global _memo
	if not length in _memo:_append_memo_with_new_sublength(length,stock)
	return _memo[length]


def _append_memo_with_new_sublength(length:int,stock:List[Stock])->None:
	global _memo
	lowest_found_cost = -1
	optimally_picked = Picked()
	for item in stock:
		picked = _pick_for_sublength(length-item.length, stock)
		cost = picked.cost+item.price
		if(lowest_found_cost>cost or lowest_found_cost==-1):
			lowest_found_cost = cost
			picked.add_stock(item)
			optimally_picked = picked
	_memo[length] = optimally_picked



