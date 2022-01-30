# A GUI app to watermark an image

from tkinter import Tk, Button, filedialog, Label
from PIL import ImageTk, Image

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
panel = None
WATERMARK = None


def open_image():
    global panel
    # Check for existing image in window and remove
    if panel != None:
        panel.destroy()
    # Get filename and open image
    filename = openfilename()
    img = Image.open(filename)
    img_width, img_height = img.size  # Find size of image for scaling
    img_scale = (WINDOW_WIDTH - 50) / img_width  # Scale image to fit width
    # Check height of image vs window height and reset scale if needed
    if img_height * img_scale > WINDOW_HEIGHT - 30:
        img_scale = (WINDOW_HEIGHT - 30) / img_height
    preview_img = img.resize((int(img_width*img_scale),
                              int(img_height*img_scale)),
                             Image.ANTIALIAS)
    preview_img = ImageTk.PhotoImage(preview_img)
    panel = Label(image=preview_img)
    panel.image = preview_img
    panel.place(relwidth=1.0)


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
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    # window.resizable(width=True, height=True)
    open_button = Button(text="Open Image", command=open_image)
    # Place button at bottom
    open_button.place(width=100, relx=0.5, x=-50, rely=1, y=-25)
    window.mainloop()  # Keep the window open


if __name__ == '__main__':
    main()
