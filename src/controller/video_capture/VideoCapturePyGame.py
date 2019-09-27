import numpy
import pygame.camera
from src.controller.face_detector import VideoCapture


class VideoCapturePyGame(VideoCapture):

    def __init__(self, camera):
        pygame.init()
        pygame.camera.init()
        self.screen = pygame.display.set_mode((camera.x_res, camera.y_res))
        self.camera_pg = pygame.camera.Camera(camera.camera_string, (camera.x_res, camera.y_res))
        self.camera_pg.start()
        self.image_surface = None

    def capture(self):
        self.image_surface = self.camera_pg.get_image()
        image_array = pygame.surfarray.array3d(self.image_surface)
        image = numpy.array(image_array).copy()
        return image

    def correct_image_shape(self, image):
        image = numpy.rot90(image, -1)
        image = numpy.fliplr(image)
        return image

    def correct_image_color(self, image):
        image = image[..., ::-1]
        return image

    def prepare_save(self, saved_image):
        saved_image = self.correct_image_shape(saved_image)
        saved_image = self.correct_image_color(saved_image)
        return saved_image

    def display(self, frame, showCam=False):
        pygame.surfarray.blit_array(self.image_surface, frame)
        self.screen.blit(self.image_surface, (0, 0))
        if showCam:
            pygame.display.update()
        else:
            pygame.display.iconify()

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return VideoCapturePyGame.CAM_EVENT_QUIT
        key = pygame.key.get_pressed()
        if key[pygame.K_KP_MINUS]:
            return VideoCapturePyGame.CAM_EVENT_STOP
        elif key[pygame.K_KP_PLUS]:
            return VideoCapturePyGame.CAM_EVENT_START
        elif key[pygame.K_KP_PERIOD]:
            return VideoCapturePyGame.CAM_EVENT_QUIT

    def destroy(self):
        self.camera_pg.stop()
        pygame.camera.quit()
        pygame.quit()


