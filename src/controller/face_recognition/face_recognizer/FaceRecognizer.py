from src.controller.face_detector.FaceDetector import FaceDetector
from src.debug.debugutils import DebugUtils
import src.controller.face_recognition.train_test_invoker.train_test_invoker as tti
from src.controller import person_face_records_controller as pfrc
import cv2
import os
import time
from copy import copy
import queue
import threading
import operator

debug = DebugUtils.get_instance()


# This class recognizes and saves the files labeled in the face_files_dir_out
class FaceRecognizer(FaceDetector):

    def __init__(self):
        super().__init__()
        self.train_exec = None
        self.face_files_dir_out
        self.curr_pfr = None
        self.recognizer_method = 'median_sum_accuracy'  # 'count', 'median_sum_accuracy'
        self.max_threads = 1
        self.label_results_accum = {}
        self.label_results_count = {}
        self.threads_recognize = []
        self.threads_recognize_after = []
        self.queue_recog = []
        self.queue_recog_after = []
        self.all_recog = []
        self.current_suspect_name = None
        self.recog_time_last = None
        self.recog_time_sum = None
        self.recog_timestamp_first = None
        self.recog_timestamp_last = None
        self.capture_timestamp_last = None
        self.recog_real_time = False
        self.train_pars = {}

    def initialize(self, train_exec, pfr, video_capture):
        self.train_exec = train_exec
        self.video_capture = video_capture
        self.train_pars = tti.create_test_params(train_exec)
        super().initialize()
        self.curr_pfr = pfr
        self.label_results_accum = {}
        self.label_results_count = {}
        self.all_recog = []
        self.recog_timestamp_first = 0
        self.recog_time_sum = 0
        self.capture_timestamp_last = time.time()
        self.recog_real_time = self.cam.recog_real_time

        self.face_files_dir_out = pfr.suspect_db_dir()
        os.makedirs(self.face_files_dir_out, exist_ok=True)
        self.max_threads = self.cam.recog_threads
        print("MAX THREADS ==================================", self.max_threads)
        self.queue_recog = queue.Queue()
        self.threads_recognize = []
        for i in range(self.max_threads):
            t = threading.Thread(target=self.consume_recog_queue)
            t.start()
            self.threads_recognize.append(t)

        if not self.recog_real_time:
            self.queue_recog_after = queue.Queue()
            self.threads_recognize_after = []
            for i in range(self.max_threads):
                t = threading.Thread(target=self.consume_recog_queue_after)
                # t.start()
                self.threads_recognize_after.append(t)

        # super().capture_loop()

    def recognize(self):

        self.queue_recog.join()
        # stop workers
        for i in range(self.max_threads):
            self.queue_recog.put(None)
        for t in self.threads_recognize:
            t.join()

        if not self.recog_real_time:
            for t in self.threads_recognize_after:
                t.start()
            self.queue_recog_after.join()
            for i in range(self.max_threads):
                self.queue_recog_after.put(None)
            for t in self.threads_recognize_after:
                t.join()
        for t in self.all_recog:
            # if not self.recog_real_time:
            #     t.recognize()
            os.remove(t.totest_filename)
            pfrc.pfr_add_face_record(t.curr_pfr, t.rec_filename, commit=False)
            debug.msg('Creating suspect: {} faces in {}'.format(t.curr_pfr.suspect_name, t.rec_filename))
            file_path = "{}/{}".format(self.face_files_dir_out, t.rec_filename)
            cv2.imwrite(file_path, t.current_face_image)
            for person, result in t.labels_results.items():
                if person in self.label_results_accum.keys():
                    self.label_results_accum[person] = self.label_results_accum[person] + result
                    self.label_results_count[person] += 1
                else:
                    self.label_results_accum[person] = result
                    self.label_results_count[person] = 1
        pfrc.dao.commit()

        pfrc.calculate_median_accuracy(self.recognizer_method, self.label_results_accum, self.curr_pfr)

        recogs_len = len(self.all_recog)
        print('RECOGs # = ', recogs_len)
        if recogs_len > 0:
            recog_total_time = time.time() - self.recog_timestamp_first
            print("RECOGs TIME SUM = ", self.recog_time_sum)
            print("RECOGs TIME TOTAL = ", recog_total_time)
            print("RECOGs PER SECOND = ", recogs_len / self.recog_time_sum)
        return self.curr_pfr

    def consume_recog_queue(self):
        while True:
            item = self.queue_recog.get()
            if item is None:
                # self.queue_recog.task_done()
                break
            now = time.time()
            if self.recog_timestamp_first == 0:
                self.recog_timestamp_first = now
            item.run()
            # TODO configure or not not print name in box
            # self.current_frame = item.current_frame
            self.current_suspect_name = item.person_more_acc
            self.recog_timestamp_last = item.recog_timestamp_last
            if self.recog_real_time:
                self.recog_time_last = item.recog_time_last
                self.recog_time_sum += item.recog_time_last
                print('recog time = ', item.recog_time_last)
            self.queue_recog.task_done()

    def consume_recog_queue_after(self):
        while True:
            item = self.queue_recog_after.get()
            if item is None:
                break
            item.recognize()
            # TODO configure or not not print name in box
            # self.current_frame = item.current_frame
            self.current_suspect_name = item.person_more_acc
            self.recog_time_last = item.recog_time_last
            self.recog_time_sum += item.recog_time_last
            print('recog time = ', item.recog_time_last)
            self.queue_recog_after.task_done()

    def execute_after_detection(self):
        time_now = time.time()
        if (time_now - self.capture_timestamp_last) > self.cam.face_capture_time_interval:
            self.capture_timestamp_last = time_now
            thread = FaceRecognizeThread(
                self.face_files_dir_out, copy(self.current_face_number), self.current_face_image.copy(),
                self.current_frame.copy(), self.train_pars, copy(self.x_ini_face), copy(self.y_ini_face), self.curr_pfr,
                self.video_capture, self.recog_real_time)
            self.queue_recog.put(thread)
            if not self.recog_real_time:
                self.queue_recog_after.put(thread)
            self.all_recog.append(thread)

