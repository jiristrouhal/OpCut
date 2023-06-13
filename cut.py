from typing import List, Protocol, Tuple
import dataclasses


@dataclasses.dataclass
class Length_P(Protocol):
	length:int
	id:int


@dataclasses.dataclass
class Length:
	length:int
	id:int=0


@dataclasses.dataclass
class Combined_Length:
	original:Length
	pieces:List[int]


@dataclasses.dataclass
class Cutted_Raw:
	original:int
	pieces:List[int]


def cut(lengths:List[Length],stock:List[int])->Tuple[List[Combined_Length],List[Cutted_Raw]]:
	cutted_lengths:List[Combined_Length] = list()
	cutted_stock:List[Cutted_Raw] = list()

	for l in lengths: cutted_lengths.append(Combined_Length(l,[]))
	for s in stock: cutted_stock.append(Cutted_Raw(s,[]))

	for l in lengths: assert(l.length>0)
	for s in stock: assert(s>0)

	i,j = 0,0
	dist_to_length_end = lengths[i].length
	dist_to_stock_end = stock[j]

	m,n = len(lengths), len(stock)

	while not (i==m or j==n):
		if dist_to_length_end<dist_to_stock_end:
			cutted_lengths[i].pieces.append(dist_to_length_end)
			cutted_stock[j].pieces.append(dist_to_length_end)

			assert(cutted_stock[j].pieces[-1]>0)
			assert(cutted_lengths[i].pieces[-1]>0)

			i += 1
			dist_to_stock_end -= dist_to_length_end
			if i<m: dist_to_length_end = lengths[i].length
			else: cutted_stock[j].pieces.append(dist_to_stock_end)
		else:
			cutted_lengths[i].pieces.append(dist_to_stock_end)
			cutted_stock[j].pieces.append(dist_to_stock_end)
			j += 1
			dist_to_length_end -= dist_to_stock_end
			if j<n: dist_to_stock_end = stock[j]
			if dist_to_length_end==0: 
				i += 1
				if i<m: dist_to_length_end = lengths[i].length

	return cutted_lengths, cutted_stock



