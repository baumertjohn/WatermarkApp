# A watermarking GUI app utilizing classes

from tkinter import Entry, Tk, Button, filedialog, Label, StringVar, messagebox
from PIL import ImageTk, Image, ImageDraw, ImageFont
import copy

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
WM_FONT_SIZE = 30


class Watermarker(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.watermark = StringVar()
        self.title('Simple Watermarking App')
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        # Open Image
        open_button = Button(text="Open Image", command=self.open_image)
        open_button.place(width=120, relx=0.5, x=-260, rely=1, y=-25)
        # Watermark entry
        wm_entry = Entry(0, textvariable=self.watermark)
        wm_entry.insert(0, 'Watermark Text')
        wm_entry.place(width=120, relx=0.5, x=-125, rely=1, y=-22)
        # Preview button
        preview_button = Button(text='Preview Watermark',
                                command=self.make_watermark)
        preview_button.place(width=120, relx=0.5, x=5, rely=1, y=-25)
        # Save button
        save_button = Button(text='Save Image', command=self.save_image)
        save_button.place(width=120, relx=0.5, x=140, rely=1, y=-25)

    def open_image(self):
        try:
            self.img_panel.destroy()
        except AttributeError:
            pass
        self.filename = self.openfilename()
        self.photo = Photo(Image.open(self.filename))
        preview_image = ImageTk.PhotoImage(self.photo.img_small)
        self.img_panel = Label(image=preview_image)
        self.img_panel.image = preview_image
        self.img_panel.place(relwidth=1.0)

    def openfilename(self):
        # Open file dialog box to select image
        filename = filedialog.askopenfilename(initialdir='%USERPROFILE%',
                                              title='Select an Image.',
                                              filetypes=[('Image files',
                                                          '*.jpg *.jpeg *.png'),
                                                         ('All files', '*.*')])
        return filename

    def make_watermark(self):
        self.img_panel.destroy()
        watermark = self.watermark.get()
        # Create working copy of image for preview
        preview_wm_img = copy.copy(self.photo.img_small).convert('RGBA')
        txt = Image.new('RGBA', preview_wm_img.size, (255, 255, 255, 0))
        wm_font = ImageFont.truetype('./open-sans.extrabold.ttf', WM_FONT_SIZE)
        d = ImageDraw.Draw(txt)
        # Find preview image center for text
        img_width, img_height = preview_wm_img.size
        d.text((img_width-10, img_height-10), watermark,
               font=wm_font, anchor='rs', fill=(0, 0, 0, 50))
        combined_img = Image.alpha_composite(preview_wm_img, txt)
        preview_image = ImageTk.PhotoImage(combined_img)
        self.img_panel = Label(image=preview_image)
        self.img_panel.image = preview_image
        self.img_panel.place(relwidth=1.0)
        self.watermark1 = watermark

    def save_image(self):
        final_img = self.photo.img.convert('RGBA')
        txt = Image.new('RGBA', final_img.size, (255, 255, 255, 0))
        wm_font = ImageFont.truetype('./open-sans.extrabold.ttf',
                                     int(WM_FONT_SIZE/self.photo.img_scale))
        d = ImageDraw.Draw(txt)
        img_width, img_height = self.photo.img.size
        d.text((img_width-int(10/self.photo.img_scale),
                img_height-int(10/self.photo.img_scale)), self.watermark1,
               font=wm_font, anchor='rs', fill=(0, 0, 0, 50))
        combined_img = Image.alpha_composite(final_img, txt)
        # combined_img.show()
        # Find the file extension to separate and add "_watermark" to name
        end_count = 1
        for char in reversed(self.filename):
            if char == '.':
                break
            end_count += 1
        filename = self.filename[:-end_count]
        extension = self.filename[-end_count:]
        new_filename = f"{filename}_watermark{extension}"
        # Save file after converting back to RGB (needed for jpeg files)
        combined_img.convert('RGB').save(new_filename)
        # Find first '/' to show user new filename in pop window.
        end_count = 0
        for char in reversed(new_filename):
            if char == '/':
                break
            end_count += 1
        messagebox.showinfo("Watermark App",
                            f"Image saved as\n{new_filename[-end_count:]}")


class Photo:
    def __init__(self, img):
        self.img = img
        self.width, self.height = img.size
        self.img_small = self.resize()

    def resize(self):
        img_scale = self.find_scale()
        new_width = self.width * img_scale
        new_height = self.height * img_scale
        return self.img.resize((int(new_width), int(new_height)),
                               Image.ANTIALIAS)

    def find_scale(self):
        self.img_scale = (WINDOW_WIDTH - 50) / self.width
        if self.img_scale * self.height > WINDOW_HEIGHT - 30:
            self.img_scale = (WINDOW_HEIGHT - 30) / self.height
        return self.img_scale


app = Watermarker()
app.mainloop()
