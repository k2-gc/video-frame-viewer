from .utils import get_logger
from .frame_position_manager import Model
from .window_creater import View


class Controller:
    def __init__(self, root, video_path: str):
        self.logger = get_logger()
        self.logger.info("Init Controller class")
        self.model = Model(video_path=video_path)
        image_width, image_height = self.model.get_image_size()
        self.view = View(root, (image_width, image_height))

        # Bind variables in Model to widgets in View class
        self.view.current_frame.config(textvariable=self.model.currnet_frame_index)
        self.view.skip_frame.config(textvariable=self.model.skip_frame_num)

        # Bind callback function to button in View class
        self.view.next_btn.config(command=lambda: self.update_frame(True))
        self.view.prev_btn.config(command=lambda: self.update_frame(False))
        self.view.save_btn.config(command=self.model.save_frame)

        # Display first frame
        self._update_image()

    def update_frame(self, is_next=True):
        self.model.update_frame_index(is_next=is_next)
        self._update_image()

    def _update_image(self):
        image = self.model.show_frame()
        self.view.update_image(image)
