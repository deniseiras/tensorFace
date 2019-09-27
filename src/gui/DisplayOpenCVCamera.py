import cv2
from src.gui.DisplayCamera import DisplayCamera


class DisplayOpenCVCamera(DisplayCamera):

    def __init__(self):
        self.is_show_video = True

    def display(self, frame):
        cv2.imshow("Security Feed", frame)
