from test.controller.TestCaseWithDatabase import TestCaseWithDatabase
from src.controller.face_recognition.face_recognizer.FaceRecognizer import FaceRecognizer
from src.controller import person_face_records_controller as pfrc
import src.controller.face_recognition.train_test_invoker.train_test_invoker as tti
from src.controller import train_configuration_controller as tcc
from src.controller import camera_controller
from src.gui.DisplayOpenCVCamera import DisplayOpenCVCamera
from test.controller.face_recognition.face_detector.face_recorder import TestFaceRecorder
from src.debug.debugutils import DebugUtils
import unittest
import time

debug = DebugUtils.get_instance()


class TestFaceRecognizer(TestCaseWithDatabase):

    # 1) Records Faces ideitifying every person
    # 2) Trains the system with the faces
    # 3) Try to recognize faces with FaceRecognizer, recording them in the the Suspect Entity, and the files at the
    #    suspect_dir

    def assert_person(self, train_exec, exp, fr, camera, source, should):
        seconnds_init = int(round(time.time()))
        pfrc.recognize_suspect_faces(train_exec, exp, fr, camera, source)
        fr.capture_loop()
        pfr = fr.recognize()
        seconds_tot = int(round(time.time())) - seconnds_init
        debug.msg('Suspect {} recognized with {}% of confidence in {} seconds'.format(pfr.suspect_name, pfr.suspect_confidence * 100, seconds_tot))
        self.assertEqual(should, pfr.suspect_name, 'Should be {} but was {}'.format(should, pfr.suspect_name))

    def assert_not_person(self, train_exec, exp, fr, camera, source, should):
        pfrc.recognize_suspect_faces(train_exec, exp, fr, camera, source)
        # fr.stop()
        pfr = fr.recognize()
        debug.msg('Suspect {} recognized with {}% of confidence '.format(pfr.suspect_name, pfr.suspect_confidence * 100))
        self.assertNotEqual(pfr.suspect_name, should, 'Should not be {}'.format(should))

    def test_recognize_faces(self):

        exp = TestFaceRecorder.create_exp_face_records()
        train = tcc.create_train_configuration(100, 192) # TODO put 400 steps
        camera = camera_controller.get_object_by_id(1)
        train_exec = tti.invoke_trainer(exp, train)

        fr = FaceRecognizer()
        fr.is_show_roi_rect = True
        fr.display_system = DisplayOpenCVCamera()
        fr.capture_delay_secs = 0

        self.assert_person(train_exec, exp, fr, camera, '/dados/face_bds/sessaocachu/avi/de_2.avi', 'denis')
        self.assert_person(train_exec, exp, fr, camera, '/dados/face_bds/sessaocachu/avi/bruna_2.avi', 'bruna')
        self.assert_person(train_exec, exp, fr, camera, '/dados/face_bds/sessaocachu/avi/carol_2.avi', 'carol')
        self.assert_person(train_exec, exp, fr, camera, '/dados/face_bds/sessaocachu/avi/mae_2.avi', 'lia')
        self.assert_person(train_exec, exp, fr, camera, '/dados/face_bds/sessaocachu/avi/nana_2.avi', 'nana')
        self.assert_person(train_exec, exp, fr, camera, '/dados/face_bds/sessaocachu/avi/nina_2.avi', 'nina')
        self.assert_not_person(train_exec, exp, fr, camera, '/dados/face_bds/sessaocachu/avi/dan_2.avi', 'daniel_non_ecxiste')


if __name__ == '__main__':
    unittest.main()
