import tkinter as tk

from .app_controller import Controller
from .utils import get_logger


def run_app(video_path):
    logger = get_logger()
    logger.info("App start!")
    root = tk.Tk()
    app = Controller(root, video_path)
    root.mainloop()
    logger.info("App done!")
