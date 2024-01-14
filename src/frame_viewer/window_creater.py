import tkinter as tk

from PIL import ImageTk

from .utils import get_logger

class View(tk.Frame):
    def __init__(self, parent, image_size):
        super().__init__(parent)
        self.parent = parent
        self.logger = get_logger()
        self.logger.info("Init View class")
        image_width, image_height = image_size
        self.image_width, self.imaeg_height = self.resize_window_size(image_width, image_height)

        # Create tkinter widgets
        self.canvas = tk.Canvas(self, bg="white", height=self.imaeg_height, width=self.image_width)
        self.frame_label = tk.Label(self, width=1, text="Frame:")
        self.current_frame = tk.Label(self, width=1)
        self.skip_label = tk.Label(self, width=1, text="Skip num:")
        self.skip_frame = tk.Entry(self, width=1)
        self.prev_btn = tk.Button(self, text="Prev")
        self.next_btn = tk.Button(self, text="Next")
        self.save_btn = tk.Button(self, text="Save")

        # Locate tkinter widgets
        self.canvas.grid(column=0, columnspan=7, row=0)
        self.grid_columnconfigure(index=(0, 1, 6), weight=3)
        self.grid_columnconfigure(index=(3, 4), weight=2)
        self.grid_columnconfigure(index=(2, 5), weight=1)
        self.prev_btn.grid(column=0, row=1, sticky="news")
        self.save_btn.grid(column=1, row=1, sticky="news")
        self.frame_label.grid(column=2, row=1, sticky="news")
        self.current_frame.grid(column=3, row=1, sticky="news")
        self.skip_label.grid(column=4, row=1, sticky="news")
        self.skip_frame.grid(column=5, row=1, sticky="news")
        self.next_btn.grid(column=6, row=1, sticky="news")
        self.pack()

        # For display image
        self.image_obj = None
    
    def update_image(self, image):
        del self.image_obj
        image = image.resize((self.image_width, self.imaeg_height))
        image = ImageTk.PhotoImage(image)
        self.image_obj = image
        self.canvas.create_image(0, 0, image=image, anchor=tk.NW)
    
    def resize_window_size(self, image_width, image_height):
        if image_width < 650:
            r = 650 / image_width
            image_width = image_width*r
            image_height = image_height*r
        return int(image_width), int(image_height)

