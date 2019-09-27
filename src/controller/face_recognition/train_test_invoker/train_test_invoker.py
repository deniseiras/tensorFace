import src.controller.face_recognition.face_tester.tester as tester
import src.controller.face_recognition.face_trainer.trainer as trainer
import src.controller.face_recognition.train_test_invoker.directory_manager as dir_manager
from src.controller import train_execution_controller as tec
from src.dao.database.DatabaseController import DatabaseController
from src.debug.debugutils import DebugUtils
import os
import shutil

# https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/#3

# Inception V3 has a first-choice accuracy of 78% on ImageNet, but is the model is 85MB, and requires many times more
# processing than even the largest MobileNet configuration, which achieves 70.5% accuracy, with just a 19MB download.
#
# Pick the following configuration options:
#
# Input image resolution: 128,160,192, or 224px. Unsurprisingly, feeding in a higher resolution image takes more
# processing time, but results in better classification accuracy. We recommend 224 as an initial setting.
# The relative size of the model as a fraction of the largest MobileNet: 1.0, 0.75, 0.50, or 0.25. We recommend 0.5 as
# an initial setting. The smaller models run significantly faster, at a cost of accuracy.
# Experiment parameters =============================

debug = DebugUtils.get_instance()


def invoke_create_train_test_face_directories(exp):
    dir_manager.create_train_test_face_directories(exp)


def log_total_individuals_faces(exp):
    train_dirs_count, train_faces_count = dir_manager.get_dir_files_count(exp["train_dir"])
    debug.msg("\nTotal individuals: {}".format(train_dirs_count))
    debug.msg("Total faces: {}".format(train_faces_count))


def invoke_trainer(exp, train_cfg):

    train_exec = tec.create_train_execution(exp, train_cfg, commit=False)
    sub_case = '{}_steps{}_{}'.format(exp.name, train_cfg.train_steps, train_cfg.get_architecture())
    sub_case_dir = "{0}{1}/".format(exp.trains_dir(), sub_case)

    pars = {}
    pars["model_dir"] = exp.tf_env.model_dir
    pars["summaries_dir"] = exp.tf_env.summaries_dir + sub_case
    pars["bottlenecks_dir"] = "{0}bottlenecks".format(sub_case_dir)
    pars["model_file"] = "{0}retrained_graph.pb".format(sub_case_dir)
    pars["label_file"] = "{0}retrained_labels.txt".format(sub_case_dir)
    pars["architecture"] = train_cfg.get_architecture()
    pars["train_steps"] = train_cfg.train_steps
    pars["testing_percentage"] = train_cfg.testing_percentage
    pars["validation_percentage"] = train_cfg.validation_percentage
    pars["train_dir"] = exp.face_records_dir()
    pars["random_brightness"] = train_cfg.random_brightness
    pars["random_scale"] = train_cfg.random_scale
    pars["random_crop"] = train_cfg.random_crop
    # pars["train_dir"] = "{0}train/".format(sub_case_dir)
    # pars["test_dir"] = "{0}test/".format(sub_case_dir)
    # if flag_create_dirs:
    # invoke_create_train_test_face_directories(pars)
    train_exec.sub_case_dir = sub_case_dir
    train_exec.model_dir = pars["model_dir"]
    train_exec.summaries_dir = pars["summaries_dir"]
    train_exec.bottlenecks_dir = pars["bottlenecks_dir"]
    train_exec.model_file = pars["model_file"]
    train_exec.label_file = pars["label_file"]
    train_exec.train_dir = pars["train_dir"]
    tec.dao.update_object(train_exec)
    id_train_exec = train_exec.id

    log_total_individuals_faces(pars)

    debug.msg("\n============== Experiment {} ==================".format(pars["architecture"]))
    debug.msg("Train Steps:{}".format(pars["train_steps"]))
    debug.msg("Test Percent:{}".format(pars["testing_percentage"]))
    # if flag_backup_files:
    #     shutil.copytree(exp["summaries_dir"], "{}summaries".format(backup_sub_case_dir))
    #     shutil.copytree(sub_case_dir, "{}tf_files".format(backup_sub_case_dir))
    test_accuracy = trainer.train(pars)
    #TODO reconnect (after long time)    looses outher objects in caller of this
    # dbc = DatabaseController.get_instance()
    # dbc.reconnect()
    train_exec = tec.get_object_by_id(id_train_exec)
    train_exec.test_accuracy = test_accuracy
    tec.dao.update_object(train_exec)
    return train_exec


