import tkinter as tk
import pick_and_cut as pc
from typing import List
import cz


window = tk.Tk()
window.geometry("800x600")
window.title("BestCut")


input_frame = tk.Frame(window)
input_frame.pack(side=tk.TOP,expand=1)
controls_frame = tk.Frame(window)
controls_frame.pack(side=tk.TOP)
output_frame = tk.Frame(window)
output_frame.pack(side=tk.BOTTOM,expand=2)


from typing import List
import re
ITEM_DELIM = ";"
def is_int_list(src:str)->bool:
	is_valid = True
	if src.strip()=="": return is_valid
	if src[0]==ITEM_DELIM: src=src[1:]
	if src[-1]==ITEM_DELIM: src=src[:-1]
	for item in src.split(ITEM_DELIM):
		if not (re.fullmatch(r"\d+",item.strip()) or item==' '):
			is_valid = False
			break
	return is_valid


def auto_add_space_before_number(event:tk.Event)->None:
	src = lengths_input.get()
	for digit in range(10): src=src.replace(f"{ITEM_DELIM}{digit}",f"{ITEM_DELIM} {digit}")
	lengths_input.delete(0,tk.END)
	lengths_input.insert(0,src)
	return


vcmd = (window.register(is_int_list))
lengths_input = tk.Entry(input_frame,width=100,validate="key",validatecommand=(vcmd,'%P'))
lengths_input.bind("<KeyRelease>",auto_add_space_before_number)
lengths_input.pack()
stock_input = tk.Entry(input_frame,width=100)
stock_input.pack()


order_output = tk.Text(output_frame,width=30)
order_output.pack(side=tk.LEFT,expand=1)
combined_lengths_output = tk.Text(output_frame,width=30)
combined_lengths_output.pack(side=tk.RIGHT,expand=1)
cutted_stock_output = tk.Text(output_frame,width=30)
cutted_stock_output.pack(side=tk.RIGHT,expand=1)


def __underline(text:str)->str:
	text += "\n"+"–"*len(text)
	return text


def __read_lengths_input()->List[int]:
	lengths_str:List[str] = lengths_input.get().split(ITEM_DELIM)
	lengths:List[int] = list()
	for li in lengths_str: 
		li = li.strip()
		if li=='': continue
		lengths.append(int(li))
	return lengths


def __read_stock_input()->List[pc.Stock]:
	stock_str:List[str] = stock_input.get().split(ITEM_DELIM)
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
	order_str = __underline(cz.ORDER)+"\n"
	order_str += cz.TOTAL_COST+":"+f" {order.total_price}\n\n" + cz.ITEMS+":\n"
	for length,count in order.items.items():
		order_str += f"\t{length:5} ...\t{count:3} {cz.PIECES}\n"
	order_output.delete("1.0",tk.END)
	order_output.insert(tk.END,order_str)


def __redraw_cutted_stock(stock:List[pc.Cutted_Stock])->None:
	stock_str = __underline(cz.HOW_TO_CUT_STOCK)+"\n"
	for s in stock:
		stock_str += f"{s.original_length:4} → "
		for piece in s.pieces[:-1]:
			stock_str += f"{piece}, "
		stock_str += f"{s.pieces[-1]}\n"

	cutted_stock_output.delete("1.0",tk.END)
	cutted_stock_output.insert(tk.END,stock_str)


def __redraw_combined_lengths(lengths:List[pc.Combined_Length])->None:
	lengths_str = __underline(cz.HOW_TO_COMBINE_LENGTHS)+"\n"
	print(lengths)
	for l in lengths:
		lengths_str += f"{l.length:4} ← "
		for piece in l.pieces[:-1]:
			lengths_str += f"{piece}, "
		if len(l.pieces)>0:
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