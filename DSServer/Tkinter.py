from time import sleep
from tkinter import *
root = Tk()
root.iconbitmap(default='app.ico')
def btn_click():
	TOKENI = loginInput.get()
	IDI = ID.get()
	
	Token = open('token.txt', 'w', encoding='utf-8')
	Token.write(TOKENI)
	Token.close()

	IF = open('information.txt', 'w', encoding='utf-8')
	IF.write("ID: " + IDI + "\n" + "Token: " + TOKENI)
	Token.close()
	title['text'] = "Connected!"
	id['text'] = "Connected!"
	btn['text'] = "Connected!"
	import os

	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Tkinter.py')
	os.remove(path)

root['bg'] = '#fafafa'
root.title('DSServer!')
root.wm_attributes('-alpha', 0.7)
root.geometry('300x250')

root.resizable(width=False, height=False)

canvas = Canvas(root, height=250, width=250)
canvas.pack()

frame = Frame(root, bg='red')
frame.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.6)

title = Label(frame, text='Enter bot token!', bg='gray', font=40)
title.pack()


loginInput = Entry(frame, bg='white')
loginInput.pack()

'''passField = Entry(frame, bg='white')
passField.pack()'''

id = Label(frame, text='Enter bot id!', bg='gray', font=40)
id.pack()

ID = Entry(frame, bg='white')
ID.pack()

btn = Button(frame, text='Connect!', bg='yellow', command=btn_click)
btn.pack()

root.mainloop()