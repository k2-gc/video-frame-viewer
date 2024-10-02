import tkinter as tk

from PIL import ImageTk

from .utils import get_logger

class View(tk.Frame):
    """Manage app screen.

    Args:
        parent (tkinter.Tk): tkinter.Tk object
        image_size (tuple): (width, height)
    """
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
    
    def __del__(self):
        self.logger.info("View object deleting...")
    
    def update_image(self, image):
        """Update displayed frame on app screen.
        """
        del self.image_obj
        image = image.resize((self.image_width, self.imaeg_height))
        image = ImageTk.PhotoImage(image)
        self.image_obj = image
        self.canvas.create_image(0, 0, image=image, anchor=tk.NW)
    
    def resize_window_size(self, image_width, image_height):
        """Resize app screen size if need.
        If frame width>1500, resize to half.
        If frame width<650, resize to 650 and keep aspect ratio.

        Args:
            image_width (int | float): Frame width.
            image_height (int | float): Frame height.
        
        Returns:
            image_width: Frame width.
            image_width: Frame height.
        """
        if image_width > 4000:
            image_width = image_width / 4
            image_height = image_height / 4
        elif image_width > 1500:
            image_width = image_width / 2
            image_height = image_height / 2
        elif image_width < 650:
            r = 650 / image_width
            image_width = image_width*r
            image_height = image_height*r
        return int(image_width), int(image_height)

