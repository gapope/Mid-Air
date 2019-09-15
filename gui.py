from Tkinter import *
import platform

from util import *

#App class
class Application(Frame):
    
    def __init__(self, window):
        window.title("Mid Air")
        window.geometry("2000x900")
        
        Frame.__init__(self, window)

        self.pack(expand=1, fill='both')

        self.initBackground()
        self.initObjects()

    #Build background
    def initBackground(self):
        self.background_image = PhotoImage(file="images/guibkg.png")
        self.background_label = Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    #Build objects
    def initObjects(self):
        #startstop
        self.startBtnImage = PhotoImage(file="images/button_start.png")
        self.startButton = Button(self, image = self.startBtnImage, command=self.startClicked, activebackground="DeepSkyBlue2", activeforeground="DeepSkyBlue2", bg = "seagreen1", state = ACTIVE, justify = CENTER, highlightcolor = "DeepSkyBlue2", highlightbackground="white", fg="Black", highlightthickness=6)
        self.startButton.grid(column = 0, row = 0, padx=5, pady=5, sticky=E)

        self.stopBtnImage = PhotoImage(file="images/button_stop.png")
        self.stopButton = Button(self, image = self.stopBtnImage, command=self.stopClicked, activebackground="DeepSkyBlue2", activeforeground="DeepSkyBlue2", bg = "seagreen1", state = DISABLED, justify = CENTER, highlightcolor = "DeepSkyBlue2", highlightbackground="white", fg="Black", highlightthickness=6)
        self.stopButton.grid(column = 1, row = 0, padx=5, pady=5, sticky=W)

        #Message label
        self.mesgLbl = Label(self, text = "Press start to begin", font=("Arial Bold", 50))
        self.mesgLbl.grid(column=1, row=1, padx=5, pady=5)

        #Image label
        self.defaultImage = PhotoImage(file='images/default.png')
        self.imgLbl = Label(self, image=self.defaultImage)
        self.imgLbl.grid(column=0, row=1, padx=5, pady=5)

        #Text input
        self.txtInput = Text(self, height=10, width=50)
        self.txtInput.grid(column=0, row=2, padx=5, pady=5)

    #Start Leap Motion data recording and switch to stop mode
    def startClicked(self):
        try:
            assert startLeapMotion(self), "Listener attach failure"

            #Swap mode
            self.stopButton.configure(state=ACTIVE)
            self.startButton.configure(state=DISABLED)
        except Exception as e:
            output(self, "Unable to start LeapMotion motion: " +str(e))

    #Stop Leap Motion data recording, trigger data anylsis ad switch to start mode
    def stopClicked(self):
        try:
            stopLeapMotion(self)

            #Swap mode
            self.startButton.configure(state=ACTIVE)
            self.stopButton.configure(state=DISABLED)
        except Exception as e:
            output(self, "Error with halting LeapMotion motion and/or processing data: " +str(e))

    #Set a string in the 'Message' label
    def setMessageLabel(self, mesg):
        self.mesgLbl.configure(text=mesg)

    #Set an image in the 'Image' label
    def setImageLabel(self, imageFile):
        self.image = PhotoImage(file=imageFile)

        self.imgLbl.configure(image=self.image)


#Run the app
def main():
    window = Tk()
    app = Application(window)

    app.mainloop()


if __name__ == '__main__':
    main()