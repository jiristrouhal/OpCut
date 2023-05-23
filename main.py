import pickstock,sortall,cut
from typing import List, Dict
import dataclasses


@dataclasses.dataclass
class Stock:
	length:int
	price:int


def pickandcut(lengths:List[int],stock:List[Stock],minimum:int=0):
	prepared_stock = [pickstock.Stock(s.length,s.price) for s in stock]
	picked_stock = pickstock.ecopick(lengths, prepared_stock)
	sorted_lengths, sorted_stock = sortall.mincutsort(lengths,picked_stock.items,)
	prepared_sorted_lengths = [cut.Length(l.length,l.id) for l in sorted_lengths]
	cutted_lengths, cutted_stock = cut.cut(prepared_sorted_lengths,sorted_stock)
	cutted_lengths.sort(key = lambda x: x.original.id)

	return cutted_lengths, cutted_stock


def printcutted(lengths:List[cut.Cutted_Length],stock:List[cut.Cutted_Stock]):
	print("Stock:")
	for s in stock:
		print(f"\t{s.original:4} -> ",end='')
		for p in s.pieces:
			print(f"{p}, ",end='')
		print("")
	print("Lengths:")
	for l in lengths:
		print(f"\t{l.original.length:4} <- ",end='')
		for p in l.pieces:
			print(f"{p}, ",end='')
		print("")


L = [100, 200, 150, 230, 95, 45, 255, 100, 158, 100, 250]
S = [Stock(100,1000), Stock(250,1500)]

l,s = pickandcut(L,S)
printcutted(l,s)
