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
	sorted_lengths, sorted_stock = sortall.mincutsort(lengths,picked_stock.items)
	prepared_sorted_lengths = [cut.Length(l.length,l.id) for l in sorted_lengths]
	cutted_lengths, cutted_stock = cut.cut(prepared_sorted_lengths,sorted_stock)
	cutted_lengths.sort(key = lambda x: x.original.id)

	return cutted_lengths, cutted_stock

L = [100, 200, 150]
S = [Stock(100,1000), Stock(150,1500)]

l,s = pickandcut(L,S)
print(l)
print(s)