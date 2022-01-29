# A GUI app to watermark an image

from tkinter import Tk, Button, filedialog, Label, N
from PIL import ImageTk, Image


def open_image():
    filename = openfilename()
    img = Image.open(filename)
    img = img.resize((500, 500), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(image=img)
    panel.image = img
    panel.place(y=25, relwidth=1.0)


def openfilename():
    # Open file dialog box to select image
    filename = filedialog.askopenfilename(initialdir='%USERPROFILE%',
                                          title='Select an Image.',
                                          filetypes=[('Image files',
                                                      '*.jpg *.jpeg *.png'),
                                                     ('All files', '*.*')])
    return filename


def main():
    window = Tk()
    window.title("Simple Watermarking App")
    window.geometry("500x500")
    window.resizable(width=True, height=True)
    open_button = Button(text="Open Image", command=open_image)
    open_button.place(width=100, relx=0.5, x=-50)
    window.mainloop()  # Keep the window open


if __name__ == '__main__':
    main()
