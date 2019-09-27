import os
from src.controller.face_detector.FaceDetector import FaceDetector
from src.controller import person_face_records_controller as pfrc
from src.debug.debugutils import DebugUtils
import cv2
import shutil
import time
import datetime

debug = DebugUtils.get_instance()


# TODO - check if needs to speed up process by creating FaceRecord at the end of process
class FaceRecorder(FaceDetector):

    def __init__(self, add_or_ovewrite_faces):
        super().__init__()
        self.add_or_ovewrite_faces = add_or_ovewrite_faces
        self.person = None
        self.last_rec_time = time.time()
        self.to_record_files = []

    def initialize(self, person, video_capture):
        self.video_capture = video_capture
        self.person = person
        debug.msg('Recording faces of {} from {} into {}'.format(self.person.name, self.video_capture.camera.camera_string, self.person.person_db_dir()))

        if not os.path.isdir(self.person.person_db_dir()):
            os.makedirs(self.person.person_db_dir())
            debug.msg('>>> Person {} dir created on {}'.format(self.person.name, self.person.person_db_dir()))
        else:
            if not self.add_or_ovewrite_faces:
                debug.msg('>>> Person {} dir already exists on {} . Exiting ...'.format(self.person.name, self.person.person_db_dir()))
                exit(-1)
        self.face_files_dir_out = self.person.person_db_dir()
        super().initialize()

    def record_faces(self):
        for rec in self.to_record_files:
            cv2.imwrite('{}/{}'.format(self.face_files_dir_out, rec[0]), rec[1])
            pfrc.person_add_face_record(self.person, rec[0], commit=False)
        pfrc.dao.update_object(self.person, commit=True)

    def execute_after_detection(self):
        time_now = time.time()
        if (time_now - self.last_rec_time) > self.cam.face_capture_time_interval:
            nfilename = "face_{}.jpg".format(self.current_face_number)
            self.to_record_files.append([nfilename, self.current_face_image])
            self.last_rec_time = time_now

    def create_face_dir_out(self):
        if os.path.isdir(self.face_files_dir_out):
            shutil.rmtree(self.face_files_dir_out)
        os.makedirs(self.face_files_dir_out)