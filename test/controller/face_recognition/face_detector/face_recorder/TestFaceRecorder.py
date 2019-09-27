from src.controller.face_recorder.FaceRecorder import FaceRecorder
from src.controller import camera_controller, experiment_controller as em
from src.controller import person_face_records_controller as pfrc
from test.controller.experiment_controller import TestExperimentController
from test.controller.TestCaseWithDatabase import TestCaseWithDatabase
from src.business.Experiment import Experiment

import unittest


# intelbras
# rtsp://admin:camera123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0
# unitoptek
# rtsp://192.168.1.10:554/user=admin&password=&channel=1&stream=0.sdp
# rtsp://192.168.1.11:554/user=admin&password=&channel=1&stream=0.sdp
# rtsp://192.168.1.10:554/user=admin&password=&channel=1&stream=0.sdp?real_streal - diz q melhora velocidade
# preta - está com o ip fixo - ver a arquivo cameras.txt
# rtsp://192.168.1.12/user=admin&password=&channel=1&stream=0.sdp
# rtsp://192.168.1.13/user=admin&password=&channel=1&stream=0.sdp


def create_exp_face_records():
    exp1 = TestExperimentController.create_experiment_default()
    camera1 = camera_controller.create_camera('camera_front', 'stringf', exp1 )
    fr = FaceRecorder(True)
    # create_person_face_records(exp1, fr, camera1, 'Daniel', '/dados/face_bds/sessaocachu/avi/dan_1.avi')
    # TODO - record faces actually doesn not create pfr anymore
    pfrc.record_faces_identified_person(exp1, fr, camera1, '/dados/face_bds/sessaocachu/avi/bia_1.avi', 'Bianca')
    pfrc.record_faces_identified_person(exp1, fr, camera1, '/dados/face_bds/sessaocachu/avi/bruna_1.avi', 'Bruna')
    pfrc.record_faces_identified_person(exp1, fr, camera1, '/dados/face_bds/sessaocachu/avi/carol_1.avi', 'Carol')
    pfrc.record_faces_identified_person(exp1, fr, camera1, '/dados/face_bds/sessaocachu/avi/de_1.avi', 'Denis')
    pfrc.record_faces_identified_person(exp1, fr, camera1, '/dados/face_bds/sessaocachu/avi/mae_1.avi', 'Lia')
    pfrc.record_faces_identified_person(exp1, fr, camera1, '/dados/face_bds/sessaocachu/avi/miguel_1.avi', 'Miguel')
    pfrc.record_faces_identified_person(exp1, fr, camera1, '/dados/face_bds/sessaocachu/avi/nina_1.avi', 'Nina')
    pfrc.record_faces_identified_person(exp1, fr, camera1, '/dados/face_bds/sessaocachu/avi/nana_1.avi', 'Nana')
    return exp1


class TestFaceRecorder(TestCaseWithDatabase):

    def test_create_person_face_records(self):
        create_exp_face_records()
        exp1 = em.dao.get_object_by_id(Experiment, 1)
        self.assertEqual(8, len(exp1.persons))
        for person in exp1.persons:
            self.assertIsNotNone(person.person_face_records)
            self.assertGreater(len(person.face_records), 10)
        # TODO check files


if __name__ == '__main__':
    unittest.main()
