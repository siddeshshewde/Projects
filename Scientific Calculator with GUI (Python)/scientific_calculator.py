# Importing libraries
from tkinter import*
import math
import parser
import tkinter.messagebox

### Functions ###

# Exit Function
def exit():
    exit = tkinter.messagebox.askyesno("Scientific Calculator", "Confirm if you want to exit")
    if exit > 0:
        root.destroy()
        return 

# Standard Calculator Function
def standard():
    root.resizable(width = False, height = False)
    root.geometry("450x300+0+0")

# Scientific Calculator Function
def scientific():
    root.resizable(width = False, height = False)
    root.geometry("694x568+0+0")



### Outer Frame ###

root = Tk()
root.title("Scientific Calculator")
root.configure(background="powder blue")
root.resizable(width = True, height = True)
root.geometry("600x568+0+0")

calc = Frame(root)
calc.grid(ipadx=100, ipady=100)

### Outer Frame ###


### Inner Grid ###

text_display = Entry(calc, font=('arial', 20, 'bold'), bg = "powder blue", bd = 30, width = 28, justify = RIGHT)
text_display.grid(row = 0, column = 0, columnspan = 4, pady = 0)
text_display.insert(0, "0")

# Standard Calculator
number_pad = "1234567890"
i = 0
button = []

for j in range (2, 5):
    for k in range (3):
        button.append(Button(calc, width=6, height=2, font=('arial', 20, 'bold'), text = number_pad[i]))
        button[i].grid(row = j, column = k)

        i += 1

clear_button = Button(calc, text = "C", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 1, column = 1)
clearAll_button = Button(calc, text = "CE", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 1, column = 0)
back_button = Button(calc, text = "Back", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 1, column = 2)

dot_button = Button(calc, text = ".", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 5, column = 0)
zero_button = Button(calc, text = "0", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 5, column = 1)
equal_button = Button(calc, text = "=", width = 13, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 5, column = 2, columnspan = 2)

add_button = Button(calc, text = "+", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 1, column = 3)
subtract_button = Button(calc, text = "-", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 2, column = 3)
multiply_button = Button(calc, text = "*", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 3, column = 3)
divide_button = Button(calc, text = "/", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 4, column = 3)

# Scientific Calculator
sin_button = Button(calc, text = "sin", width = 6, height = 2, font=('arial', 20, 'bold'), bg = "powder blue").grid(row = 1, column = 5)
cos_button = Button(calc, text = "cos", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 1, column = 6)
tan_button = Button(calc, text = "tan", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 1, column = 7)

log_button = Button(calc, text = "log", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 2, column = 5)
exponent_button = Button(calc, text = "e", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 2, column = 6)
pi_button = Button(calc, text = "π", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 2, column = 7)



percent_button = Button(calc, text = "%", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 3, column = 5)
power_button = Button(calc, text = "^", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 3, column = 6)
factorial_button = Button(calc, text = "!", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 3, column = 7)

sqrt_button = Button(calc, text = "√", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 4, column = 5)
ln_button = Button(calc, text = "ln", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 4, column = 6)
inverse_button = Button(calc, text = "+/-", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 4, column = 7)

openbracket_button = Button(calc, text = "(", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 5, column = 5)
closebracket_button = Button(calc, text = ")", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 5, column = 6)
closebracket_button = Button(calc, text = ")", width = 6, height = 2, font=('arial', 20, 'bold'),  bg = "powder blue").grid(row = 5, column = 6)

### Inner Grid ###




### Menu Bar ###

menubar = Menu(calc)

# File Menu
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label = "File", menu = filemenu)
filemenu.add_command(label = "Standard", command = standard)
filemenu.add_command(label = "Scientific", command = scientific)
filemenu.add_command(label = "Send Feedback")
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = exit)

# Edit Menu
editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Edit", menu = editmenu)
editmenu.add_command(label = "Cut")
editmenu.add_command(label = "Copy")
editmenu.add_command(label = "Paste")

# Help Menu
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Help", menu = helpmenu)
helpmenu.add_command(label = "View Help")

### Menu Bar ###


root.config(menu = menubar)
root.mainloop()
