import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import configparser

config = configparser.ConfigParser()
config.read("config.conf")

class ImageCropper:
    def __init__(self, root, file_path, uuid):
        self.root = root
        self.root.title("区域选择")

        self.center_window()

        self.canvas = tk.Canvas(root, width=1024, height=700)
        self.canvas.pack()

        self.crop_rect = None
        self.start_x = None
        self.start_y = None
        self.uuid = uuid

        self.crop_button = tk.Button(root, text="确定", command=self.crop_image)
        self.crop_button.pack()

        self.image = Image.open(file_path)
        self.displayed_image = None
        self.scale_ratio = 1
        self.x_offset = 0
        self.y_offset = 0
        self.display_image()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 1024
        window_height = 768

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    def display_image(self):
        if self.image:
            canvas_width = 1024
            canvas_height = 700

            img_width, img_height = self.image.size
            ratio = min(canvas_width / img_width, canvas_height / img_height)
            self.scale_ratio = ratio
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)

            resized_image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.displayed_image = ImageTk.PhotoImage(resized_image)

            self.x_offset = (canvas_width - new_width) // 2
            self.y_offset = (canvas_height - new_height) // 2

            self.canvas.delete("all")
            self.canvas.create_image(self.x_offset, self.y_offset, image=self.displayed_image, anchor=tk.NW)

    def crop_image(self):
        if self.crop_rect:
            x1, y1, x2, y2 = self.canvas.coords(self.crop_rect)

            x1 -= self.x_offset
            y1 -= self.y_offset
            x2 -= self.x_offset
            y2 -= self.y_offset

            x1, y1 = int(x1 / self.scale_ratio), int(y1 / self.scale_ratio)
            x2, y2 = int(x2 / self.scale_ratio), int(y2 / self.scale_ratio)

            cropped = self.image.crop((x1, y1, x2, y2))
            cropped.save(f"{config['Directory']['crop_dir']}/{self.uuid}.png")
            self.root.destroy()

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        if self.start_x and self.start_y:
            self.canvas.delete(self.crop_rect)
            self.crop_rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="red", width=2)

    def setup_events(self):
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)

def crop_image(file_path, uuid):
    root = tk.Tk()
    cropper = ImageCropper(root, file_path, uuid)
    cropper.setup_events()
    root.mainloop()
    return f"{config['Directory']['crop_dir']}/{uuid}.png"
