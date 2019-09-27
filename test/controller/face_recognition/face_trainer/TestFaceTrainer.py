import os
import shutil
import unittest
import operator

from src.business.TrainConfiguration import TrainConfiguration
from src.controller import camera_controller
from src.controller import person_face_records_controller as pfrc
from src.controller import train_configuration_controller as tcc
from src.controller import train_execution_controller as train_ec
from src.controller import experiment_controller as ec
from src.controller.face_recognition.train_test_invoker import train_test_invoker
from src.dao.PersonFaceRecordsDao import PersonFaceRecordsDao as pfrdao
from src.debug.debugutils import DebugUtils
from test.controller.TestCaseWithDatabase import TestCaseWithDatabase
from test.controller.experiment_controller import TestExperimentController as tec
from datetime import datetime

debug = DebugUtils.get_instance()


class TestFaceTrainer(TestCaseWithDatabase):

    # def test_face_trainer(self):
    #
    #     exp = TestFaceRecorder.create_exp_face_records()
    #
    #     train = tcc.create_train_configuration(100, 128)
    #     camera = camera_controller.get_object_by_id(1)
    #
    #     results = {}
    #     for image_size in (128, 160, 192, 224):
    #         tcc.set_image_size(train, image_size)
    #         train_exec = train_test_invoker.invoke_trainer(exp, train)
    #         results[image_size] = train_exec.test_accuracy
    #         self.assertGreater(train_exec.test_accuracy, 0.80)
    #     # TODO - acuraccy varying
    #     debug.msg('Results:')
    #     for image_size, accuracy in results.items():
    #         debug.msg('Test accuracy for image size {}: {}'.format(image_size, '{0:.4f}%%'.format(accuracy*100)))
    #     # self.assertAlmostEquals(train_exec.test_accuracy.item(), 0.88461536)
    #     # self.assertAlmostEquals(train_exec.test_accuracy.item(), 0.92307692)
    #     # self.assertAlmostEquals(train_exec.test_accuracy.item(), 0.96153843)
    #     # self.assertAlmostEquals(train_exec.test_accuracy.item(), 0.92307692)

    def test_face_trainer_lfw(self):

        tfe = tec.create_tf_env_default()
        # Experiment LFW
        exp = tec.create_experiment('lfw', tfe)
        logfilename = "{}{date:%Y%m%d-%H%M%S}.txt".format(exp.log_dir(), date=datetime.now())
        DebugUtils.get_instance().set_logfilename(logfilename)
        DebugUtils.get_instance().open_file()
        camera = camera_controller.create_camera('camera_front', 'stringf', exp)

        dir_lfw = '/media/denis/dados/face_bds/lfw_face100_min30_max500'
        for person_name in os.listdir(dir_lfw):
            try:
                shutil.copytree(os.path.join(dir_lfw, person_name), os.path.join(exp.face_records_dir(), person_name))
            except FileExistsError:
                pass

        for person_name in os.listdir(exp.face_records_dir()):

            pfr = pfrdao.create_person_face_records(exp, person_name, camera)
            pfrdao.update_object(pfr.person)

            fnumber = 0
            person = pfr.person
            for file in [f for f in os.listdir(person.person_db_dir()) if
                         os.path.isfile(os.path.join(person.person_db_dir(), f))]:
                fnumber += 1
                pfrc.person_add_face_record(person, file)

        train = tcc.create_train_configuration(5000, 128)
        id_train = train.id
        id_exp = exp.id

        results = {}
        for image_size in reversed(TrainConfiguration.get_architecture_sizes()):
            for relative_size in TrainConfiguration.get_architecture_relative_sizes():
        # for image_size in ['224']:
        #     for relative_size in ['0.50']:
                tcc.set_image_size(train, int(image_size))
                tcc.set_relative_size(train, relative_size)
                train_exec = train_test_invoker.invoke_trainer(exp, train)
                # Connection is loosy, invoke_trainer reconnects
                train = tcc.get_object_by_id(id_train)
                exp = ec.get_object_by_id(id_exp)
                results['{}_{}'.format(image_size, relative_size)] = train_exec.test_accuracy
                # TODO - accuracy varying
                # self.assertGreater(train_exec.test_accuracy, 0.80)
                debug.flush_file()

        debug.msg('Results:')
        configs = results.keys()
        for config in sorted(configs):
            debug.msg('Test accuracy for {}: {}'.format(config, '{0:.4f}%%'.format(results[config] * 100)))

        # self.assertAlmostEquals(train_exec.test_accuracy.item(), 0.88461536)
        # self.assertAlmostEquals(train_exec.test_accuracy.item(), 0.92307692)
        # self.assertAlmostEquals(train_exec.test_accuracy.item(), 0.96153843)
        # self.assertAlmostEquals(train_exec.test_accuracy.item(), 0.92307692)


if __name__ == '__main__':
    unittest.main()