# class FaceRecognizeThread(Thread):
class FaceRecognizeThread:
    def __init__(self, face_files_dir_out, current_face_number, current_face_image, current_frame, train_pars,
                 x_ini_face, y_ini_face, curr_pfr, video_capture, recog_real_time):
        # Thread.__init__(self)
        # copy of fr instance
        self.face_files_dir_out = face_files_dir_out
        self.current_face_number = current_face_number
        self.current_face_image = current_face_image
        self.current_frame = current_frame
        self.x_ini_face = x_ini_face
        self.y_ini_face = y_ini_face
        self.curr_pfr = curr_pfr
        self.labels_results = {}
        self.rec_filename = None
        self.video_capture = video_capture
        self.person_more_acc = None
        self.totest_filename = None
        self.recog_timestamp_last = None
        # self.capture_timestamp_last = 0
        self.recog_time_last = 0
        self.recog_real_time = recog_real_time
        self.train_pars = train_pars


    def run(self):
        # self.capture_timestamp_last = time.time()
        self.totest_filename = "{}/face_{}.jpg".format(self.face_files_dir_out, self.current_face_number)
        cv2.imwrite(self.totest_filename, self.current_face_image)
        # TODO invoke with memory instead of wrinting file
        # check tensorflow/python/client/session.py line 1361 (where executes openning file)
        if self.recog_real_time:
            self.recognize()
        self.rec_filename = "{}_{}.jpg".format(self.curr_pfr.person.name, self.current_face_number)

    def recognize(self):
        print("=============>>> recognizing ...")
        self.recog_timestamp_last = time.time()
        self.labels_results, time_exec = tti.invoke_test_file(self.train_pars, self.totest_filename)
        if len(self.labels_results.items()) > 0:
            # font_color = (0, 255, 255)
            self.person_more_acc = max(self.labels_results.items(), key=operator.itemgetter(1))[0]
            # TODO configure or not not print name in box
            # cv2.putText(self.current_frame, person_more_acc, (self.x_ini_face, self.y_ini_face - 10),
            #             cv2.FONT_HERSHEY_SIMPLEX,
            #             0.90, font_color, 1)
            # Erro no display cv2 com threads
            # self.display_system.display(self.current_frame)
        else:
            self.person_more_acc = 'not_recognized'
        self.recog_time_last = time.time() - self.recog_timestamp_last

