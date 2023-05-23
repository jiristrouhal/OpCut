from typing import List, Dict, Tuple
import dataclasses


@dataclasses.dataclass
class Length:
	length:int
	id:int


@dataclasses.dataclass
class Ordered_Stock:
	length:int
	count:int

	def take(self)->int: 
		if self.count>0: 
			self.count -= 1
			return self.length
		return 0
	
	def __str__(self)->str: 
		return "Length: "+str(self.length)+"; count: "+str(self.count)
	
	
	

class NotEnoughStockItems(Exception): pass
		

def mincutsort(lengths_list:List[int],stock_dict:Dict[int,int])->Tuple[List[Length],List[int]]:
	# The lengths list is converted into list of Length objects, which keep their original id
	# stored as an attribute for later use.
	__check_enough_stock_items(sum(lengths_list),stock_dict)

	lengths:List[Length] = __prepare_lengths_for_sorting(lengths_list)
	stock:List[Ordered_Stock] = __prepare_stock_for_taking(stock_dict)

	matching_lengths = __pick_lengths_and_stock_of_same_length(lengths,stock)
	remaining_sorted_lengths, remaning_sorted_stock = \
		__sort_unmatching_stock_and_lengths(lengths,stock)
	sorted_lengths = matching_lengths.copy() + remaining_sorted_lengths
	sorted_stock = [l.length for l in matching_lengths] + remaning_sorted_stock

	return sorted_lengths, sorted_stock


def __check_enough_stock_items(total_length, stock:Dict[int,int]):
	stock_length_sum = 0
	for length,count in stock.items(): stock_length_sum += length*count
	if stock_length_sum<total_length: raise NotEnoughStockItems
	

def __prepare_lengths_for_sorting(lengths:List[int])->List[Length]:
	return [Length(lengths[i],i) for i in range(len(lengths))]

def __prepare_stock_for_taking(stock:Dict[int,int])->List[Ordered_Stock]:
	ordered_stock:List[Ordered_Stock] = list()
	for length,count in stock.items():
		ordered_stock.append(Ordered_Stock(length,count))
	return ordered_stock


def __pick_lengths_and_stock_of_same_length(
	lengths:List[Length],
	stock:List[Ordered_Stock]
	)->List[Length]:

	matches:List[Length] = list()
	for stock_item in stock:
		for length_item in lengths:
			if (stock_item.length==length_item.length) and (stock_item.take()>0): 
				lengths.remove(length_item)
				matches.append(length_item)
	return matches


_memo:Dict[str,Tuple[int,List[Length],List[int]]] = dict()
def __sort_unmatching_stock_and_lengths(
	lengths:List[Length],
	stock:List[Ordered_Stock]
	)->Tuple[List[Length],List[int]]:

	sorted_stock:List[int] = list()
	sorted_lengths:List[Length] = lengths.copy()

	stock_length_sum = __sum_ordered_stock_lengths(stock)
	lengths_sum = __sum_lengths(lengths)
	
	global _memo
	_memo = dict()
	cuts, sorted_lengths, sorted_stock = \
		_maximize_matching_ends(lengths_sum,stock_length_sum,lengths,stock)
	print(cuts)
	return sorted_lengths, sorted_stock


def _maximize_matching_ends(
	l_sum:int, 
	s_sum:int, 
	l:List[Length], 
	s:List[Ordered_Stock]
	)->Tuple[int,List[Length],List[int]]:

	if s_sum==0: return 0, l.copy(), []
	elif l_sum==0:
		# if s_sum is not zero, exactly one piece of one item of stock list 's' should be available"
		return 0, [], [si.length for si in s if si.count>0]
	
	global _memo
	label=str(l)+str(s)
	if label in _memo: return _memo[label]

	# The highest possible maximum number of cuts corresponds to no match between ends
	# of lengths and the stock items. Add one to enable assigning some content to opt_sorted_## lists."
	score = len(l)+2
	opt_l:List[Length] = list()
	opt_s:List[int] = list()

	if l_sum>=s_sum:
		for li in l:
			reduced_lengths = l.copy()
			reduced_lengths.remove(li)
			cuts, sorted_l, sorted_s = _maximize_matching_ends(l_sum-li.length,s_sum,reduced_lengths,s.copy())
			if l_sum!=s_sum: cuts += 1 
			if cuts<max_cuts:
				max_cuts=cuts
				opt_l=sorted_l.copy()
				opt_l.append(li)
				opt_s=sorted_s.copy()

	else:
		for i in range(len(s)):
			reduced_stock = s.copy()
			taken_length = reduced_stock[i].take()
			if taken_length==0: continue
			cuts, sorted_l, sorted_s = _maximize_matching_ends(l_sum,s_sum-taken_length,l.copy(),reduced_stock)
			cuts += 1 
			if cuts<max_cuts:
				max_cuts=cuts
				opt_l=sorted_l.copy()
				opt_s=sorted_s.copy()
				opt_s.append(s[i].length)

	_memo[label] = (max_cuts, opt_l.copy(), opt_s.copy())
	return _memo[label]


def __sum_ordered_stock_lengths(stock:List[Ordered_Stock]):
	stock_length_sum = 0
	for item in stock: stock_length_sum += item.count*item.length
	return stock_length_sum

def __sum_lengths(lengths:List[Length]):
	lengths_sum = 0
	for item in lengths: lengths_sum += item.length
	return lengths_sum




