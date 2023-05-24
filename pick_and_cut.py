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


@dataclasses.dataclass
class Picked_And_Cutted:
	order:Ordered_Stock
	combined_lengths:List[Combined_Length]
	cutted_stock:List[Cutted_Stock]


def pickandcut(lengths:List[int],stock:List[Stock], priority:Literal['cost','count','cost and count']='cost')->Picked_And_Cutted:
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

	return Picked_And_Cutted(ordered_stock, combined_lengths, cutted_stock)


def printcutted(picked_and_cutted:Picked_And_Cutted)->None:
	picked_and_cutted.cutted_stock.sort(key= lambda x: x.original_length)

	print("Order:")
	print(f"\tTotal cost: {picked_and_cutted.order.total_price}")
	for length,count in picked_and_cutted.order.items.items(): print(f"\t{length}: {count:3}×")
	print("Cutted stock:")
	for s in picked_and_cutted.cutted_stock:
		print(f"\t{s.original_length:4} -> ",end='')
		for p in s.pieces:
			print(f"{p}, ",end='')
		print("")
	print("Combined lengths:")
	for l in picked_and_cutted.combined_lengths:
		print(f"\t{l.length:4} <- ",end='')
		for p in l.pieces:
			print(f"{p}, ",end='')
		print("")

