import os
import tkinter as tk
import tkinter.filedialog

from .utils import get_logger
from .frame_position_manager import Model
from .window_creater import View


class Controller:
    """App controller
    This class corresponds to 'Controller' in MVC design.

    Args:
        root (tkinter.Tk): tkinter.Tk object.
        video_path (str): Video_path to be loaded.
    """
    def __init__(self, root):
        self.logger = get_logger()
        self.logger.info("Init Controller class")
        self.model = Model()
        self.view = View(root, (640, 480))

        self.root = root
        self.next_key = ["d", "Right"]
        self.prev_key = ["a", "Left"]
        self.save_key = ["s", "Down"]
        self.quit_key = ["q"]
        self._bind_func()

    def _bind_func(self):
        # Bind variables in Model to widgets in View class
        self.view.current_frame.config(textvariable=self.model.currnet_frame_index)
        self.view.skip_frame.config(textvariable=self.model.skip_frame_num)

        # Bind callback function to button in View class
        self.view.next_btn.config(command=lambda: self.update_frame(True))
        self.view.prev_btn.config(command=lambda: self.update_frame(False))
        self.view.save_btn.config(command=self.model.save_frame)
        self.view.file_dialog.config(command=self.open_video)

        # Bind callback function to key pressing
        self.root.bind("<KeyPress>", self.key_event)
    
    def __del__(self):
        self.logger.info("Controller object deleting...")

    def update_frame(self, is_next=True):
        """Calculated how many frames to skip and update displayed frame on app.
        Calculated how many frames to skip and update.
        This function is called when 'next button', 'prev button' or some keys on keyboard.

        Args:
            is_next (bool): Whether next frame or previous frame.
        """
        self.model.update_frame_index(is_next=is_next)
        self._update_image()

    def _update_image(self):
        """Load frame image to be shown and update displayed frame on app.

        """
        image = self.model.show_frame()
        self.view.update_image(image)
    
    def open_video(self):
        """Using filedialog, open mp4 video file
        
        """
        fTyp = [("", "*mp4")]
        iDir = os.path.abspath(os.getcwd())
        file_path = tk.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        if file_path == "":
            return
        self.logger.info(f"Video path: {file_path}")
        if os.path.exists(file_path):
            self.model.set_video_info(file_path)
            width, height = self.model.get_image_size()
            self.view.create_window(image_width=width, image_height=height)
            self._bind_func()
            self.update_frame()
            self.logger.info(f"Loaded: {file_path}")
            self.video_name = os.path.basename(file_path)
        else:
            self.logger.warning(f"Video not found: {file_path}")

    def key_event(self, event):
        """Key pressing operation.
        Called this function and run a function corresponding to key When pressing a key.

        Args:
            event (tkinter.Event): tkinter.Event object.
        """
        if event.keysym in self.next_key:
            self.update_frame(is_next=True)
            return
        elif event.keysym in self.prev_key:
            self.update_frame(is_next=False)
            return
        elif event.keysym in self.save_key:
            self.model.save_frame()
            return
        elif event.keysym in self.quit_key:
            self.root.destroy()
            self.root.quit()
        else:
            self.logger.info(f"No functions is assigned to key '{event.keysym}'")
