##import tkinter as tk
from tkinter import * 
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        menu = Menu(self.master)
        master.config(menu=menu)

        bmp_menu = Menu(menu)
        bmp_menu.add_command(label="Encrypt bmp file (ECB)", command=self.EncryptBMP_ECB)
        bmp_menu.add_command(label="Decrypt bmp file (ECB)", command=self.DecryptBMP_ECB)
        bmp_menu.add_command(label="Encrypt bmp file (CBC)", command=self.EncryptBMP_CBC)
        bmp_menu.add_command(label="Decrypt bmp file (CBC)", command=self.DecryptBMP_CBC)
        bmp_menu.add_command(label="Exit", command=self.quit)
        menu.add_cascade(label="bmp file", menu=bmp_menu)

        text_menu = Menu(menu)
        text_menu.add_command(label="Encrypt txt file (ECB)", command=self.EncryptText_ECB)
        text_menu.add_command(label="Decrypt txt file (ECB)", command=self.EncryptText_CBC)
        text_menu.add_command(label="Encrypt txt file (CBC)", command=self.DecryptText_ECB)
        text_menu.add_command(label="Decrypt txt file (CBC)", command=self.DecryptText_CBC)
        menu.add_cascade(label="text file", menu=text_menu)

        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=True)
        self.image = None # none yet

    #Function for open bmp file
    def openFileBMP(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select BMP File", filetypes=[("BMP Files","*.bmp")])
        if not filename:
            return # user cancelled; stop this method

        self.canvas.delete('all')
        self.load = Image.open(filename)
        w, h = self.load.size
        self.render = ImageTk.PhotoImage(self.load) #must keep a reference to this

        if self.load is not None: # if an image was already loaded
            self.canvas.delete(self.load) # remove the previous image
        
        label = Label(root, text="Original", image=self.render, compound='top')
        self.canvas.create_window(300, 300, window=label)
        root.geometry("%dx%d" % (w, h))

    #Function for open bmp file
    def openFileText(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select text File", filetypes=[("text Files","*.txt")])
        if not filename:
            return # user cancelled; stop this method

        self.canvas.delete('all')
        #Read file
        with open(filename) as f:
            contents = f.read()
            #print(contents)

            # Create text widget and specify size.
            T = Text(root, height = 5, width = 52)
            label = Label(root, text="Original", compound='top')
            self.canvas.create_window(250, 30, window=label)
            self.canvas.create_window(250, 100, window=T)
            # Insert The Fact.
            T.insert(END, contents)

    #Function for encrypt bmp file use ECB mode
    def EncryptBMP_ECB(self):
        self.openFileBMP()
    
    #Function for encrypt bmp file use ECB mode
    def EncryptBMP_CBC(self):
        self.openFileBMP()
    
    #Function for encrypt bmp file use ECB mode
    def DecryptBMP_ECB(self):
        self.openFileBMP()
    
    #Function for encrypt bmp file use ECB mode
    def DecryptBMP_CBC(self):
        self.openFileBMP()

    #Function for encrypt Text file use ECB mode
    def EncryptText_ECB(self):
        self.openFileText()
    
    #Function for encrypt Text file use ECB mode
    def EncryptText_CBC(self):
        self.openFileText()
    
    #Function for encrypt Text file use ECB mode
    def DecryptText_ECB(self):
        self.openFileText()
    
    #Function for encrypt Text file use ECB mode
    def DecryptText_CBC(self):
        self.openFileText()

root = Tk()
root.geometry("%dx%d" % (300, 300))
root.title("Symmetryc Encryption GUI")
app = Window(root)
app.pack(fill=BOTH, expand=1)
root.mainloop()