import tkinter as tk
import pick_and_cut as pc
from typing import List
import cz


window = tk.Tk()
window.geometry("800x600")


input_frame = tk.Frame(window)
input_frame.pack(side=tk.TOP,expand=1)
controls_frame = tk.Frame(window)
controls_frame.pack(side=tk.TOP)
output_frame = tk.Frame(window)
output_frame.pack(side=tk.BOTTOM,expand=2)


lengths_input = tk.Entry(input_frame,width=100)
lengths_input.pack()
stock_input = tk.Entry(input_frame,width=100)
stock_input.pack()


order_output = tk.Text(output_frame,width=30)
order_output.pack(side=tk.LEFT,expand=1)
combined_lengths_output = tk.Text(output_frame,width=30)
combined_lengths_output.pack(side=tk.RIGHT,expand=1)
cutted_stock_output = tk.Text(output_frame,width=30)
cutted_stock_output.pack(side=tk.RIGHT,expand=1)


def __read_lengths_input()->List[int]:
	lengths_str:List[str] = lengths_input.get().split(";")
	lengths:List[int] = list()
	for li in lengths_str: 
		li = li.strip()
		if li=='': continue
		lengths.append(int(li))
	return lengths


def __read_stock_input()->List[pc.Stock]:
	stock_str:List[str] = stock_input.get().split(";")
	if len(stock_str)==0: return []
	stock:List[pc.Stock] = list()
	for s in stock_str:
		if s.strip()=='': continue
		s=s.replace("(","").replace(")","").strip()
		if s.count(",") != 1: return []
		length, price = tuple(s.split(","))
		stock.append(pc.Stock(int(length),int(price)))
	return stock


def __redraw_order(order:pc.Ordered_Stock)->None:
	order_str = cz.TOTAL_COST+f": {order.total_price}\n\n" + cz.ITEMS+":\n"
	for length,count in order.items.items():
		order_str += f"\t{length:5} ...\t{count:3} {cz.PIECES}\n"
	order_output.delete("1.0",tk.END)
	order_output.insert(tk.END,order_str)


def __redraw_cutted_stock(stock:List[pc.Cutted_Stock])->None:
	stock_str = ""
	for s in stock:
		stock_str += f"{s.original_length:4} -> "
		for piece in s.pieces[:-1]:
			stock_str += f"{piece}, "
		stock_str += f"{s.pieces[-1]}\n"
	cutted_stock_output.delete("1.0",tk.END)
	cutted_stock_output.insert(tk.END,stock_str)


def __redraw_combined_lengths(lengths:List[pc.Combined_Length])->None:
	lengths_str = ""
	for l in lengths:
		lengths_str += f"{l.length:4} <- "
		for piece in l.pieces[:-1]:
			lengths_str += f"{piece}, "
		lengths_str += f"{l.pieces[-1]}\n"
	combined_lengths_output.delete("1.0",tk.END)
	combined_lengths_output.insert(tk.END,lengths_str)


def calculate()->None:
	lengths = __read_lengths_input()
	stock = __read_stock_input()
	if not (lengths and stock): return
	result = pc.pickandcut(lengths,stock)
	__redraw_order(result.order)
	__redraw_cutted_stock(result.cutted_stock)
	__redraw_combined_lengths(result.combined_lengths)


calculate_button = tk.Button(controls_frame,text=cz.CALCULATE,command=calculate).pack()


window.mainloop()