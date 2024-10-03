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
        self.create_window(image_width, image_height)
    
    def create_window(self, image_width, image_height):
        self.logger.info("Creating window...")
        self.image_width, self.imaeg_height = self.resize_window_size(image_width, image_height)

        # Create tkinter widgets
        self.tool_bar = tk.Frame(self.parent, width=self.image_width)
        self.command_bar = tk.Frame(self.parent, width=self.image_width)
        self.tool_bar.grid(column=0, row=0, sticky="NEWS")
        self.command_bar.grid(column=0, row=2, sticky="NEWS")
        self.canvas = tk.Canvas(self.parent, bg="white", height=self.imaeg_height, width=self.image_width-4)
        self.file_dialog = tk.Button(self.tool_bar, text="File", width=10, height=1, bg="white")
        for i in range(7):
            self.command_bar.grid_columnconfigure(i, weight=1)

        self.frame_label = tk.Label(self.command_bar, text="Frame:")
        self.current_frame = tk.Label(self.command_bar)
        self.skip_label = tk.Label(self.command_bar, text="Skip num:")
        self.skip_frame = tk.Entry(self.command_bar, width=3)
        self.prev_btn = tk.Button(self.command_bar, text="Prev")
        self.next_btn = tk.Button(self.command_bar, text="Next")
        self.save_btn = tk.Button(self.command_bar, text="Save")

        self.canvas.grid(column=0, row=1)
        command_button = [
            self.prev_btn,
            self.save_btn,
            self.frame_label,
            self.current_frame,
            self.skip_label,
            self.skip_frame,
            self.next_btn,
        ]
        for i, command in enumerate(command_button):
            command.grid(column=i, row=0)
            command.grid_columnconfigure(i, weight=1)
        self.file_dialog.grid(column=0, row=0, padx=0, pady=2, sticky=tk.W)

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
        If frame width>4000, resize each of width and height to a quarter.
        If frame width>1500, resize each of width and height to half.
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

