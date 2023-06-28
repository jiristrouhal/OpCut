#   Created by Jiří Strouhal (2023).
#   Written in Python 3.10.10
#   Licensed under the MIT License. See the LICENSE in the project root folder. 
#   Public repository: https://github.com/jiristrouhal/opcut.
#   Use MznStrouhal@gmail.com to contact the author.


from typing import List, Dict, Tuple
import dataclasses


@dataclasses.dataclass
class Length:
	length:int
	id:int


@dataclasses.dataclass
class Ordered_Raw:
	length:int
	count:int

	def take(self)->int: 
		if self.count>0: 
			self.count -= 1
			return self.length
		return 0
	
	def put_back(self)->None:
		self.count += 1
	
	def __str__(self)->str: 
		return "Length: "+str(self.length)+"; count: "+str(self.count)
	

class NotEnoughRawItems(Exception): pass
		

def mincutsort(lengths_list:List[int],stock_dict:Dict[int,int])->Tuple[List[Length],List[int]]:
	# The lengths list is converted into list of Length objects, which keep their original id
	# stored as an attribute for later use.
	__raise_if_not_enough_stock(sum(lengths_list),stock_dict)

	lengths:List[Length] = __append_original_list_ids_to_lengths(lengths_list)
	stock:List[Ordered_Raw] = __convert_stock_dict_to_ordered_stock_objects(stock_dict)

	already_ok_stock, remaining_lengths, remaining_stock = __pick_stock_that_does_not_to_be_cut(lengths,stock)

	sorted_lengths_to_be_combined, sorted_stock_to_be_cutted = \
		_sort_remaining_stock_and_lengths(remaining_lengths, remaining_stock)
	
	sorted_lengths = already_ok_stock.copy() + sorted_lengths_to_be_combined
	sorted_stock = [l.length for l in already_ok_stock] + sorted_stock_to_be_cutted

	return sorted_lengths, sorted_stock


def __raise_if_not_enough_stock(total_length, stock:Dict[int,int]):
	stock_length_sum = 0
	for length,count in stock.items(): stock_length_sum += length*count
	if stock_length_sum<total_length: raise NotEnoughRawItems
	

def __append_original_list_ids_to_lengths(lengths:List[int])->List[Length]:
	return [Length(lengths[i],i) for i in range(len(lengths))]


def __convert_stock_dict_to_ordered_stock_objects(stock:Dict[int,int])->List[Ordered_Raw]:
	ordered_stock:List[Ordered_Raw] = list()
	for length,count in stock.items():
		ordered_stock.append(Ordered_Raw(length,count))
	return ordered_stock


def __pick_stock_that_does_not_to_be_cut(
	lengths:List[Length],
	stock:List[Ordered_Raw]
	)->Tuple[List[Length],List[Length],List[Ordered_Raw]]:

	matches:List[Length] = list()
	for stock_item in stock:
		for length_item in lengths:
			if (stock_item.length==length_item.length) and (stock_item.take()>0): 
				lengths.remove(length_item)
				matches.append(length_item)
	return matches, lengths.copy(), stock.copy()


_memo:Dict[str,Tuple[int,int,List[Length],List[int]]] = dict()
def _sort_remaining_stock_and_lengths(
	lengths:List[Length],
	stock:List[Ordered_Raw]
	)->Tuple[List[Length],List[int]]:

	sorted_stock:List[int] = list()
	sorted_lengths:List[Length] = lengths.copy()

	stock_length_sum = __sum_ordered_stock_lengths(stock)
	lengths_sum = __sum_lengths(lengths)
	
	global _memo
	_memo = dict()
	score_1, score_2, sorted_lengths, sorted_stock = \
		__maximize_matching_ends(lengths_sum,stock_length_sum,lengths,stock)
	
	assert(sum([l.length for l in sorted_lengths])==lengths_sum)
	assert(sum(sorted_stock)==stock_length_sum)

	return sorted_lengths, sorted_stock


def __maximize_matching_ends(
	l_sum:int, 
	s_sum:int, 
	l:List[Length], 
	s:List[Ordered_Raw]
	)->Tuple[int,int,List[Length],List[int]]:

	if s_sum==0: return 0,0,l.copy(),[]
	elif l_sum==0: return 0, 0, [], _unpack_remaining_stock(s)
	
	global _memo
	label=str(l)+str(s)
	if label in _memo: return _memo[label]

	# The highest possible maximum number of cuts corresponds to no match between ends
	# of lengths and the stock items. Add one to enable assigning some content to opt_sorted_## lists."
	max_score_1, max_score_2 = -1, -1
	opt_l:List[Length] = list()
	opt_s:List[int] = list()

	ls_sum_diff = l_sum-s_sum
	ls_sum_diff2 = ls_sum_diff*ls_sum_diff

	if ls_sum_diff>=0:
		for i in range(len(l)):
			li = l.pop(i)
			score_1, score_2, sorted_l, sorted_s = \
				__maximize_matching_ends(l_sum-li.length,s_sum,l.copy(),s)
			l.insert(i,li)
			score_1 += 1 if ls_sum_diff==0 else 0
			score_2 += ls_sum_diff2
			if (score_1>max_score_1) or (score_1==max_score_1 and score_2>max_score_2):
				max_score_1=score_1
				max_score_2=score_2
				opt_l=sorted_l.copy()
				opt_l.append(li)
				opt_s=sorted_s.copy()

	else:
		for si in s:
			taken_length = si.take()
			if taken_length==0: continue
			score_1, score_2, sorted_l, sorted_s = \
				__maximize_matching_ends(l_sum,s_sum-taken_length,l,s.copy())
			si.put_back()
			score_2 += ls_sum_diff2
			if (score_1>max_score_1) or (score_1==max_score_1 and score_2>max_score_2):
				max_score_1=score_1
				max_score_2=score_2
				opt_l=sorted_l.copy()
				opt_s=sorted_s.copy()
				opt_s.append(taken_length)

	_memo[label] = (max_score_1, max_score_2, opt_l.copy(), opt_s.copy())
	return _memo[label]


def _unpack_remaining_stock(s:List[Ordered_Raw])->List[int]:
	s_list:List[int] = []
	for si in s:
		s_list += [si.length]*si.count
	return s_list


def __sum_ordered_stock_lengths(stock:List[Ordered_Raw]):
	stock_length_sum = 0
	for item in stock: stock_length_sum += item.count*item.length
	return stock_length_sum


def __sum_lengths(lengths:List[Length]):
	lengths_sum = 0
	for item in lengths: lengths_sum += item.length
	return lengths_sum




