from src.controller import camera_controller, experiment_controller as em
from test.controller.experiment_controller import TestExperimentController
from test.controller.TestCaseWithDatabase import TestCaseWithDatabase
from src.business.Experiment import Experiment

import unittest


class TestCameraController(TestCaseWithDatabase):

    def test_create_cameras_in_experiment(self):
        exp1 = TestExperimentController.create_experiment_default()
        cam_e = camera_controller.create_camera('cam_e', 'Entrance Camera', exp1)
        cam_x = camera_controller.create_camera('cam_x', 'Exit Camera', exp1)
        exp1 = em.dao.get_object_by_id(Experiment, 1)

        cam_e = camera_controller.get_object_by_id(2)
        self.assertEqual(cam_e.name, 'cam_x')
        self.assertEqual(len(exp1.cameras), 2)


if __name__ == '__main__':
    unittest.main()
