import tkinter as tk

from .app_controller import Controller
from .utils import get_logger


def run_app(video_path):
    """Run app.

    Args:
        video_path (str): Video_path to be loaded.
    """
    logger = get_logger()
    logger.info("App start!")
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()
    logger.info("App stopped!")
