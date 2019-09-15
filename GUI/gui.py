import tkinter as tk
from tkinter import * 
import platform

window = Tk()  #constructor blank window 
window.title("MID AIR")

#background 
background_image=tk.PhotoImage(file="GUI/guibkg.png")
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

#startstop
startStopButton = Button(window, text = "Start/Stop", font =("Arial Bold", 50), activebackground = "DeepSkyBlue2", activeforeground = "DeepSkyBlue2", bg = "seagreen1", state = ACTIVE, justify = CENTER, highlightcolor = "DeepSkyBlue2", highlightbackground="white", fg="Black", highlightthickness=6)
startStopButton.grid(column = 0, row = 0)

showTextLbl = Label(window, text = "Get text from LEAP", font =("Arial Bold", 50))
showTextLbl.grid(column=1, row=1)

showPicLbl = Label(window, text="and pic will be here", font =("Arial Bold", 50))
showPicLbl.grid(column=0, row=2)

window.geometry("2000x900")
window.mainloop()
