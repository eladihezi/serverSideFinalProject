#gui import
from tkinter import * 
from tkinter import simpledialog
import tkinter.messagebox as box 


top = Tk()
Tk().withdraw()

def integerbox(title='Title', prompt='Prompt text:'):
    '''Creates a simple integer input box with Ok/Cancel buttons. Ok returns
    the integer entered. Cancel returns "cancel".'''
    Tk().withdraw()
    enteredInteger = simpledialog.askinteger(title, prompt)
    if enteredInteger is None:
        return 'cancel'
    else:
        return enteredInteger

def inputbox(title='Title', prompt='Prompt text:'):
    '''Creates a simple string input box with Ok/Cancel buttons. Ok returns
    the string entered unless the string is empty then "empty" is returned.
    Cancel returns "cancel".'''
    Tk().withdraw()
    enteredString = simpledialog.askstring(title, prompt)
    if enteredString is None:
        return 'cancel'
    elif enteredString == '':
        return 'empty'
    else:
        return enteredString

num1 = integerbox("input1","enter number between 1 - 100")
str1 = inputbox("input2","enter string:")
print (num1)
print (str1)




def helloCallBack():
    exit()
def quit():
    top.destroy()

B1 = tkinter.Button(top, text ="Exit", command =  helloCallBack )

B1.pack()
B2 = tkinter.Button(top, text ="OK", command =  quit )
B2.pack()

top.mainloop()