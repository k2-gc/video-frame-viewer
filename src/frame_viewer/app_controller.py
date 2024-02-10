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
    def __init__(self, root, video_path: str):
        self.logger = get_logger()
        self.logger.info("Init Controller class")
        self.model = Model(video_path=video_path)
        image_width, image_height = self.model.get_image_size()
        self.view = View(root, (image_width, image_height))
        self.root = root
        self.next_key = ["d", "Right"]
        self.prev_key = ["a", "Left"]
        self.save_key = ["s", "Down"]
        self.quit_key = ["q"]

        # Bind variables in Model to widgets in View class
        self.view.current_frame.config(textvariable=self.model.currnet_frame_index)
        self.view.skip_frame.config(textvariable=self.model.skip_frame_num)

        # Bind callback function to button in View class
        self.view.next_btn.config(command=lambda: self.update_frame(True))
        self.view.prev_btn.config(command=lambda: self.update_frame(False))
        self.view.save_btn.config(command=self.model.save_frame)

        # Bind callback function to key pressing
        self.root.bind("<KeyPress>", self.key_event)

        # Display first frame
        self._update_image()
    
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
