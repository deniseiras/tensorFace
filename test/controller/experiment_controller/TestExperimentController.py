import os
import unittest
from test.controller.TestCaseWithDatabase import TestCaseWithDatabase
import src.controller.experiment_controller as em
from src.business.Experiment import Experiment


def create_tf_env_default():
    # Tensor Flow Env
    tfe = em.create_tf_env('/media/denis/dados/dev/tensorface_data/')
    em.create_tf_env_dirs(tfe)
    return tfe


def create_experiment(exp_name, tfe):
    exp1 = em.create_experiment(exp_name, tfe)
    em.create_exp_dirs(exp1)
    return exp1


def create_experiment_default():
    # Tensor Flow Env
    tfe = create_tf_env_default()
    # Experiment
    exp1 = create_experiment('sessao_cachu', tfe)
    return exp1


class TestExperimentController(TestCaseWithDatabase):

    def test_create_experiment(self):
        create_experiment_default()
        exp1 = em.dao.get_object_by_id(Experiment, 1)
        tfe = exp1.tf_env
        self.assertEqual(exp1.name, 'sessao_cachu')
        self.assertEqual(tfe.root_dir, '/media/denis/dados/dev/tensorface_data/')
        self.assertTrue(os.path.exists(exp1.log_dir()))
        self.assertTrue(os.path.exists(exp1.trains_dir()))
        self.assertTrue(os.path.exists(exp1.trains_dir()))
        self.assertTrue(os.path.exists(exp1.face_records_dir()))
        self.assertTrue(os.path.exists(exp1.suspect_dir()))


if __name__ == '__main__':
    unittest.main()

