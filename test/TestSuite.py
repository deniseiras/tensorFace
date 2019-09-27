import unittest
from test.controller.experiment_controller.TestExperimentController import TestExperimentController
from test.controller.face_recognition.face_detector.face_recognizer.TestFaceRecognizer import TestFaceRecognizer
from test.controller.face_recognition.face_detector.face_recorder.TestFaceRecorder import TestFaceRecorder
from test.controller.face_recognition.face_tester.TestFaceTester import TestFaceTester
from test.controller.face_recognition.face_trainer.TestFaceTrainer import TestFaceTrainer
from test.controller.TestCameraController import TestCameraController


test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(TestExperimentController))
test_suite.addTest(unittest.makeSuite(TestFaceRecognizer))
test_suite.addTest(unittest.makeSuite(TestFaceRecorder))
test_suite.addTest(unittest.makeSuite(TestFaceTester))
test_suite.addTest(unittest.makeSuite(TestFaceTrainer))
test_suite.addTest(unittest.makeSuite(TestCameraController))


runner=unittest.TextTestRunner()
runner.run(test_suite)

