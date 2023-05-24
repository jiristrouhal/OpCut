from __future__ import annotations
import dataclasses
from typing import List, Dict, Literal


COST = 'cost'
COUNT = 'count'
COST_AND_COUNT = 'cost and count'


@dataclasses.dataclass(frozen=True)
class Stock:
	length:int
	price:int
	def __new__(cls,length:int,price:int)->Stock:
		if length<=0:
			raise ValueError(f"Stock can have only positive length (curent value: {length}).")
		if price<=0:
			raise ValueError(f"Stock can have only positive price (current value: {price}).")
		return super().__new__(cls)


@dataclasses.dataclass
class Picked:
	cost:int = 0
	items:Dict[int,int] = dataclasses.field(default_factory=dict)

	@property
	def total_length(self)->int: 
		totlength = 0
		for length, count in self.items.items(): totlength += length*count
		return totlength

	@property
	def n_of_items(self)->int: 
		n = 0
		for nitems in self.items.values():
			n+=nitems
		return n
	
	def __repr__(self)->str:
		return f"Picked(cost={self.cost}, items={self.items}, total_length={self.total_length})"

	def add_stock(self, stock:Stock)->None: 
		self.cost += stock.price
		if stock.length not in self.items: 
			self.items[stock.length] = 1
		else: self.items[stock.length] += 1

	def copy(self)->Picked:
		new = Picked()
		new.items = self.items.copy()
		new.cost = self.cost
		return new


_priority:str = ""
_memo:Dict[int,Picked] = dict()
def ecopick(lengths:List[int],stock:List[Stock],priority:Literal['cost','count','cost and count']='cost')->Picked:
	global _memo, _priority

	_priority = priority
	if not bool(stock): return __pick_nothing()
	__raise_exception_if_some_nonpositive_length(lengths)

	__empty_memo()
	# sort to prevent program from skipping stock, which's cost and length is multiple of some
	# previously tried. After the sort, the program saves results for the longer stock.
	stock.sort(key=lambda x: x.length, reverse=True)
	picked = __pick_for_sublength(sum(lengths),stock)
	return picked


def __pick_nothing()->Picked:
	picked = Picked()
	return picked


def __empty_memo()->None:
	global _memo 
	_memo=dict()


def __raise_exception_if_some_nonpositive_length(lengths:List[int]):
	for length in lengths:
		if length<=0: raise ValueError(f"Specify positive lengths (found length {length}).")


def __pick_for_sublength(sublength:int, stock:List[Stock])->Picked:
	if sublength<=0: return __pick_nothing()

	global _memo
	best = Picked()
	if not sublength in _memo: 
		best = __pick_for_sublength(sublength-stock[0].length, stock)
		best.add_stock(stock[0])
		for i in range(1,len(stock)):
			new = __pick_for_sublength(sublength-stock[i].length, stock)
			new.add_stock(stock[i])
			best = __choose(best,new)
		_memo[sublength] = best
	# Do not return the original memo (in other case, the memo contents would be rewritten later).
	return _memo[sublength].copy()


def __choose(best:Picked,new:Picked):
	global _priority
	match _priority:
		case 'cost': return __choose_by_least_cost(best,new)
		case 'count': return __choose_by_least_count(best,new)
		case 'cost and count': return __choose_by_compromise_of_least_count_and_cost(best,new)


def __choose_by_least_cost(best:Picked, new:Picked)->Picked:
	if(new.cost<best.cost): return new
	elif(new.cost>best.cost): return best
	else:
		if new.n_of_items<best.n_of_items: 
			return new
	return best


def __choose_by_least_count(best:Picked, new:Picked)->Picked:
	if(new.n_of_items<best.n_of_items): return new
	elif(new.n_of_items>best.n_of_items): return best
	else:
		if new.cost<best.cost: 
			return new
	return best


def __choose_by_compromise_of_least_count_and_cost(best:Picked,new:Picked)->Picked:
	x = (new.n_of_items*new.cost)/(best.n_of_items*best.cost)
	if x<1: return new
	elif(x>1): return best
	else:
		if new.total_length>best.total_length: return new
		else: return best

