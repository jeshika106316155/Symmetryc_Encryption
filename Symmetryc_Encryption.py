from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from SelfAES import *
import os
import base64


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
        text_menu.add_command(label="Decrypt txt file (ECB)", command=self.DecryptText_ECB)
        text_menu.add_command(label="Encrypt txt file (CBC)", command=self.EncryptText_CBC)
        text_menu.add_command(label="Decrypt txt file (CBC)", command=self.DecryptText_CBC)
        menu.add_cascade(label="text file", menu=text_menu)

        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=True)
        self.image = None  # none yet

    # Function for open bmp file
    def openFileBMP(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select BMP File",
                                              filetypes=[("BMP Files", "*.bmp")])
        if not filename:
            return  # user cancelled; stop this method
        contents = 0
        self.canvas.delete('all')
        with open(filename, "rb") as f:
            contents = f.read()
            self.load = Image.open(filename)
            w, h = self.load.size
            self.render = ImageTk.PhotoImage(self.load)  # must keep a reference to this

            if self.load is not None:  # if an image was already loaded
                self.canvas.delete(self.load)  # remove the previous image

            label = Label(root, text="Original", image=self.render, compound='top')
            self.canvas.create_window(300, 300, window=label)
            root.geometry("%dx%d" % (w, h))

        return contents

    # Function for open bmp file
    def openFileText(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select text File",
                                              filetypes=[("text Files", "*.txt")])
        if not filename:
            return  # user cancelled; stop this method
        contents = ""
        self.canvas.delete('all')
        # Read file
        with open(filename) as f:
            contents = f.read()
            # print(contents)

            # Create text widget and specify size.
            T = Text(root, height=5, width=52)
            label = Label(root, text="Original", compound='top')
            self.canvas.create_window(250, 30, window=label)
            self.canvas.create_window(250, 100, window=T)
            # Insert The Fact.
            T.insert(END, contents)
        return contents

    # Function for encrypt bmp file use ECB mode
    def EncryptBMP_ECB(self):
        plain_data = self.openFileBMP()
        self_aes = SelfAES()
        need_trim = len(plain_data) % 16  # 截斷
        clear_trimmed = plain_data[64:-need_trim]  # 截斷 16 倍數
        cipher_data = self_aes.ecb_encrypt(clear_trimmed)
        cipher_data = plain_data[0:64] + cipher_data + plain_data[-need_trim:]
        with open("tux_ecb.bmp", "wb") as f:
            f.write(cipher_data)

    # Function for encrypt bmp file use ECB mode
    def EncryptBMP_CBC(self):
        plain_data = self.openFileBMP()
        self_aes = SelfAES()
        need_trim = len(plain_data) % 16  # 截斷
        clear_trimmed = plain_data[64:-need_trim]  # 截斷 16 倍數
        cipher_data = self_aes.cbc_encrypt(clear_trimmed)
        cipher_data = plain_data[0:64] + cipher_data + plain_data[-need_trim:]
        with open("tux_cbc.bmp", "wb") as f:
            f.write(cipher_data)

    # Function for encrypt bmp file use ECB mode
    def DecryptBMP_ECB(self):
        cipher_data = self.openFileBMP()
        self_aes = SelfAES()
        need_trim = len(cipher_data) % 16  # 截斷
        clear_trimmed = cipher_data[64:-need_trim]  # 截斷 16 倍數
        plain_data = self_aes.ecb_decrypt(clear_trimmed)
        plain_data = cipher_data[0:64] + plain_data + cipher_data[-need_trim:]
        with open("tux_ecb_return.bmp", "wb") as f:
            f.write(plain_data)

    # Function for encrypt bmp file use ECB mode
    def DecryptBMP_CBC(self):
        cipher_data = self.openFileBMP()
        self_aes = SelfAES()
        need_trim = len(cipher_data) % 16  # 截斷
        clear_trimmed = cipher_data[64:-need_trim]  # 截斷 16 倍數
        plain_data = self_aes.cbc_decrypt(clear_trimmed)
        plain_data = cipher_data[0:64] + plain_data + cipher_data[-need_trim:]
        with open("tux_cbc_return.bmp", "wb") as f:
            f.write(plain_data)

    # Function for encrypt Text file use ECB mode
    def EncryptText_ECB(self):
        plain_text = self.openFileText()
        plain_text = plain_text.encode(encoding="utf-8")
        self_aes = SelfAES()
        pad_plain_text = self_aes.pad(plain_text)
        cipher_text = self_aes.ecb_encrypt(pad_plain_text)
        cipher_text_b64 = base64.b64encode(cipher_text)
        with open("test_1_ecb.txt", "w") as f:
            f.write(cipher_text_b64.decode('ascii'))

    # Function for encrypt Text file use ECB mode
    def EncryptText_CBC(self):
        plain_text = self.openFileText()
        plain_text = plain_text.encode(encoding="utf-8")
        self_aes = SelfAES()
        pad_plain_text = self_aes.pad(plain_text)
        cipher_text = self_aes.cbc_encrypt(pad_plain_text)
        cipher_text_b64 = base64.b64encode(cipher_text)
        with open("test_1_cbc.txt", "w") as f:
            f.write(cipher_text_b64.decode('ascii'))

    # Function for encrypt Text file use ECB mode
    def DecryptText_ECB(self):
        cipher_text_b64 = self.openFileText()
        cipher_text = base64.b64decode(cipher_text_b64)
        self_aes = SelfAES()
        pad_plain_text = self_aes.ecb_decrypt(cipher_text)
        plain_text = self_aes.unpad(pad_plain_text)
        plain_text = plain_text.decode("utf-8")
        with open("test_1_ecb_return.txt", "w") as f:
            f.write(plain_text)


    # Function for encrypt Text file use ECB mode
    def DecryptText_CBC(self):
        cipher_text_b64 = self.openFileText()
        cipher_text = base64.b64decode(cipher_text_b64)
        self_aes = SelfAES()
        pad_plain_text = self_aes.cbc_decrypt(cipher_text)
        plain_text = self_aes.unpad(pad_plain_text)
        plain_text = plain_text.decode("utf-8")
        with open("test_1_cbc_return.txt", "w") as f:
            f.write(plain_text)


root = Tk()
root.geometry("%dx%d" % (300, 300))
root.title("Symmetryc Encryption GUI")
app = Window(root)
app.pack(fill=BOTH, expand=1)
root.mainloop()
