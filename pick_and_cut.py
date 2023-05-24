import pickstock,sortall,cut
from typing import List, Dict, Literal
import dataclasses


@dataclasses.dataclass
class Stock:
	length:int
	price:int


@dataclasses.dataclass
class Ordered_Stock:
	total_price:int
	items:Dict[int,int]


@dataclasses.dataclass
class Cutted_Stock:
	original_length:int
	pieces:List[int]


@dataclasses.dataclass
class Combined_Length:
	length:int
	pieces:List[int]


def pickandcut(lengths:List[int],stock:List[Stock], priority:Literal['cost','count','cost and count']='cost'):
	prepared_stock = [pickstock.Stock(s.length,s.price) for s in stock]
	raw_ordered_stock = pickstock.ecopick(lengths, prepared_stock, priority)
	sorted_lengths, sorted_stock = sortall.mincutsort(lengths,raw_ordered_stock.items,)
	prepared_sorted_lengths = [cut.Length(l.length,l.id) for l in sorted_lengths]
	raw_combined_lengths, raw_cutted_stock = cut.cut(prepared_sorted_lengths,sorted_stock)
	raw_combined_lengths.sort(key = lambda x: x.original.id)

	assert(sum([sum(l.pieces) for l in raw_combined_lengths]) <= sum([sum(s.pieces) for s in raw_cutted_stock]))

	combined_lengths:List[Combined_Length] = list()
	cutted_stock:List[Cutted_Stock] = list()
	for l in raw_combined_lengths:
		combined_lengths.append(Combined_Length(l.original.length, l.pieces))
	for s in raw_cutted_stock:
		cutted_stock.append(Cutted_Stock(s.original, s.pieces))
	ordered_stock = Ordered_Stock(raw_ordered_stock.cost,raw_ordered_stock.items)

	assert(sum([sum(l.pieces) for l in raw_combined_lengths]) == sum([sum(l.pieces) for l in combined_lengths]))

	return ordered_stock, combined_lengths, cutted_stock


def printcutted(cost:int, order:Dict[int,int],lengths:List[Combined_Length],stock:List[Cutted_Stock]):
	stock.sort(key= lambda x: x.original_length)

	print("Order:")
	print(f"\tTotal cost: {cost}")
	for length,count in order.items(): print(f"\t{length}: {count:3}×")
	print("Cutted stock:")
	for s in stock:
		print(f"\t{s.original_length:4} -> ",end='')
		for p in s.pieces:
			print(f"{p}, ",end='')
		print("")
	print("Combined lengths:")
	for l in lengths:
		print(f"\t{l.length:4} <- ",end='')
		for p in l.pieces:
			print(f"{p}, ",end='')
		print("")