def invoke_test_file(pars, file_name):
    # pars = create_test_params(train_exec)
    # debug.msg("\n\nTESTING file {} \n\n".format(file_name))
    labels_results, time_exec = tester.test(pars, file_name)
    if len(labels_results) == 0:
        debug.msg("File not exists")

    return labels_results, time_exec


def invoke_test_test_dir(test_config):
    pars = create_test_params(test_config.train_exec)
    debug.msg("\n\n ===> TESTING files in {} \n\n".format(test_config.test_dir))
    debug.msg(('\n Using model {}'.format(test_config.train_exec.model_file)))
    debug.msg(('\n Using labels {}'.format(test_config.train_exec.label_file)))
    files_tested = 0
    time_exec_total = 0
    all_results = []
    for root, dirs, files in os.walk(test_config.train_exec.test_dir):
        for file in files:
            if file.endswith(".jpg"):
                file_name = os.path.join(root, file)
                # TODO entender / Testar std, mean
                # time_exec = test_label_image_func(sub_case_dir, file_name, image_size, image_size, input_mean, input_std)
                all_results.append(results)
                labels, results, time_exec = tester.test(pars, file_name)
                # debug.msg(" ===> file tested in {} milliseconds".format(time_exec))
                time_exec_total += time_exec
                files_tested += 1
    if files_tested == 0:
        debug.msg("No files tested")
    else:
        avg_time_tested = time_exec_total / files_tested
        debug.msg("\n{0} files tested in {1} seconds. Average time = {2} miliseconds".format(files_tested,
                                                                                             time_exec_total / 1000,
                                                                                             avg_time_tested))
        debug.flush_file()

    return labels, all_results, files_tested, time_exec_total


def create_test_params(train_exec):
    pars = {}
    pars["architecture"] = train_exec.arch_name
    pars["input_height"] = train_exec.input_height
    pars["input_width"] = train_exec.input_width
    pars["input_mean"] = train_exec.input_mean
    pars["input_std"] = train_exec.input_std
    pars["model_file"] = train_exec.model_file
    pars["label_file"] = train_exec.label_file
    return pars
#
# def invoke_train_and_test(exp, flag_train, flag_test, flag_create_dirs, flag_backup_files):
#     if exp["is_extract_face"]:
#         is_face_str = "face_size_{}+{}".format(exp["min_face_width"], exp["face_border_size"])
#     else:
#         is_face_str = "whole"
#     exp["sub_case"] = '{}_{}_itens{}-{}_steps{}_test{}_{}'.format(exp["case"], is_face_str, exp["face_items_ini"],
#                                                                   exp["face_items_fin"], exp["train_steps"],
#                                                                   exp["test_percent"],
#                                                                   exp["architecture"])
#     exp["sub_case_dir"] = "{0}{1}/".format(exp["case_dir"], exp["sub_case"])
#     exp["train_dir"] = "{0}train/".format(exp["sub_case_dir"])
#     exp["test_dir"] = "{0}totest/".format(exp["sub_case_dir"])
#     exp["summaries_dir"] = exp["summaries_root_dir"] + exp["sub_case"]
#     exp["bottlenecks_dir"] = "{0}bottlenecks".format(exp["sub_case_dir"])
#     exp["model_file"] = "{0}retrained_graph.pb".format(exp["sub_case_dir"])
#     exp["label_file"] = "{0}retrained_labels.txt".format(exp["sub_case_dir"])
#     backup_sub_case_dir = "{}{}/".format(exp["exp_backup"], exp["sub_case"])
#     if flag_backup_files:
#         if os.path.isdir(backup_sub_case_dir):
#             shutil.rmtree(backup_sub_case_dir)
#     if flag_create_dirs:
#         invoke_create_train_test_face_directories(exp)
#     # # debug_fname = "{}{date:%Y%m%d-%H%M%S}.txt".format(exp["sub_case_dir"], date=datetime.datetime.now())
#     # debug = DebugUtils.get_instance(0, debug_fname)
#     log_total_individuals_faces(exp)
#
#     debug.msg("\n============== Experiment {} ==================".format(exp["architecture"]))
#     debug.msg("Face / whole image:{}".format(is_face_str))
#     debug.msg("Train Steps:{}".format(exp["train_steps"]))
#     debug.msg("Test Percent:{}".format(exp["test_percent"]))
#     if flag_train:
#         invoke_trainer(exp)
#     if flag_test:
#         invoke_test_test_dir(exp)
#     if flag_backup_files:
#         shutil.copytree(exp["summaries_dir"], "{}summaries".format(backup_sub_case_dir))
#         shutil.copytree(exp["sub_case_dir"], "{}tf_files".format(backup_sub_case_dir))
