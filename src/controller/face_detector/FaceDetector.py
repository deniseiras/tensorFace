import copy
import time

import cv2
import numpy as np

from src.debug.debugutils import DebugUtils

# from threading import Thread

debug = DebugUtils.get_instance()


class FaceDetector:

    def __init__(self):
        # parameters ##################
        # self.min_area = 1000
        self.face_files_dir_out = None
        # TODO nao detectou nada - reset
        self.start_after_secs = 0
        self.show_FPS_millis = 1000
        self.haarcascade_xml = '/dados/dev/tensorface-venv/lib/python3.5/site-packages/cv2/data/haarcascade_frontalface_alt.xml'
        self.face_cascade = cv2.CascadeClassifier(self.haarcascade_xml)
        self.video_capture = None
        self.cam = None
        self.is_show_roi_rect = True
        self.is_show_face_rect = True
        self.current_face_image = None
        self.current_frame = None
        self.current_face_number = 0
        self.y_ini_face = 0
        self.y_end_face = 0
        self.x_ini_face = 0
        self.x_end_face = 0
        self.y_res_cam = 0
        self.x_res_cam = 0
        self.xmin = 0
        self.ymin = 0
        self.xmax = 0
        self.ymax = 0
        self.roi_back_gray_top = None
        self.roi_back_color_top = None
        self.firstFrame = None
        self.millis_tot_initial_frame = 0
        self.millis_tot_capture = 0

    def initialize(self):
        debug.msg("Initializing capture")
        time.sleep(self.start_after_secs)
        self.create_face_dir_out()
        self.firstFrame = None
        self.millis_tot_capture = 0
        self.millis_this_capture = 0
        self.current_frame = self.video_capture.capture()
        self.y_res_cam = self.current_frame.shape[0]
        self.x_res_cam = self.current_frame.shape[1]
        # TODO just for video file
        self.video_capture.rewind()
        self.xmin = 0
        self.ymin = 0
        # TODO update camera
        self.xmax = self.x_res_cam
        self.ymax = self.y_res_cam
        self.current_face_number = 0
        self.cam = self.video_capture.camera
        self.millis_tot_initial_frame = self.cam.reset_time_init_frame_millis

    def capture_loop(self):
        while self.current_frame is not None:
            self.capture()

    def capture(self):

        if self.cam.back_sub_do:
            millis_init = time.time()
        millis_init_capture = time.time()
        # debug.initFPS()
        self.current_frame = self.video_capture.capture()
        if self.current_frame is None:
            print("n0en3")
            return None, None
        # TODO check resize to save faces
        # resize the frame, convert it to grayscale, and blur it
        # self.current_frame = imutils.resize(self.current_frame, width=500)
        # self.current_frame = cv2.resize(capturedImg, (min_area * 3, min_area * 4), interpolation=cv2.INTER_CUBIC)
        if self.cam.back_sub_do or self.cam.face_detection_do:
            try:
                gray = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2GRAY)
            except:
                return None, None

        if self.cam.back_sub_do:
            gray_blur = cv2.GaussianBlur(gray, (21, 21), 0)
            # if the first frame is None, initialize it
            if self.firstFrame is None:
                self.firstFrame = gray_blur
                return self.current_frame, 0
            # compute the absolute difference between the current frame and
            # first frame
            frame_delta = cv2.absdiff(self.firstFrame, gray_blur)
            thresh = cv2.threshold(frame_delta, self.cam.back_sub_thresh_num, 255, cv2.THRESH_BINARY)[1]
            # dilate the thresholded image to fill in holes ...
            thresh = cv2.dilate(thresh, None, iterations=2)
            (imgCnts, cnts, hierarchy) = cv2.findContours(copy.copy(thresh), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # print "contornos: ", len(cnts)
            # loop over the contours
            self.xmin = self.x_res_cam - self.cam.back_sub_roi_x_res_reduction
            self.ymin = self.y_res_cam
            self.xmax = self.cam.back_sub_roi_x_start
            self.ymax = 0

            if len(cnts) > 0:
                for c in cnts:
                    (xb, yb, wb, hb) = cv2.boundingRect(c)
                    if self.cam.back_sub_roi_x_start < xb < self.xmin:
                        self.xmin = xb
                    if yb < self.ymin:
                        self.ymin = yb
                    if self.xmax < xb + wb < self.x_res_cam - self.cam.back_sub_roi_x_res_reduction:
                        self.xmax = xb + wb
                    if yb + hb > self.ymax:
                        self.ymax = yb + hb
                # if changed self.xmin and self.xmax
                if self.xmin < self.xmax:
                    self.xmin = max(self.xmin - self.cam.back_sub_roi_top_border, 0)
                    self.ymin = max(self.ymin - self.cam.back_sub_roi_top_border, 0)
                    self.xmax = min(self.xmax + self.cam.back_sub_roi_top_border, self.x_res_cam)
                    # self.ymax = min(self.ymax, self.y_res_cam) # dont need to increase bottom
                    # TODO implement configuratiopn for the upper region - only the upper region have faces
                    # ymax_top = self.ymin + int((self.ymax - self.ymin) / 1.5)
                    ymax_top = self.ymax
                    self.roi_back_gray_top = copy.copy(gray[self.ymin:ymax_top, self.xmin:self.xmax])
                    self.roi_back_color_top = copy.copy(self.current_frame[self.ymin:ymax_top, self.xmin:self.xmax])
                    if self.is_show_roi_rect:
                        # TODO implement configuratiopn for the upper region - only the upper region have faces
                        # cv2.rectangle(self.current_frame, (self.xmin, self.ymin), (self.xmax, self.ymax),
                        #               (0, 255, 0), 2)
                        cv2.rectangle(self.current_frame, (self.xmin, self.ymin), (self.xmax, ymax_top),
                                      (0, 0, 255), 2)
        else:
            if self.cam.face_detection_do:
                self.roi_back_gray_top = copy.copy(gray)
                self.roi_back_color_top = copy.copy(self.current_frame)
        # print("x,y = ({},{}) ({},{})".format(self.xmin,self.ymin,self.xmax,self.ymax))
        # TODO calcular tamanho ideal para roi_back_gray (tamanho minimo da cabeca)
        if self.cam.face_detection_do and self.xmin < self.xmax and self.roi_back_gray_top.shape[
            1] > self.cam.face_capture_min_width_fixed:
            self.detect_face()
        self.millis_this_capture = time.time() - millis_init_capture
        self.millis_tot_capture += self.millis_this_capture
        if self.cam.back_sub_do:
            millis_this = time.time() - millis_init
            if self.millis_tot_initial_frame >= self.cam.reset_time_init_frame_millis:
                debug.msg('Reset Initial frame ')
                self.firstFrame = None
                self.millis_tot_initial_frame = 0
            else:
                self.millis_tot_initial_frame += millis_this
        return self.current_frame, self.millis_this_capture

    def detect_face(self):
        # roi_back_gray = self.video_capture.correct_image_shape(roi_back_gray)
        millis_point = time.time()
        minNeig = self.cam.face_capture_min_neighbors if self.cam.face_capture_min_neighbors > 0 else None
        # default : scaleFactor=1.1, minNeighors=3
        faces = self.face_cascade.detectMultiScale(self.roi_back_gray_top, minSize=(
            int(self.cam.face_capture_min_width_fixed), int(self.cam.face_capture_min_width_fixed)),
                                                   minNeighbors=minNeig, scaleFactor=self.cam.face_capture_scale_factor)
        # debug.msg("detecttime = {} milllis".format(int(round(time.time() * 1000)) - millis_point))
        for (x, y, w, h) in faces:
            # if isinstance(self.cam, CameraPyGamePsEye):
            # inverted x, y + position of roi
            # cv2.rectangle(self.current_frame, (self.ymin+y, self.xmin+x), (self.ymin+y+h, self.xmin+x+w), (255, 0, 0), 2)
            # else:
            # print("face x,y = ({},{}) ({},{})".format(x, y, x+w, y+w))
            # cv2.rectangle(self.current_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face_y_border = h * self.cam.face_border_increase_pct
            face_x_border = w * self.cam.face_border_increase_pct
            y_ini_face_roi = max(int(y - face_y_border), 0)
            y_end_face_roi = min(int(y + h + face_y_border), self.roi_back_gray_top.shape[0])
            x_ini_face_roi = max(int(x - face_x_border), 0)
            x_end_face_roi = min(int(x + w + face_x_border), self.roi_back_gray_top.shape[1])
            self.current_face_image = self.roi_back_color_top[y_ini_face_roi:y_end_face_roi,
                                      x_ini_face_roi:x_end_face_roi]

            # TESTS ILUMINANCE ================================
            # ===================================================
            blue = self.current_face_image[:, :, 0]
            green = self.current_face_image[:, :, 1]
            red = self.current_face_image[:, :, 2]
            k = 1
            # self.relative_iluminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
            # self.relative_iluminance = self.matrix_sample(self.relative_iluminance, k)
            self.relative_iluminance = self.current_face_image
            self.relative_iluminance = cv2.GaussianBlur(self.relative_iluminance, (21, 21), 0)
            n, m, dumb = self.relative_iluminance.shape

            self.y_ini_face = y_ini_face_roi + self.ymin
            self.y_end_face = y_end_face_roi + self.ymin
            self.x_ini_face = x_ini_face_roi + self.xmin
            self.x_end_face = x_end_face_roi + self.xmin

            if self.is_show_face_rect:
                self.current_frame[0:n, 0:m, :] = self.relative_iluminance
                # self.current_frame[0:n, 0:m, 0] = self.relative_iluminance
                # self.current_frame[0:n, 0:m, 1] = self.relative_iluminance
                # self.current_frame[0:n, 0:m, 2] = self.relative_iluminance
                cv2.rectangle(self.current_frame, (self.x_ini_face, self.y_ini_face),
                              (self.x_end_face, self.y_end_face), (255, 0, 0), 2)
            self.current_face_number += 1
            self.execute_after_detection()

    def matrix_mean(self, A, k):
        N, M = A.shape
        A1 = np.empty((N // k, M // k))
        for i in range(N // k):
            for j in range(M // k):
                A1[i, j] = A[k * i:k * i + k, k * j:k * j + k].mean()
        return A1

    def matrix_max(self, A, k):
        N, M = A.shape
        A1 = np.empty((N // k, M // k))
        for i in range(N // k):
            for j in range(M // k):
                A1[i, j] = A[k * i:k * i + k, k * j:k * j + k].max()
        return A1

    def matrix_sample(self, A, k):
        N, M = A.shape
        A1 = np.empty((N // k, M // k))
        for i in range(N // k):
            for j in range(M // k):
                A1[i, j] = A[k * i, k * j]
        return A1

    def stop(self):
        debug.msg("Capture stopped")
        self.video_capture.destroy()

    def execute_after_detection(self):
        pass

    def create_face_dir_out(self):
        pass
