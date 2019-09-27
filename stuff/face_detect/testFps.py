import datetime
import sys
import pygame.camera
import time
import cv2
import numpy

#parameters
millisResetTimeInitFrame = 10000
xRes = 640 / 2
yRes = 480 / 2
#parameters


pygame.init()
pygame.camera.init()
screen = pygame.display.set_mode((xRes, yRes))
cam = pygame.camera.Camera("/dev/video0", (xRes, yRes))
cam.start()


fps = 0
millisTotFPS = 0
millisTotInitialFrame = 0
imgNum = 0

while 1:
    millisInit = int(round(time.time() * 1000))
    imageSurface = cam.get_image()
    screen.blit(imageSurface, (0,0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # save as video output
            sys.exit()

    millisThis = int(round(time.time() * 1000)) - millisInit
    if millisTotInitialFrame > millisResetTimeInitFrame:
        fps = fps * 1000 / millisTotInitialFrame
        print 'FPS: ', fps
        print 'Reset Initial frame '
        millisTotInitialFrame = 0
        millisTotFPS = 0
        fps = 0
    else:
        millisTotInitialFrame += millisThis
        millisTotFPS += millisThis
        fps += 1

# cleanup the camera and close any open windows
cv2.destroyAllWindows()


