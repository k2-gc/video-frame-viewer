import os
from pathlib import Path
import shutil
import tkinter as tk

import cv2
from PIL import Image

from .utils import get_logger

class Model:
    """Manage frame position, load and svae a frame.
    Hold opencv VideoCapture object, frame num, current frame index and so on.
    This class corresponds to 'Model' in MVC design.

    Args: 
        video_path (str): video_path to be loaded
    """
    def __init__(self):
        self.logger = get_logger()
        self.logger.info("Init Model class")
        self.cap = None
        self.tmp_video_path = None
        self.val = tk.IntVar(value=0)

        # tkinter variables setting
        self.currnet_frame_index = tk.IntVar(value=0)
        self.skip_frame_num = tk.IntVar(value=1)
    
    def set_video_info(self, video_path):
        self.tmp_video_path = "tmp" + Path(video_path).suffix
        shutil.copyfile(video_path, self.tmp_video_path)
        self._check_video_file_validation(video_path=video_path)

        self.cap = cv2.VideoCapture(self.tmp_video_path)
        self.video_frame_num = self._get_frame_num()
        self.logger.info(f"Checking '{video_path}' ...")
        self.show_info()

        # Prepare output dir
        self.out_dir = Path(Path(video_path).stem)
        self.logger.info(f"Output directory '{self.out_dir}' creating...")
        self.out_dir.mkdir(exist_ok=True, parents=True)
    
    def __del__(self):
        if not self.cap is None:
            del self.cap
        if not self.tmp_video_path is None:
            self.logger.info(f"'{self.tmp_video_path}' deleting...")
            os.remove(self.tmp_video_path)
        self.logger.info("Model object deleting...")
    
    def _check_video_file_validation(self, video_path):
        """Check video file existence.
        If exists, copy video file to 'tmp.mp4'.

        Args:
            video_path (str): Video path to be checked.
        """
        if not Path(video_path).exists():
            self.logger.critical(f"Video path '{video_path}' not found.")
            self.logger.info("App stopped")
            exit()
        self.logger.info(f"'{video_path}' copying to 'tmp.mp4'")
        shutil.copy2(video_path, self.tmp_video_path)
        cap = cv2.VideoCapture(self.tmp_video_path)
        if not cap.isOpened():
            self.logger.critical(f"Video path '{video_path}' load failed.")
            self.logger.info("App stopped")
            exit()
    
    def show_info(self):
        """Show video info.
        Show frame num in video, frame rate of video, width and height of frame.
        """
        self.logger.info("******************")
        self.logger.info(f"Frame num: '{self.video_frame_num}'")
        self.logger.info(f"Frame rate: '{self.cap.get(cv2.CAP_PROP_FPS)}'")
        self.logger.info(f"Image width: '{self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)}'")
        self.logger.info(f"Image height: '{self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}'")
        self.logger.info("******************")

    def _get_frame_num(self):
        """Count the number of frames of video instead of 'cap.get(cv2.CAP_PROP_FRAME_COUNT)'.

        Returns:
            frame_count: Total frame num
        """
        frame_count = 0
        while True:
            ret, _ = self.cap.read()
            if not ret:
                break
            frame_count += 1
        return frame_count

    def show_frame(self):
        """Get current frame.
        Read current frame from cap and return Image object.

        Returns: 
            image: Image object
        """
        current_frame_index = self.currnet_frame_index.get()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_index) 
        ret, image = self.cap.read()
        if not ret:
            self.logger.warning(f"Reading '{current_frame_index}' failed")
            return None
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        self.logger.info(f"Showing! frame index: '{current_frame_index}'")
        return image
        
    
    def update_frame_index(self, is_next: bool = True):
        """Update frame index
        Get int number that is input on app and calculate current frame index.

        Args:
            is_next (bool): If true, add input number to 'self.current_frame_index'.
                            Otherwise, substract.
        """
        try:
            skip_frame_num = self.skip_frame_num.get()
        except:
            self.logger.warning("'Skip num' is not int")
            return

        if skip_frame_num < 0:
            self.logger.warning("'Skip frame' num must be positive")
            return
        if is_next:
            next_frame_index = min(self.currnet_frame_index.get() + skip_frame_num, self.video_frame_num-1)
            self.currnet_frame_index.set(next_frame_index)
        else:
            next_frame_index = max(0, self.currnet_frame_index.get() - skip_frame_num)
            self.currnet_frame_index.set(next_frame_index)
    
    def save_frame(self):
        """Save current frame
        First, save frame named 'tmp.png' and rename it 'frame_FRAME-INDEX.png'.
        """
        current_frame_index = self.currnet_frame_index.get()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_index) 
        ret, image = self.cap.read()
        if not ret:
            self.logger.warning(f"Reading '{current_frame_index}' failed")
            return None
        self.logger.info(f"Saving! frame index: '{current_frame_index}'")
        cv2.imwrite("tmp.png", image)
        out_name = f"frame_{str(current_frame_index).zfill(6)}.png"
        out_path = self.out_dir / out_name
        shutil.move("tmp.png", out_path)
    
    def get_image_size(self):
        """Get frame width and height.
        
        Returns:
            width: Frame width.
            height: Frame height.
        """
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return width, height

