"""
R-Type Project
CS332L, Spring 2016

Rick Miyamoto
"""
from tkinter import *
import math


win = Frame()
win.grid_propagate(0)
win.config(bg='black', height=50, width=50)
win.pack()

cc_prompt = Label(win, text='R-Type')
cc_prompt.config(font=('arial', 20, 'bold'))
cc_prompt.pack()


b1 = Button(win, text='Start', command=sys.exit)
b2 = Button(win, text='Exit', command=sys.exit)

b2.pack(side=RIGHT)
b1.pack(side=RIGHT)



win.mainloop()