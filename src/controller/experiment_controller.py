import os
from src.business.Experiment import Experiment
from src.business.TensorFlowEnv import TensorFlowEnv
from src.dao.GenericDao import GenericDao

dao = GenericDao


def get_object_by_id(q_id):
    return dao.get_object_by_id(Experiment, q_id)


def save_tf_env(tfe):
    tfe.make_default_values()
    dao.update_object(tfe)
    create_tf_env_dirs(tfe)


def create_tf_env(tf_root_dir):
    # Tensor Flow Env
    tfe = TensorFlowEnv(root_dir=tf_root_dir)
    tfe.make_default_values()
    dao.update_object(tfe)
    return tfe


def create_tf_env_dirs(tfe):
    os.makedirs(tfe.tf_files_dir, exist_ok=True)
    os.makedirs(tfe.summaries_dir, exist_ok=True)


def create_experiment(name, tf_env, commit=True):
    # TODO check best places - create envs, records
    exp1 = Experiment(name=name, tf_env=tf_env)
    exp1.make_default_values()
    dao.update_object(exp1, commit=commit)
    return exp1


def create_exp_dirs(exp1):
    os.makedirs(exp1.face_records_dir(), exist_ok=True)
    os.makedirs(exp1.log_dir(), exist_ok=True)
    os.makedirs(exp1.tests_dir(), exist_ok=True)
    os.makedirs(exp1.trains_dir(), exist_ok=True)
    os.makedirs(exp1.suspect_dir(), exist_ok=True)
    # debug_fname = "{}{date:%Y%m%d-%H%M%S}.txt".format(exp1.log_dir(), date=datetime.now())
    # debug = DebugUtils.get_instance(1000, debug_fname)


