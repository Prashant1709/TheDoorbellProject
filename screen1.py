THEME_COLOR = "#375362"
BUTTON_COLOR = "#32a891"
from tkinter import *
from PIL import ImageTk, Image
def psuedo():
    print("Unrecognised!")
window = Tk()
window.title("Display")
window.config(padx=20,pady=20,background=THEME_COLOR)
score = Label(text="WELCOME!!",fg="white",bg=THEME_COLOR,width=10,font=("Arial",20,"italic"))
face = ImageTk.PhotoImage(Image.open("./image.jpg"))
score.grid(row=0,column=0,columnspan=2)
canvas = Canvas(height=380,width=380,background="white")
#question = canvas.create_text(150,125,width=280,text="Images",fill=THEME_COLOR,font=("Arial",20,"italic"))
im = canvas.create_image(0,0,image=face,anchor=NW)
canvas.grid(row=1,column=0,columnspan=2,pady=50)
b_1 = Button(text="ADD NEW USER",background=BUTTON_COLOR,highlightthickness=0,command=psuedo,padx=20)
b_2 = Button(text="   REJECT   ",background=BUTTON_COLOR,highlightthickness=0,command=psuedo,padx=40)
b_1.grid(row=2,column=0)
b_2.grid(row=2,column=1)
window.mainloop()
