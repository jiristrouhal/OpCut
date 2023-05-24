import pickstock,sortall,cut
from typing import List, Dict
import dataclasses


@dataclasses.dataclass
class Stock:
	length:int
	price:int


def pickandcut(lengths:List[int],stock:List[Stock]):
	prepared_stock = [pickstock.Stock(s.length,s.price) for s in stock]
	picked_stock = pickstock.ecopick(lengths, prepared_stock)
	sorted_lengths, sorted_stock = sortall.mincutsort(lengths,picked_stock.items,)
	prepared_sorted_lengths = [cut.Length(l.length,l.id) for l in sorted_lengths]
	cutted_lengths, cutted_stock = cut.cut(prepared_sorted_lengths,sorted_stock)
	cutted_lengths.sort(key = lambda x: x.original.id)

	assert(sum([sum(l.pieces) for l in cutted_lengths])<=sum([sum(s.pieces) for s in cutted_stock]))

	return picked_stock, cutted_lengths, cutted_stock


def printcutted(cost:int, order:Dict[int,int],lengths:List[cut.Cutted_Length],stock:List[cut.Cutted_Stock]):
	stock.sort(key= lambda x: x.original)

	print("Order:")
	print(f"\tTotal cost: {cost}")
	for length,count in order.items(): print(f"\t{length}: {count:3}×")
	print("Cutted stock:")
	for s in stock:
		print(f"\t{s.original:4} -> ",end='')
		for p in s.pieces:
			print(f"{p}, ",end='')
		print("")
	print("Combined lengths:")
	for l in lengths:
		print(f"\t{l.original.length:4} <- ",end='')
		for p in l.pieces:
			print(f"{p}, ",end='')
		print("")


L = [100, 200, 150, 230, 95, 45, 255, 100, 100, 100, 250, 120, 45, 78, 80, 120, 140, 450]
S = [Stock(100,1000), Stock(200,2000), Stock(150,1500), Stock(250,2500)]
order,l,s = pickandcut(L,S)
printcutted(order.cost, order.items, l,s)
