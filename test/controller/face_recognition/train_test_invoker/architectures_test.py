# from face_recognition.train_test_invoker.train_test_invoker import invoke_train_and_test
#
#
# if __name__ == '__main__':
#     # Experiment Parameters
#     exp = {}
#     exp["case"] = "sessao_cachu_face_train"
#     exp["source_face_database_dir"] = "/media/denis/dados/face_bds/sessaocachu_face_face_size_40+0_with_test/train"
#
#     exp["face_items_ini"] = 1
#     exp["face_items_fin"] = 200
#     exp["train_steps"] = 2000
#     exp["test_percent"] = 0
#     exp["is_extract_face"] = False
#     exp["min_face_width"] = 40
#     exp["face_border_size"] = 0
#
#
#     # exp["tensor_dir"] = "/cloud/dev/tensorflow-for-poets-2/"
#     exp["tensor_dir"] = "/dados/dev/tf_work_dir/"
#     exp["model_dir"] = exp["tensor_dir"] + 'models'
#     exp["case_dir"] = "{0}tf_files/{1}/".format(exp["tensor_dir"],  exp["case"])
#     exp["summaries_root_dir"] = exp["tensor_dir"] + "training_summaries/"
#     exp["exp_backup"] = "/dados/dev/training_sums/"
#     # exp["random_scale"]
#     # exp["random_brightness"]
#     # exp["random_crop"]
#     flag_do_backup = True
#     flag_create_dirs = True
#     flag_train = True
#     flag_test = False
#     # ===================================================
#
#     # for arch_name in ["mobilenet", "inception_v3"]:
#     # for arch_name in ["inception_v3"]:
#     for arch_name in ["mobilenet"]:
#         if arch_name == "inception_v3":
#             # from master
#             exp["architecture"] = arch_name
#             exp["input_height"] = 299
#             exp["input_width"] = 299
#             exp["input_mean"] = 0
#             exp["input_std"] = 255
#             invoke_train_and_test(exp, flag_train, flag_test, flag_create_dirs, flag_do_backup)
#         elif arch_name == "mobilenet":
#             for image_size in [128, 160, 192, 224]:
#                 exp["input_height"] = image_size
#                 exp["input_width"] = image_size
#                 exp["input_mean"] = 128
#                 exp["input_std"] = 128
#                 for relative_size in ["1.0"]:
#                 # for relative_size in ["0.25", "0.50", "0.75", "1.0"]:
#                     exp["architecture"] = "mobilenet_{0}_{1}".format(relative_size, image_size)
#                     invoke_train_and_test(exp,  flag_train, flag_test, flag_create_dirs, flag_do_backup)
