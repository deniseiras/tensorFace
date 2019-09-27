

class VideoCapture:

    CAM_EVENT_START = 1
    CAM_EVENT_STOP = 2
    CAM_EVENT_QUIT = 3

    def __init__(self, camera=None):
        self.camera = camera
        self.video_capturer = None
        pass

    def capture(self):
        pass

    def rewind(self):
        pass

    def correct_image_shape(self, image):
        # print("Generic cam correct_image_shape() ...")
        return image

    def correct_image_color(self, image):
        # print("Generic cam correct_image_color() ...")
        return image

    def prepare_save(self, saved_image):
        # print("Generic cam prepare_save() ...")
        return saved_image

    def destroy(self):
        pass

    @staticmethod
    def get_event():
        pass
