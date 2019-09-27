import cv2
from src.controller.video_capture.VideoCapture import VideoCapture
from src.debug.debugutils import DebugUtils

debug = DebugUtils.get_instance()

# TODO get_event


class VideoCaptureOpenCV(VideoCapture):

    def __init__(self, camera):
        super().__init__(camera)
        # rtsp://USUARIO:SENHA@IP:PORTA/cam/realmonitor?channel=1&subtype=0
        if camera.camera_string == '0':
            camera.camera_string = 0
        self.video_capturer = cv2.VideoCapture(camera.camera_string)

    def initialize(self):
        # self.videoCap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'));
        if not self.video_capturer.isOpened():
            debug.msg("Cannot open the video cam")
            return False
        # TODO nao funciona
        # self.video_capturer.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera.y_res)
        # self.video_capturer.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera.x_res)
        return True

    def rewind(self):
        self.video_capturer.set(cv2.CAP_PROP_POS_FRAMES, 1)

    def capture(self):
        ret, image = self.video_capturer.read()
        return image

    def destroy(self):
        self.video_capturer.release()
        cv2.destroyAllWindows()

    @staticmethod
    def get_event():
        k=cv2.waitKey(30) & 0xff
        if k == 27 or k == 46:
            return VideoCapture.CAM_EVENT_QUIT
        elif k == 45:
            return VideoCapture.CAM_EVENT_STOP
        elif k == 43:
            return VideoCapture.CAM_EVENT_START


