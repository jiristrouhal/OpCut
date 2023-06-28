#   Created by Jiří Strouhal (2023).
#   Written in Python 3.10.10
#   Licensed under the MIT License. See the LICENSE in the project root folder. 
#   Public repository: https://github.com/jiristrouhal/opcut.
#   Use MznStrouhal@gmail.com to contact the author.


import tkinter as tk
from typing import Optional


class ToolTip(object):
    #https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python

    def __init__(self, widget:tk.Widget):
        self._widget = widget
        self._tipwindow:Optional[tk.Toplevel] = None
        self.id = None
        self.x = self.y = 0
   
    def showtip(self, text):
        """Display text in tooltip window"""
        self.text = text
        if self._tipwindow or not self.text: return
        coords = self._widget.bbox()
        if coords is not None:
            x, y, cx, cy = coords
            x = x + cx  + self._widget.winfo_rootx() + 25
            y = y + cy + self._widget.winfo_rooty() + 25
            self._tipwindow = tw = tk.Toplevel(self._widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry("+%d+%d" % (x, y))
            label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0",relief=tk.SOLID, borderwidth=1,
                      font=("Arial", "9", "normal"))
            label.pack(ipadx=1)

    def hidetip(self):
        tw = self._tipwindow
        self._tipwindow = None
        if tw: tw.destroy()

def createToolTip(widget:tk.Widget, text:str):
    toolTip = ToolTip(widget)
    def enter(event:tk.Event):
        toolTip.showtip(text)
    def leave(event:tk.Event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
