from Tkinter import *

root = Tk()

p1 = Button(root, text="Hello", fg="black", bg="red")
p2 = Button(root, text="Hello 2", fg="black", bg="green")
p3 = Button(root, text="Hello 3", fg="white", bg="blue")

p1.grid(column=2)
p2.grid(row=3, column=1)
p3.grid(row=4)

root.mainloop()
