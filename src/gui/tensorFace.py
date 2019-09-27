import math
import os
import shutil
import sys

from sqlalchemy import and_, or_

from src.business.Camera import *
from src.business.Experiment import Experiment
from src.business.Person import *
from src.business.PersonFaceRecords import PersonFaceRecords
from src.business.TensorFlowEnv import TensorFlowEnv
from src.business.TrainConfiguration import TrainConfiguration
from src.business.TrainExecution import TrainExecution
from src.controller import camera_controller as cc
from src.controller import experiment_controller as ec
from src.controller import person_face_records_controller as pfrc
from src.controller import train_configuration_controller as tcc
from src.controller.face_detector.FaceDetector import FaceDetector
from src.controller.face_recognition.train_test_invoker import train_test_invoker as tti
from src.controller.video_capture.VideoCaptureOpenCV import VideoCaptureOpenCV
from src.dao.database.DatabaseController import DatabaseController
from src.util.string_utils import *

if sys.version_info[0] == 3:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *

from src.gui import tensorFaceGui


# TODO
#

class TensorFaceController(QMainWindow, tensorFaceGui.Ui_Dialog):
    filechoose = ''
    wMessage = ''
    dbc = None
    session = None
    m_tensor_flow_env = None
    m_experiment = None
    m_camera = None
    m_person = None
    m_pfr = None
    cam_display = None
    person_display = None
    face_recorder = None
    person_curr_face_num = -1
    control_curr_face_num = -1
    m_train = None
    m_result = None
    control_display_1 = None
    face_recognizer_1 = None
    control_display_2 = None
    face_recognizer_2 = None
    control_display_face = None
    tface_data_dir = 'src/gui'
    splashPixMap = None
    splash = None
    queue_recog = None
    queue_recog_num_of_recogs = None
    queue_recog_total_time = None

    def __init__(self):

        super().__init__()
        self.setupUi(self)  # TODO - second line works insisde pycharm
        # self.splashPixMap = QPixmap("{}/tface_logo.png".format(self.tface_data_dir))
        self.splashPixMap = QPixmap("{}/tface_logo.png".format('.'))
        self.splashPixMap = self.splashPixMap.scaled(self.splashPixMap.size(), Qt.KeepAspectRatio,
                                                     Qt.SmoothTransformation)
        self.splash = QSplashScreen(self.splashPixMap)
        self.splashMessage('Intializing ...')
        # File select buttons
        # self.sf01Button.clicked.connect(self.fntBt01)

        self.connect_to_db()
        self.init_actions()
        self.load_general_cfg_tab()
        self.refresh_list_experiments()
        self.configure_list_columns()
        self.refresh_list_cameras()
        self.refresh_list_persons()
        self.refresh_person_from_selected()
        self.refresh_combo_person_cameras()
        self.refresh_list_trains()
        self.refresh_list_trains_2()
        self.refresh_combo_control_cameras()
        self.refresh_list_control()
        self.clearSplash()

    def configure_list_columns(self):
        self.cam_list.setColumnWidth(0, 233)
        self.cam_list.setColumnWidth(1, 0)
        self.train_list.setColumnWidth(0, 125)
        self.train_list.setColumnWidth(1, 75)
        self.train_list.setColumnWidth(2, 55)
        self.train_list.setColumnWidth(3, 0)
        self.train_list_2.setColumnWidth(0, 100)
        self.train_list_2.setColumnWidth(1, 70)
        self.train_list_2.setColumnWidth(2, 70)
        self.train_list_2.setColumnWidth(3, 45)
        self.train_list_2.setColumnWidth(4, 55)
        self.person_list.setColumnWidth(0, 225)
        self.person_list.setColumnWidth(1, 0)
        self.control_list.setColumnWidth(0, 115)
        self.control_list.setColumnWidth(1, 115)
        self.control_list.setColumnWidth(2, 230)
        self.control_list.setColumnWidth(3, 115)
        self.control_list.setColumnWidth(4, 230)
        self.control_list.setColumnWidth(5, 0)

    def init_actions(self):
        self.general_cfg_save.clicked.connect(self.save_general_cfg_tab)
        self.exp_new.clicked.connect(self.new_experiment)
        self.exp_save.clicked.connect(self.save_experiment)
        self.exp_list.itemSelectionChanged.connect(self.refresh_experiment_from_selected)
        self.exp_delete.clicked.connect(self.delete_experiment)

        self.cam_new.clicked.connect(self.new_camera)
        self.cam_save.clicked.connect(self.save_camera)
        self.cam_list.itemSelectionChanged.connect(self.refresh_camera_from_selected)
        self.cam_delete.clicked.connect(self.delete_camera)
        self.cam_start.clicked.connect(self.cam_start_display)
        self.cam_stop.clicked.connect(self.cam_stop_display)
        self.cam_face_capture_min_width_auto_true.clicked.connect(self.cam_enable_disable_min_fixed)
        self.cam_face_capture_min_width_auto_false.clicked.connect(self.cam_enable_disable_min_fixed)

        self.person_new.clicked.connect(self.new_person)
        self.person_save.clicked.connect(self.save_person)
        self.person_list.itemSelectionChanged.connect(self.refresh_person_from_selected)
        self.person_delete.clicked.connect(self.delete_person)
        self.person_record_faces.clicked.connect(self.person_start_display)
        self.person_stop_record_faces.clicked.connect(self.person_stop_display)
        self.person_face_delete.clicked.connect(self.person_delete_face)
        self.person_goto_face_first.clicked.connect(self.person_display_face_first)
        self.person_goto_face_last.clicked.connect(self.person_display_face_last)
        self.person_goto_face_next.clicked.connect(self.person_display_face_next)
        self.person_goto_face_prev.clicked.connect(self.person_display_face_prev)
        self.person_convert_person.clicked.connect(self.person_convert_person_clicked)
        self.person_import_faces.clicked.connect(self.person_import_faces_clicked)

        self.train_new.clicked.connect(self.new_train)
        self.train_save.clicked.connect(self.save_train)
        self.train_list.itemSelectionChanged.connect(self.refresh_train_from_selected)
        self.train_list_2.itemSelectionChanged.connect(self.refresh_train_2_from_selected)
        self.train_delete.clicked.connect(self.delete_train)
        self.train_execute.clicked.connect(self.execute_train)
        self.train_fill_architectures()
        self.train_fill_architecture_size()
        self.train_fill_relative_size()

        self.control_record_faces_1.clicked.connect(lambda: self.control_start_recognize('control_display_1',
                                                                                         'face_recognizer_1',
                                                                                         self.control_camera_1,
                                                                                         self.control_train_1,
                                                                                         self.control_face_opt_entrance,
                                                                                         self.control_suspect_1,
                                                                                         self.control_graphics_1))
        self.control_record_faces_2.clicked.connect(lambda: self.control_start_recognize('control_display_2',
                                                                                         'face_recognizer_2',
                                                                                         self.control_camera_2,
                                                                                         self.control_train_2,
                                                                                         self.control_face_opt_exit,
                                                                                         self.control_suspect_2,
                                                                                         self.control_graphics_2))
        self.control_record_stop_record_1.clicked.connect(
            lambda: self.control_stop_recognize('control_display_1', 'face_recognizer_1'))
        self.control_record_stop_record_2.clicked.connect(
            lambda: self.control_stop_recognize('control_display_2', 'face_recognizer_2'))
        # self.control_list.clicked.connect(self.refresh_control_from_selected)
        self.control_list.itemSelectionChanged.connect(self.refresh_control_from_selected)
        # self.control_list.itemSelectionChanged
        self.control_goto_face_first.clicked.connect(self.control_display_face_first)
        self.control_goto_face_last.clicked.connect(self.control_display_face_last)
        self.control_goto_face_next.clicked.connect(self.control_display_face_next)
        self.control_goto_face_prev.clicked.connect(self.control_display_face_prev)
        self.control_face_delete.clicked.connect(self.control_delete_face)
        self.control_pfr_recog_all.clicked.connect(self.control_pfr_recog_all_clicked)

    def connect_to_db(self):
        db_name = 'ALFA'
        db_url = 'mysql://root:sk8ordie@localhost:3306'
        self.dbc = DatabaseController.get_instance()
        self.dbc.connect(db_url, use_db=db_name)
        self.dbc.create_tables()
        self.session = self.dbc.get_session()

    def closeEvent(self, QCloseEvent):
        QMainWindow.closeEvent(self, QCloseEvent)
        self.sair()

    def sair(self):
        # self.information_message('See you soon!')
        self.close()
        self.destroy()
        exit(0)

    def warning_message(self, msg):
        QMessageBox.warning(self, 'Warning', msg, QMessageBox.Ok)

    def information_message(self, msg):
        QMessageBox.information(self, 'Information', msg)

    # TODO -AttributeError: 'builtin_function_or_method' object has no attribute 'showMessage'
    def status_message(self, msg):
        self.status_bar.setText(msg)

    def clear_status_message(self):
        self.status_bar.setText('')

    def splashMessage(self, msg):
        self.splash.show()
        self.splash.showMessage(msg, alignment=Qt.AlignHCenter)
        self.status_message(msg)
        self.splash.repaint()

    def clearSplash(self):
        self.splash.clearMessage()
        self.splash.hide()
        self.clear_status_message()

    def about(self):
        QMessageBox.about(self, 'TensorFace 1.0', '\n' + 'By Denis Eiras'.center(40, ' ') +
                          '\n\n' + '2018'.center(40, ' ') + '\n\n' + 'Brazil'.center(40, ' ') + '\n')

    # ======================= GENERAL CONFIG  =============================
    # =============================================================

    def load_general_cfg_tab(self):
        self.m_tensor_flow_env = ec.dao.get_object_by_id(TensorFlowEnv, 1)
        self.env_root_dir.setText(self.m_tensor_flow_env.root_dir)

    def save_general_cfg_tab(self):
        env_root_dir = self.env_root_dir.text().strip()
        if len(env_root_dir) > 0:
            self.m_tensor_flow_env.root_dir = env_root_dir
            ec.save_tf_env(self.m_tensor_flow_env)
            self.information_message('Directory created sucessfully!')

    def disable_buttons(self, is_disabled):
        self.cam_new.setDisabled(is_disabled)
        self.cam_save.setDisabled(is_disabled)
        self.cam_delete.setDisabled(is_disabled)
        self.person_new.setDisabled(is_disabled)
        self.person_save.setDisabled(is_disabled)
        self.person_delete.setDisabled(is_disabled)
        self.person_face_delete.setDisabled(is_disabled)
        self.disable_person_buttons(is_disabled)
        self.control_face_delete.setDisabled(is_disabled)

    def disable_person_buttons(self, is_disabled):
        self.person_goto_face_prev.setDisabled(is_disabled)
        self.person_goto_face_next.setDisabled(is_disabled)
        self.person_goto_face_last.setDisabled(is_disabled)
        self.person_goto_face_first.setDisabled(is_disabled)
        self.person_face_delete.setDisabled(is_disabled)
        self.person_convert_person.setDisabled(is_disabled)
        self.person_save.setDisabled(is_disabled)
        self.person_camera.setDisabled(is_disabled)
        self.person_import_faces.setDisabled(is_disabled)

    # ======================= EXPERIMENT  =============================
    # =============================================================
    def refresh_experiment_from_selected(self):
        item = self.exp_list.currentItem()
        if item is not None and len(item.text()) > 0:
            exp_name = item.text()
            self.m_experiment = self.session.query(Experiment).filter(Experiment.name == exp_name)[0]
            self.exp_name.setText(exp_name)
            self.exp_root_dir.setText(self.m_experiment.exp_root_dir())
            self.exp_face_records_dir.setText(self.m_experiment.face_records_dir())
            self.exp_trains_dir.setText(self.m_experiment.trains_dir())
            self.exp_suspect_dir.setText(self.m_experiment.suspect_dir())
            self.exp_face_width.setText(str(self.m_experiment.face_width))
            # self.exp_log_dir.setText(self.m_experiment.log_dir())
        else:
            self.m_experiment = None
            exp_name = '-'
            self.exp_name.setText(exp_name)
            self.reset_exp_values()
            # self.exp_log_dir.setText(empty_str)

        self.refresh_experiments_texts(exp_name)
        self.disable_buttons(self.m_experiment is None)
        self.reset_camera_default_values()
        self.refresh_list_cameras()
        self.reset_person_default_values()
        self.refresh_list_persons()
        self.refresh_person_from_selected()
        self.refresh_combo_person_cameras()
        self.refresh_list_trains_2()
        self.refresh_combo_control_cameras()
        self.refresh_combos_control_train()
        self.refresh_list_control()
        self.refresh_control_from_selected()

    def refresh_experiments_texts(self, exp_name):
        self.cam_experiment.setText(exp_name)
        self.train_experiment.setText(exp_name)
        self.control_experiment.setText(exp_name)
        self.person_experiment.setText(exp_name)

    def reset_exp_values(self):
        empty_str = '-'
        self.exp_root_dir.setText(empty_str)
        self.exp_face_records_dir.setText(empty_str)
        self.exp_trains_dir.setText(empty_str)
        self.exp_suspect_dir.setText(empty_str)
        self.exp_face_width.setText(str(160.0))

    def new_experiment(self):
        self.exp_list.setRowCount(self.exp_list.rowCount() + 1)
        self.exp_name.setText('New experiment')
        self.reset_exp_values()
        exp_name = self.exp_name.text().strip()
        self.m_experiment = ec.create_experiment(exp_name, self.m_tensor_flow_env, commit=False)
        self.exp_save.setDisabled(False)
        self.exp_list.setCurrentCell(-1, -1)

    def refresh_list_experiments(self):
        linha = 0
        self.exp_list.clearContents()
        exps = self.session.query(Experiment).order_by(Experiment.name)
        total = exps.count()
        self.exp_list.setRowCount(total)
        for exp in exps:
            item = QTableWidgetItem(exp.name)
            self.exp_list.setItem(linha, 0, item)
            linha += 1
        # TODO default exp attribute
        if linha == 1:
            self.exp_list.selectRow(0)
        self.exp_save.setDisabled(True)
        self.refresh_experiment_from_selected()

    def save_experiment(self):
        if self.m_experiment is not None:
            exp_name = self.exp_name.text().strip()
            if self.session.query(Experiment).filter(Experiment.name == exp_name).count() > 0:
                self.warning_message('Experiment already exists!')
            else:
                self.m_experiment.name = exp_name
                self.m_experiment.make_default_values()
                self.m_experiment.face_width = mk_float(self.exp_face_width.text())
                ec.dao.update_object(self.m_experiment)
                ec.create_exp_dirs(self.m_experiment)
                self.refresh_list_experiments()
                self.information_message('Experiment and directories created sucessfully!')
                self.exp_save.setDisabled(True)
        else:
            self.information_message('Please input a non blank text.')

    def delete_experiment(self):
        if self.m_experiment is not None:
            ec.dao.delete_object(self.m_experiment)
            self.information_message('Experiment deleted sucessfully!')
            self.refresh_list_experiments()
        else:
            self.information_message('None item selected!')

    # ======================= CAMERA  =============================
    # =============================================================
    def new_camera(self):
        # self.m_camera = None
        self.cam_list.setRowCount(self.cam_list.rowCount() + 1)
        self.m_camera = cc.create_camera('new_cam', '', self.m_experiment)
        self.refresh_list_cameras()
        self.cam_list.selectRow(self.session.query(Camera).filter(Camera.experiment == self.m_experiment).count() - 1)
        self.refresh_camera_from_selected()
        self.cam_save.setDisabled(False)
        # self.reset_camera_default_values()
        # self.cam_list.setCurrentCell(-1, -1)

    def refresh_list_cameras(self):
        linha = 0
        self.cam_list.clearContents()
        cams = self.session.query(Camera).filter(Camera.experiment == self.m_experiment).order_by(Camera.name)
        total = cams.count()
        self.cam_list.setRowCount(total)
        for cam in cams:
            self.refresh_list_cameras_item(cam, linha)
            linha += 1
        self.cam_save.setDisabled(True)

    def refresh_camera_from_selected(self):
        curr_row = self.cam_list.currentRow()
        item = self.cam_list.item(curr_row, 0)
        if item is not None:
            cam_name = item.text()
            self.m_camera = self.session.query(Camera).filter(
                and_(Camera.name == cam_name, Camera.experiment_id == self.m_experiment.id))[0]
            self.cam_experiment.setText(self.m_camera.experiment.name)
            self.cam_name.setText(cam_name)
            if self.m_camera.type == TYPE_ENTRANCE:
                self.cam_type_entrance.setChecked(True)
            elif self.m_camera.type == TYPE_EXIT:
                self.cam_type_exit.setChecked(True)
            else:
                self.cam_type_auxiliar.setChecked(True)
            self.cam_camera_string.setText(str(self.m_camera.camera_string))
            self.cam_x_res.setText(str(self.m_camera.x_res))
            self.cam_y_res.setText(str(self.m_camera.y_res))
            self.cam_focal_distance.setText(str(self.m_camera.focal_distance))
            self.cam_apperture.setText(str(self.m_camera.apperture_size))
            self.cam_floor_height.setText(str(self.m_camera.floor_height))
            self.cam_group_back_sub.setChecked(self.m_camera.back_sub_do)
            self.cam_back_sub_roi_top_border.setText(str(self.m_camera.back_sub_roi_top_border))
            self.cam_back_sub_thresh_num.setText(str(self.m_camera.back_sub_thresh_num))
            self.cam_back_sub_roi_x_start.setText(str(self.m_camera.back_sub_roi_x_start))
            self.cam_back_sub_roi_x_res_reduction.setText(str(self.m_camera.back_sub_roi_x_res_reduction))
            self.cam_roi_reset_millis.setText(str(self.m_camera.reset_time_init_frame_millis))
            self.cam_group_recog.setChecked(self.m_camera.face_detection_do)
            self.cam_face_border_increase_pct.setText(str(self.m_camera.face_border_increase_pct))
            self.cam_face_capture_min_width_auto_true.setChecked(self.m_camera.face_capture_min_width_auto)
            self.cam_face_capture_min_width_auto_false.setChecked(not self.m_camera.face_capture_min_width_auto)
            self.cam_face_capture_min_width_fixed.setText(str(self.m_camera.face_capture_min_width_fixed))
            self.cam_face_capture_min_nighbors.setText(str(self.m_camera.face_capture_min_neighbors))
            self.cam_face_capture_time_interval.setText(str(self.m_camera.face_capture_time_interval))
            self.cam_sensor_size.setText(str(self.m_camera.sensor_size))
            self.cam_horiz_angle.setText(str(self.m_camera.horiz_angle))
            self.cam_vert_angle.setText(str(self.m_camera.vert_angle))
            self.cam_capture_height.setText(str(self.m_camera.capture_height))
            self.cam_face_capture_scale_factor.setText(str(self.m_camera.face_capture_scale_factor))
            self.cam_recog_threads.setText((str(self.m_camera.recog_threads)))
            self.cam_recog_save_timeout.setText((str(self.m_camera.recog_save_timeout)))
            self.cam_recog_real_time.setChecked(self.m_camera.recog_real_time)

            self.cam_start.setDisabled(False)
            self.cam_stop.setDisabled(False)
            self.cam_save.setDisabled(False)

            if self.cam_face_capture_min_width_auto_true.isChecked():
                # TODO - Auto is always 40 - that determines max dist and width
                min_face_width = 40
                self.cam_face_capture_min_width_fixed.setText(str(min_face_width))
                self.cam_face_capture_min_width_fixed.setDisabled(True)
            else:
                self.cam_face_capture_min_width_fixed.setDisabled(False)

            # TODO move to controller
            try:
                # sensor_size = 8.4666582  # 1/3
                # sensor_size = 6.35  # 1/4
                cam = self.m_camera

                # min_distance - formula 1
                confusion_circle = cam.sensor_size * 25.4 / 1500  # 25.4 mm / inch
                hyperf_dist = (cam.focal_distance * cam.focal_distance) / (cam.apperture_size * confusion_circle)
                print(hyperf_dist)

                # min width - formula 6
                # TODO - validar
                min_width = 2 * hyperf_dist * math.tan(math.radians(cam.horiz_angle / 2))
                print(min_width)

                # max distance - formula 7
                # TODO - just a mark to correction factor of the size of the face captured
                cam_face_min_width_correction = cam.face_capture_min_width_fixed # * 0.55
                face_width = self.m_experiment.face_width
                d_max_a = cam.x_res * face_width
                d_max_b = cam_face_min_width_correction * math.tan(math.radians(cam.horiz_angle / 2)) * 2
                d_max = d_max_a / d_max_b
                print(d_max)

                # max width - formula 5 (could be formula 6)
                res_face = cam_face_min_width_correction / face_width
                w_max = cam.x_res / res_face
                print(w_max)

                # cam tilt2
                h_man_max = cam.capture_height
                cam_tilt = 90 - math.atan((cam.floor_height - h_man_max) / d_max) - cam.vert_angle / 2
                print(cam_tilt)

            except Exception as e:
                # debug.msg('Error calculating suggested parameters')
                hyperf_dist = 0
                min_width = 0
                d_max = 0
                w_max = 0
                cam_tilt = 0
                print('Error calculating suggested parameters', e)

            self.cam_min_distance.setText(mk_str_2(hyperf_dist / 1000))
            self.cam_width_at_min_distance.setText(mk_str_2(min_width / 1000))
            self.cam_max_distance.setText(mk_str_2(d_max / 1000))
            self.cam_width_at_max_distance.setText(mk_str_2(w_max / 1000))
            self.cam_tilt.setText(mk_str_2(cam_tilt))
        else:
            self.m_camera = None
            self.reset_camera_default_values()
            self.cam_save.setDisabled(True)

        if self.cam_display:
            self.cam_stop_display()

    def reset_camera_default_values(self):
        self.cam_name.setText('')
        self.cam_type_entrance.setChecked(True)
        self.cam_camera_string.setText('')
        self.cam_x_res.setText(str(0))
        self.cam_y_res.setText(str(0))
        self.cam_focal_distance.setText(str(0))
        self.cam_apperture.setText(str(0))
        self.cam_sensor_size.setText(str(0))
        self.cam_horiz_angle.setText(str(0))
        self.cam_vert_angle.setText(str(0))
        self.cam_floor_height.setText(str(2250.0))
        self.cam_capture_height.setText(str(2250.0))
        self.cam_group_back_sub.setChecked(True)
        self.cam_back_sub_roi_top_border.setText(str(20))
        self.cam_back_sub_thresh_num.setText(str(75))
        self.cam_back_sub_roi_x_start.setText(str(0))
        self.cam_back_sub_roi_x_res_reduction.setText(str(0))
        self.cam_roi_reset_millis.setText(str(0))
        self.cam_group_recog.setChecked(True)
        self.cam_face_border_increase_pct.setText(str(0))
        self.cam_face_capture_min_width_auto_true.click()
        self.cam_face_capture_min_width_fixed.setText(str(40))
        self.cam_face_capture_min_nighbors.setText(str(3))
        self.cam_start.setDisabled(True)
        self.cam_stop.setDisabled(True)
        self.cam_min_distance.setText(str(0))
        self.cam_width_at_min_distance.setText(str(0))
        self.cam_max_distance.setText(str(0))
        self.cam_width_at_max_distance.setText(str(0))
        self.cam_tilt.setText(str(0))
        self.cam_recog_real_time.setChecked(False)

    def refresh_list_cameras_item(self, cam, linha):
        item = QTableWidgetItem(cam.name)
        self.cam_list.setItem(linha, 0, item)
        item = QTableWidgetItem(cam.type)
        self.cam_list.setItem(linha, 1, item)

    def save_camera(self):
        cam_name = self.cam_name.text().strip()
        if len(cam_name) > 0:
            if self.m_camera is None:
                self.m_camera = cc.create_camera(cam_name, self.cam_camera_string.text(), self.m_experiment)
                self.refresh_list_cameras()
                self.cam_list.selectRow(
                    self.session.query(Camera).filter(Camera.experiment_id == self.m_experiment.id).count() - 1)
                msg_ok = 'Camera created sucessfully!'
            else:
                self.m_camera.name = cam_name
                self.m_camera.camera_string = self.cam_camera_string.text()
                if self.cam_type_entrance.isChecked():
                    self.m_camera.type = TYPE_ENTRANCE
                elif self.cam_type_exit.isChecked():
                    self.m_camera.type = TYPE_EXIT
                else:
                    self.m_camera.type = TYPE_AUXILIAR
                self.m_camera.x_res = mk_int(self.cam_x_res.text())
                self.m_camera.y_res = mk_int(self.cam_y_res.text())
                self.m_camera.focal_distance = mk_float(self.cam_focal_distance.text())
                self.m_camera.apperture_size = mk_float(self.cam_apperture.text())
                self.m_camera.sensor_size = mk_float(self.cam_sensor_size.text())
                self.m_camera.horiz_angle = mk_float(self.cam_horiz_angle.text())
                self.m_camera.vert_angle = mk_float(self.cam_vert_angle.text())
                self.m_camera.floor_height = mk_float(self.cam_floor_height.text())
                self.m_camera.capture_height = mk_float(self.cam_capture_height.text())
                self.m_camera.back_sub_do = self.cam_group_back_sub.isChecked()
                self.m_camera.back_sub_thresh_num = mk_float(self.cam_back_sub_thresh_num.text())
                self.m_camera.back_sub_roi_top_border = mk_float(self.cam_back_sub_roi_top_border.text())
                self.m_camera.back_sub_roi_x_start = mk_float(self.cam_back_sub_roi_x_start.text())
                self.m_camera.back_sub_roi_x_res_reduction = mk_float(self.cam_back_sub_roi_x_res_reduction.text())
                self.m_camera.reset_time_init_frame_millis = mk_float(self.cam_roi_reset_millis.text())
                self.m_camera.face_detection_do = self.cam_group_recog.isChecked()
                self.m_camera.face_border_increase_pct = mk_float(self.cam_face_border_increase_pct.text())
                self.m_camera.face_capture_min_width_auto = self.cam_face_capture_min_width_auto_true.isChecked()
                self.m_camera.face_capture_min_width_fixed = mk_int(self.cam_face_capture_min_width_fixed.text())
                self.m_camera.face_capture_min_neighbors = mk_int(self.cam_face_capture_min_nighbors.text())
                self.m_camera.face_capture_time_interval = mk_float(self.cam_face_capture_time_interval.text())
                self.m_camera.face_capture_scale_factor = mk_float(self.cam_face_capture_scale_factor.text())
                self.m_camera.recog_threads = mk_int(self.cam_recog_threads.text())
                self.m_camera.recog_save_timeout = mk_float(self.cam_recog_save_timeout.text())
                self.m_camera.recog_real_time = self.cam_recog_real_time.isChecked()

                msg_ok = 'Camera updated sucessfully!'
                cc.dao.update_object(self.m_camera)
                self.refresh_list_cameras_item(self.m_camera, self.cam_list.currentRow())
                self.refresh_list_cameras()

            self.refresh_camera_from_selected()
            self.refresh_combo_person_cameras()
            self.refresh_combo_control_cameras()
            self.information_message(msg_ok)
        else:
            self.information_message('Please input a non blank text at name.')

    def delete_camera(self):
        if self.m_camera is not None:
            cc.dao.delete_object(self.m_camera)
            self.refresh_list_cameras()
            self.refresh_combo_control_cameras()
            self.refresh_camera_from_selected()
            self.information_message('Camera deleted sucessfully!')
        else:
            self.information_message('None item selected!')

    def cam_start_display(self):
        from src.gui.QGraphicsSceneFaceDetector import QGraphicsSceneFaceDetector
        if not self.cam_display:
            video_capture = VideoCaptureOpenCV(self.m_camera)
            if not video_capture.initialize():
                self.warning_message('The video of camera {} could not be initialized!'.format(self.m_camera.name))
                return
            face_detector = FaceDetector()
            face_detector.is_show_roi_rect = True
            face_detector.video_capture = video_capture
            face_detector.initialize()

            # TODO - capturando res da cam, nao esta sendo possivel setar em VideoCaptureOpenCV
            if mk_int(self.cam_x_res.text()) != face_detector.x_res_cam or \
                    mk_int(self.cam_y_res.text()) != face_detector.y_res_cam:
                self.cam_x_res.setText(str(face_detector.x_res_cam))
                self.cam_y_res.setText(str(face_detector.y_res_cam))
                self.m_camera.x_res = face_detector.x_res_cam
                self.m_camera.y_res = face_detector.y_res_cam
                cc.dao.update_object(self.m_camera)
                self.information_message('Camera resolution updated after capture')
            self.cam_display = QGraphicsSceneFaceDetector(self, face_detector)

            # self.cam_display.setFPS(1)
            self.cam_display.setParent(self)
            # self.cam_display.setWindowFlags(Qt.Tool)

        self.cam_display.start()

    def cam_stop_display(self):
        # self.face_detector.stop()
        self.cam_display.stop()
        self.cam_display.deleteLater()
        self.cam_display = None

    def cam_enable_disable_min_fixed(self):
        self.cam_face_capture_min_width_fixed.setDisabled(self.cam_face_capture_min_width_auto_true.isChecked())

    # ======================= PERSON  =============================
    # =============================================================
    def new_person(self):
        self.person_list.setRowCount(self.person_list.rowCount() + 1)
        self.person_name.setText('New Person')
        self.m_person = pfrc.create_person(self.person_name.text(), self.m_experiment)
        self.refresh_list_persons()
        self.person_list.selectRow(self.person_list.rowCount() - 1)
        self.refresh_person_from_selected()

    def refresh_list_persons(self):
        linha = 0
        self.person_list.clearContents()
        persons = self.session.query(Person).filter(Person.experiment == self.m_experiment)
        total = persons.count()
        self.person_list.setRowCount(total)
        for person in persons:
            self.refresh_list_person_item(person, linha)
            linha += 1
        self.person_save.setDisabled(True)

    def refresh_combo_person_cameras(self):
        self.person_camera.clear()
        self.person_camera.addItems(
            cam.name for cam in self.session.query(Camera).filter(Camera.experiment == self.m_experiment))

    def refresh_person_from_selected(self):
        curr_row = self.person_list.currentRow()
        item = self.person_list.item(curr_row, 0)
        if item is not None:
            person_name = item.text()
            self.m_person = self.session.query(Person).filter(
                and_(Person.name == person_name, Person.experiment_id == self.m_experiment.id))[0]
            self.person_name.setText(self.m_person.name)
            self.person_nick.setText(self.m_person.nick)
            if pfrc.get_person_faces_len(self.m_person) > 0:
                self.person_curr_face_num = 0
            else:
                self.person_curr_face_num = -1
            localization = pfrc.get_person_localization(self.m_person)
            self.person_localization.setText(localization)
            self.person_save.setDisabled(False)
        else:
            self.m_person = None
            self.reset_person_default_values()
            self.person_curr_face_num = -1

        self.person_display_face_last()
        no_person = self.m_person is None
        self.disable_person_buttons(no_person)
        no_cam_selected = len(self.person_camera.currentText()) == 0
        self.person_record_faces.setDisabled(no_cam_selected or no_person)
        self.person_stop_record_faces.setDisabled(no_cam_selected or no_person)
        is_suspect = not no_person and self.m_person.is_suspect
        self.person_convert_person.setDisabled(not is_suspect)
        self.person_suspect_name.setDisabled(not is_suspect)
        self.person_suspect_confidence.setDisabled(not is_suspect)
        if is_suspect:
            self.person_suspect_confidence.setText(
                mk_str_4(self.m_person.person_face_records[0].suspect_confidence * 100) + '%')
            self.person_suspect_name.setText(self.m_person.person_face_records[0].suspect_name)
        else:
            self.person_suspect_confidence.setText('-')
            self.person_suspect_name.setText('-')

    def reset_person_default_values(self):
        self.person_name.setText('')
        self.person_nick.setText('')

    def refresh_list_person_item(self, person, linha):
        item = QTableWidgetItem(person.name)
        self.person_list.setItem(linha, 0, item)
        if person.is_suspect:
            susp_str = person.person_face_records[0].suspect_name
        else:
            susp_str = person.nick
        item = QTableWidgetItem(susp_str)
        self.person_list.setItem(linha, 1, item)

    # TODO - nao permitir validation percent e test percent < 10%
    def save_person(self):
        person_name = self.person_name.text().strip()
        if len(person_name) > 0:
            if self.session.query(Person).filter(
                    and_(or_(Person.name == person_name, Person.nick == pfrc.get_nick(person_name)),
                         Person.id != self.m_person.id), Person.experiment_id == self.m_experiment.id).count() > 0:
                self.warning_message('Person name or nickname already exists')
                return
            pfrc.save_person(self.m_person, person_name)
            self.refresh_list_person_item(self.m_person, self.person_list.currentRow())
            self.refresh_person_from_selected()
            self.refresh_list_control()
            msg_ok = 'Person updated sucessfully!'
            self.information_message(msg_ok)
        else:
            self.information_message('Please input a non blank text at name.')

    def person_convert_person_clicked(self):
        person_new_or_existent, messg = pfrc.convert_suspect_into_person(self.m_person, self.person_suspect_name.text())
        self.m_person = person_new_or_existent
        linha = 0
        for i in range(self.person_list.rowCount()):
            print(self.person_list.item(i, 0).text())
            if self.person_list.item(i, 0).text() == person_new_or_existent.name:
                self.person_list.selectRow(linha)
                self.refresh_list_person_item(person_new_or_existent, linha)
                break
            linha += 1
        self.refresh_list_persons()
        # self.refresh_person_from_selected()
        self.refresh_list_control()
        self.person_list.selectRow(linha)
        self.warning_message(messg)

    def delete_person(self):
        if self.m_person is not None:
            pfrc.delete_person(self.m_person)
            self.person_list.setRowCount(self.person_list.rowCount() - 1)
            self.information_message('Person deleted sucessfully!')
            self.refresh_list_persons()
            self.refresh_person_from_selected()
            self.refresh_list_control()
        else:
            self.information_message('None item selected!')

    def person_start_display(self):
        from src.gui.QGraphicsSceneFaceRecorder import QGraphicsSceneFaceRecorder
        from src.controller.face_recorder.FaceRecorder import FaceRecorder
        if not self.person_display:
            self.face_recorder = FaceRecorder(True)
            cam = self.session.query(Camera).filter(
                and_(Camera.name == self.person_camera.currentText(), Camera.experiment_id == self.m_experiment.id))[0]
            video_capture = VideoCaptureOpenCV(cam)
            if not video_capture.initialize():
                self.warning_message('The video of camera {} could not be initialized!'.format(self.m_camera.name))
            self.face_recorder.video_capture = video_capture
            self.face_recorder.initialize(self.m_person, video_capture)
            self.person_display = QGraphicsSceneFaceRecorder(self.person_graphicsView_video, self.face_recorder)
            # self.person_display.setFPS(1)
            self.person_display.setParent(self)
            self.person_display.start()

    def person_stop_display(self):
        self.splashMessage('Recording faces, please wait ...')
        self.person_display.stop()
        self.face_recorder.stop()
        self.face_recorder.record_faces()
        self.person_display.deleteLater()
        self.person_display = None
        self.clearSplash()

        if pfrc.get_person_faces_len(self.m_person) > 0:
            self.person_curr_face_num = 0
        else:
            self.person_curr_face_num = -1
        self.person_display_face()

    def person_display_face(self):
        import os
        if self.m_person is None or self.person_curr_face_num < 0:
            self.person_face_num_lbl.setText('---')
            self.person_face_filename_lbl.setText('---')
            self.person_graphicsView_picture.setScene(None)
        else:
            frs = pfrc.get_person_faces(self.m_person)
            if frs is None:
                self.person_face_num_lbl.setText('---')
                self.person_face_filename_lbl.setText('---')
                self.person_graphicsView_picture.setScene(None)
            else:
                if self.person_curr_face_num < len(frs):
                    fr = frs[self.person_curr_face_num]
                    if os.path.isfile(fr.filepath()):
                        pix = QPixmap(fr.filepath())
                        scene = QGraphicsScene()
                        scene.addPixmap(pix)
                        self.person_graphicsView_picture.setScene(scene)
                        self.person_graphicsView_picture.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
                        self.person_face_num_lbl.setText(str(self.person_curr_face_num))
                        self.person_face_filename_lbl.setText(fr.filepath())
                    # TODO using in dev
                    # else:
                    #     self.person_delete_face()

    def person_display_face_first(self):
        self.person_curr_face_num = 0
        self.person_display_face()

    def person_display_face_prev(self):
        if self.person_curr_face_num > 0:
            self.person_curr_face_num -= 1
            self.person_display_face()

    def person_display_face_next(self):
        last_idx = pfrc.get_person_faces_len(self.m_person) - 1
        if self.person_curr_face_num < last_idx:
            self.person_curr_face_num += 1
            self.person_display_face()

    def person_display_face_last(self):
        if self.m_person is None or self.person_curr_face_num < 0:
            self.person_face_num_lbl.setText('---')
            self.person_face_filename_lbl.setText('---')
            self.person_graphicsView_picture.setScene(None)
        else:
            self.person_curr_face_num = pfrc.get_person_faces_len(self.m_person) - 1
        self.person_display_face()

    def person_delete_face(self):
        faces = pfrc.get_person_faces(self.m_person)
        if len(faces) > 0:
            if self.person_curr_face_num > 0:
                pfrc.delete_face_record(faces[self.person_curr_face_num])
                self.person_curr_face_num -= 1
            elif self.person_curr_face_num == 0:
                pfrc.delete_face_record(faces[self.person_curr_face_num])

        faces = pfrc.get_person_faces(self.m_person)
        if len(faces) == 0:
            self.person_curr_face_num = -1
        self.person_display_face()

    def person_import_faces_clicked(self):
        faces_dir = self.select_dir("Please select diretory to import files")
        if faces_dir == '':
            return

        self.splashMessage('Importing files')
        fnumber = 0
        os.makedirs(self.m_person.person_db_dir(), exist_ok=True)
        for image_file in os.listdir(faces_dir):
            try:
                if image_file.endswith('.jpg'):
                    shutil.copy(os.path.join(faces_dir, image_file), self.m_person.person_db_dir())
            except (shutil.SameFileError, FileExistsError):
                pass
            fnumber += 1
            pfrc.person_add_face_record(self.m_person, image_file)
        self.clearSplash()
        import_msg = "{} files imported!".format(fnumber)
        self.information_message(import_msg)
        self.status_message(import_msg)

    def select_dir(self, messg):
        return QFileDialog.getExistingDirectory(self, messg)

    # ================== TRAIN ===================================
    # =============================================================
    def refresh_train_from_selected(self):
        curr_row = self.train_list.currentRow()
        item = self.train_list.item(curr_row, 0)
        exist_item = item is not None and len(item.text()) > 0
        if exist_item:
            train_name = item.text()
            self.m_train = self.session.query(TrainConfiguration).filter(TrainConfiguration.name == train_name)[0]
            self.train_name.setText(train_name)
            self.train_architecture.setCurrentText(self.m_train.arch_name)
            self.train_architecture_size.setCurrentText(str(self.m_train.input_height))
            self.train_relative_size.setCurrentText(self.m_train.relative_size)
            self.train_steps.setText(str(self.m_train.train_steps))
            self.train_validation_percentage.setText(str(self.m_train.validation_percentage))
            self.train_testing_percentage.setText(str(self.m_train.testing_percentage))
            self.train_random_brightness.setText(str(self.m_train.random_brightness))
            self.train_random_scale.setText(str(self.m_train.random_scale))
            self.train_random_crop.setText(str(self.m_train.random_crop))
        else:
            self.m_train = None
            self.train_name.setText(None)
            dummy_train = TrainConfiguration()
            dummy_train.make_default_values()

            self.train_architecture.setCurrentText(dummy_train.arch_name)
            self.train_architecture_size.setCurrentText(str(dummy_train.input_height))
            self.train_relative_size.setCurrentText(dummy_train.relative_size)
            self.train_steps.setText(str(dummy_train.train_steps))
            self.train_validation_percentage.setText(str(dummy_train.validation_percentage))
            self.train_testing_percentage.setText(str(dummy_train.testing_percentage))
            self.train_random_brightness.setText(str(dummy_train.random_brightness))
            self.train_random_scale.setText(str(dummy_train.random_scale))
            self.train_random_crop.setText(str(dummy_train.random_crop))

        self.train_execute.setDisabled(not exist_item)
        self.train_save.setDisabled(not exist_item)

    def refresh_train_2_from_selected(self):
        curr_row = self.train_list_2.currentRow()
        item = self.train_list_2.item(curr_row, 0)
        if item is not None and len(item.text()) > 0:
            result_name = item.text()
            self.m_result = self.get_train_result_by_name(result_name, self.m_experiment.id)
            self.train_name_2.setText(result_name)
            self.train_test_accuracy.setText('{0:.4f}%'.format(self.m_result.test_accuracy * 100))
            self.train_architecture_2.setCurrentText(self.m_result.arch_name)
            self.train_architecture_size_2.setCurrentText(str(self.m_result.input_height))
            self.train_relative_size_2.setCurrentText(self.m_result.relative_size)
            self.train_steps_2.setText(str(self.m_result.train_steps))
            self.train_validation_percentage_2.setText(str(self.m_result.validation_percentage))
            self.train_testing_percentage_2.setText(str(self.m_result.testing_percentage))
            self.train_random_brightness_2.setText(str(self.m_result.random_brightness))
            self.train_random_scale_2.setText(str(self.m_result.random_scale))
            self.train_random_crop_2.setText(str(self.m_result.random_crop))
        else:
            self.m_result = None
            self.train_name_2.setText(None)
            dummy_train = TrainConfiguration()
            dummy_train.make_default_values()

            self.train_architecture.setCurrentText(dummy_train.arch_name)
            self.train_architecture_size.setCurrentText(str(dummy_train.input_height))
            self.train_relative_size.setCurrentText(dummy_train.relative_size)
            self.train_steps.setText('')
            self.train_validation_percentage.setText('')
            self.train_testing_percentage.setText('')
            self.train_random_brightness.setText('')
            self.train_random_scale.setText('')
            self.train_random_crop.setText('')

    def new_train(self):

        self.train_list.setRowCount(self.train_list.rowCount() + 1)
        self.train_name.setText('New Train')
        self.m_train = tcc.create_train_configuration(mk_int(self.train_steps.text()),
                                                      mk_int(self.train_architecture_size.currentText()),
                                                      name=self.train_name.text())
        self.refresh_list_trains()
        self.train_list.selectRow(self.session.query(TrainConfiguration).count() - 1)
        self.refresh_train_from_selected()

    def refresh_list_trains(self):
        linha = 0
        self.train_list.clearContents()
        trains = self.session.query(TrainConfiguration)
        total = trains.count()
        self.train_list.setRowCount(total)
        for train in trains:
            item = QTableWidgetItem(train.name)
            self.train_list.setItem(linha, 0, item)
            item = QTableWidgetItem(train.arch_name)
            self.train_list.setItem(linha, 1, item)
            item = QTableWidgetItem(str(train.input_height))
            self.train_list.setItem(linha, 2, item)
            item = QTableWidgetItem(train.relative_size)
            self.train_list.setItem(linha, 3, item)
            linha += 1
        self.refresh_train_from_selected()

    def refresh_list_trains_2(self):
        linha = 0
        self.train_list_2.clearContents()
        results = self.session.query(TrainExecution).filter(TrainExecution.experiment == self.m_experiment)
        total = results.count()
        self.train_list_2.setRowCount(total)
        for result in results:
            item = QTableWidgetItem(result.name)
            self.train_list_2.setItem(linha, 0, item)
            item = QTableWidgetItem('{0:.2f}%'.format(result.test_accuracy * 100))
            self.train_list_2.setItem(linha, 1, item)
            item = QTableWidgetItem(result.arch_name)
            self.train_list_2.setItem(linha, 2, item)
            item = QTableWidgetItem(str(result.input_height))
            self.train_list_2.setItem(linha, 3, item)
            item = QTableWidgetItem(result.relative_size)
            self.train_list_2.setItem(linha, 4, item)
            item = QTableWidgetItem(result.relative_size)
            self.train_list_2.setItem(linha, 5, item)
            linha += 1
        self.refresh_train_2_from_selected()

    def save_train(self):
        train_name = self.train_name.text().strip()
        if len(train_name) > 0:
            if self.m_train is None:
                self.m_train = tcc.create_train_configuration(mk_int(self.train_steps.text()),
                                                              mk_int(self.train_architecture_size.currentText()),
                                                              name=self.train_name.text())
                self.refresh_list_trains()
                self.information_message('Train configuration created sucessfully!')
            else:
                self.m_train.name = train_name
                self.m_train.arch_name = self.train_architecture.currentText()
                self.m_train.set_size(mk_int(self.train_architecture_size.currentText()))
                self.m_train.relative_size = self.train_relative_size.currentText()
                self.m_train.train_steps = mk_int(self.train_steps.text())
                self.m_train.validation_percentage = mk_float(self.train_validation_percentage.text())
                self.m_train.testing_percentage = mk_float(self.train_testing_percentage.text())
                self.m_train.random_brightness = mk_float(self.train_random_brightness.text())
                self.m_train.random_scale = mk_float(self.train_random_scale.text())
                self.m_train.random_crop = mk_float(self.train_random_crop.text())
                tcc.dao.update_object(self.m_train)
                self.refresh_list_trains()
                self.information_message('Train configuration updated sucessfully!')
        else:
            self.information_message('Please input a non blank text in name.')

    def delete_train(self):
        if self.m_train is not None:
            ec.dao.delete_object(self.m_train)
            self.information_message('Train deleted sucessfully!')
            self.refresh_list_trains()
            self.refresh_list_trains_2()
        else:
            self.information_message('None item selected!')

    def train_fill_architectures(self):
        self.train_architecture.addItems(TrainConfiguration.get_architecture_names())
        self.train_architecture_2.addItems(TrainConfiguration.get_architecture_names())

    def train_fill_architecture_size(self):
        self.train_architecture_size.addItems(TrainConfiguration.get_architecture_sizes())
        self.train_architecture_size_2.addItems(TrainConfiguration.get_architecture_sizes())

    def train_fill_relative_size(self):
        self.train_relative_size.addItems(TrainConfiguration.get_architecture_relative_sizes())
        self.train_relative_size_2.addItems(TrainConfiguration.get_architecture_relative_sizes())

    def execute_train(self):
        self.splashMessage('Training {}, please wait ...'.format(self.m_train.name))
        train_exec = tti.invoke_trainer(self.m_experiment, self.m_train)
        self.clearSplash()
        self.information_message('Train concluded. Result generated')
        self.refresh_list_trains_2()
        self.refresh_combos_control_train()
        # results[image_size] = train_exec.test_accuracy.item()
        self.clear_status_message()

    # ======================= SUSPECTS CONTROL =============================
    def refresh_list_control(self):
        linha = 0
        self.control_list.clearContents()
        pfr_history = self.session.query(PersonFaceRecords)\
            .filter(PersonFaceRecords.experiment == self.m_experiment) \
            .filter(and_(PersonFaceRecords.person_id == Person.id, Person.is_suspect)) \
            .order_by(PersonFaceRecords.date_time.desc())


        total = pfr_history.count()
        self.control_list.setRowCount(total)
        for pfr in pfr_history.all():
            self.refresh_list_control_item(pfr, linha)
            linha += 1

    def refresh_list_control_item(self, pfr, linha):
        time_str = pfr.date_time.strftime('%y/%m/%d %H:%M:%S')
        item = QTableWidgetItem(time_str)
        self.control_list.setItem(linha, 0, item)
        localization = pfrc.get_person_localization(pfr.person)
        item = QTableWidgetItem(localization)
        self.control_list.setItem(linha, 1, item)
        susp_str = pfr.suspect_name
        item = QTableWidgetItem(susp_str)
        self.control_list.setItem(linha, 2, item)
        if pfr.suspect_confidence is not None:
            confidence = mk_str_2(pfr.suspect_confidence * 100) + '%'
        else:
            confidence = '?'
        item = QTableWidgetItem(confidence)
        self.control_list.setItem(linha, 3, item)
        item = QTableWidgetItem(pfr.person.name)
        self.control_list.setItem(linha, 4, item)
        item = QTableWidgetItem(str(pfr.id))
        self.control_list.setItem(linha, 5, item)

    def refresh_combo_control_cameras(self):
        self.control_camera_1.clear()
        self.control_camera_2.clear()
        entrance_cams = [cam.name for cam in self.session.query(Camera).filter(Camera.experiment == self.m_experiment,
                                                                               Camera.type == TYPE_ENTRANCE)]
        exit_cams = [cam.name for cam in self.session.query(Camera).filter(Camera.experiment == self.m_experiment,
                                                                           Camera.type == TYPE_EXIT)]
        self.control_camera_1.addItems(entrance_cams)
        self.control_camera_2.addItems(exit_cams)

    def refresh_combos_control_train(self):
        self.control_train_1.clear()
        self.control_train_2.clear()
        self.control_pfr_train.clear()
        results = [train.name for train in
                   self.session.query(TrainExecution).filter(TrainExecution.experiment == self.m_experiment)]
        self.control_train_1.addItems(results)
        self.control_train_2.addItems(results)
        self.control_pfr_train.addItems(results)

    def control_start_recognize(self, control_display_name, face_recognizer_name, control_camera, control_train,
                                control_face_opt, control_suspect, control_graphics):
        from src.gui.QGraphicsSceneFaceRecorder import QGraphicsSceneFaceRecorder
        from src.controller.face_recognition.face_recognizer.FaceRecognizer import FaceRecognizer

        control_display = getattr(self, control_display_name)
        if not control_display:
            face_recognizer = FaceRecognizer()
            setattr(self, face_recognizer_name, face_recognizer)
            camera = self.session.query(Camera).filter(
                and_(Camera.name == control_camera.currentText(), Camera.experiment_id == self.m_experiment.id))[
                0]
            train_exec = self.get_train_result_by_name(control_train.currentText(), self.m_experiment.id)
            pfrc.recognize_suspect_faces(train_exec, train_exec.experiment, face_recognizer, camera)

            if control_face_opt.isChecked():
                control_graphics_face = self.control_graphics_face
            else:
                control_graphics_face = None

            q_graphics = QGraphicsSceneFaceRecorder(control_graphics, face_recognizer,
                                                    control_suspect, control_graphics_face, self)
            setattr(self, control_display_name, q_graphics)
            control_display = getattr(self, control_display_name)
            # self.person_display.setFPS(1)
            control_display.setParent(self)
            if control_display.scene_face:
                control_display.scene_face.setParent(self)
            control_display.start()

    def get_train_result_by_name(self, train_result_name, experiment_id):
        train_exec = \
            self.session.query(TrainExecution).filter(
                and_(TrainExecution.name == train_result_name,
                     TrainExecution.experiment_id == experiment_id))[0]
        return train_exec

    def control_stop_recognize(self, control_display_name, face_recognizer_name):
        self.splashMessage('Recording faces, please wait ...')
        control_display = getattr(self, control_display_name)
        face_recognizer = getattr(self, face_recognizer_name)
        control_display.stop()
        face_recognizer.stop()
        face_recognizer.recognize()
        control_display.deleteLater()
        if control_display.scene_face:
            control_display.scene_face.deleteLater()
            control_display.scene_face = None
        setattr(self, control_display_name, None)
        self.refresh_list_persons()
        self.refresh_list_control()
        self.clearSplash()

    def control_display_face(self):
        import os
        if self.m_pfr is None or self.control_curr_face_num < 0:
            self.control_face_num_lbl.setText('---')
            self.control_face_filename_lbl.setText('---')
            self.control_graphicsView_picture.setScene(None)
        else:
            frs = self.m_pfr.face_records
            if frs is None:
                self.control_face_num_lbl.setText('---')
                self.control_face_filename_lbl.setText('---')
                self.control_graphicsView_picture.setScene(None)
            else:
                if self.control_curr_face_num < len(frs):
                    fr = frs[self.control_curr_face_num]
                    if os.path.isfile(fr.filepath()):
                        pix = QPixmap(fr.filepath())
                        scene = QGraphicsScene()
                        scene.addPixmap(pix)
                        self.control_graphicsView_picture.setScene(scene)
                        self.control_graphicsView_picture.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
                        self.control_face_num_lbl.setText(str(self.control_curr_face_num))
                        self.control_face_filename_lbl.setText(fr.filepath())
                    # TODO using in dev
                    # else:
                    #     self.person_delete_face()

    def control_display_face_first(self):
        self.control_curr_face_num = 0
        self.control_display_face()

    def control_display_face_prev(self):
        if self.control_curr_face_num > 0:
            self.control_curr_face_num -= 1
            self.control_display_face()

    def control_display_face_next(self):
        last_idx = len(self.m_pfr.face_records) - 1
        if self.control_curr_face_num < last_idx:
            self.control_curr_face_num += 1
            self.control_display_face()

    def control_display_face_last(self):
        if self.m_pfr is None or self.control_curr_face_num < 0:
            self.control_face_num_lbl.setText('---')
            self.control_face_filename_lbl.setText('---')
            self.control_graphicsView_picture.setScene(None)
        else:
            self.control_curr_face_num = len(self.m_pfr.face_records) - 1
            self.control_display_face()

    def refresh_control_from_selected(self):
        curr_row = self.control_list.currentRow()
        item = self.control_list.item(curr_row, 5)
        if item is not None:
            id_pfr = mk_int(item.text())
            self.m_pfr = self.session.query(PersonFaceRecords).filter(
                and_(PersonFaceRecords.id == id_pfr, PersonFaceRecords.experiment_id == self.m_experiment.id))[0]
            if len(self.m_pfr.face_records) > 0:
                self.control_curr_face_num = 0
            else:
                self.control_curr_face_num = -1
        else:
            self.m_pfr = None
            self.control_curr_face_num = -1
        self.control_display_face_last()

    def control_delete_face(self):
        faces = self.m_pfr.face_records
        if len(faces) > 0:
            if self.control_curr_face_num > 0:
                pfrc.delete_face_record(faces[self.control_curr_face_num])
                self.control_curr_face_num -= 1
            elif self.control_curr_face_num == 0:
                pfrc.delete_face_record(faces[self.control_curr_face_num])

        faces = pfrc.get_person_faces(self.m_person)
        if len(faces) == 0:
            self.control_curr_face_num = -1
        self.control_display_face()

    def control_pfr_recog_all_clicked(self):

        mssg = 'Recognizing faces again, please wait ...'
        self.queue_recog_num_of_recogs = 0
        self.queue_recog_total_time = 0
        self.splashMessage(mssg)
        self.status_message(mssg)
        train_result = self.get_train_result_by_name(self.control_pfr_train.currentText(), self.m_experiment.id)
        train_pars = tti.create_test_params(train_result)
        pfr_suspects_history = self.session.query(PersonFaceRecords) \
            .filter(PersonFaceRecords.experiment == self.m_experiment) \
            .filter(and_(PersonFaceRecords.person_id == Person.id, Person.is_suspect)) \
            .order_by(PersonFaceRecords.date_time.desc())

        for pfr in pfr_suspects_history:
            frs = pfr.face_records
            if len(frs) > 0: # and pfr.id in [752]:
                # 750, 749, 748, 747, 746, 745, 744, 743, 742, 741, 740, 739, 738, 737, 736, 735, 734, 733, 732, 731, 730,
                # 729, 728, 727, 726, 725, 724, 723, 722, 721, 720, 719, 718, 717, 716, 715, 714, 713, 712, 711, 710,
                # 707, 706, 844, 845, 843]):
                self.consume_recog_queue(train_pars, frs)
        self.refresh_list_control()
        print('Recogs total time = ', self.queue_recog_total_time)
        print('Recogs # = ', self.queue_recog_num_of_recogs)
        print('Recogs avg time = ', self.queue_recog_total_time / self.queue_recog_num_of_recogs)

        self.status_message('Suspects recognition recalculated successfully!')
        self.clearSplash()

    def consume_recog_queue(self, train_pars, frs):
        recognizer_method = 'median_sum_accuracy'
        label_results_accum = {}
        label_results_count = {}
        for fr in frs:
            labels_results, time_exec = tti.invoke_test_file(train_pars, fr.filepath())
            self.queue_recog_num_of_recogs += 1
            self.queue_recog_total_time += time_exec
            # TODO create method for the code above and FaceRecognizer
            for person, result in labels_results.items():
                if person in label_results_accum.keys():
                    label_results_accum[person] = label_results_accum[person] + result
                    label_results_count[person] += 1
                else:
                    label_results_accum[person] = result
                    label_results_count[person] = 1
        pfr = frs[0].person_face_records
        pfrc.calculate_median_accuracy(recognizer_method, label_results_accum, pfr)

    # def control_pfr_recog_all_clicked(self):
    #     import threading
    #     import queue
    #
    #     self.control_pfr
    #
    #     mssg = 'Recognizing faces again, please wait ...'
    #     self.queue_recog_num_of_recogs = 0
    #     self.queue_recog_total_time = 0
    #     self.splashMessage(mssg)
    #     self.status_message(mssg)
    #     train_result = self.get_train_result_by_name(self.control_pfr_train.currentText(), self.m_experiment.id)
    #     train_pars = tti.create_test_params(train_result)
    #     pfr_suspects_history = self.session.query(PersonFaceRecords) \
    #         .filter(PersonFaceRecords.experiment == self.m_experiment) \
    #         .filter(and_(PersonFaceRecords.person_id == Person.id, Person.is_suspect)) \
    #         .order_by(PersonFaceRecords.date_time.desc())
    #     self.queue_recog = queue.Queue()
    #     threads_recognize = []
    #     max_threads = 1
    #     for i in range(max_threads):
    #         t = threading.Thread(target=self.consume_recog_queue, args=[train_pars])
    #         t.start()
    #         threads_recognize.append(t)
    #
    #     for pfr in pfr_suspects_history:
    #         frs = pfr.face_records
    #         if len(frs) > 0:
    #             self.queue_recog.put(pfr.face_records)
    #     self.queue_recog.join()
    #     # stop workers
    #     for i in range(max_threads):
    #         self.queue_recog.put(None)
    #     for t in threads_recognize:
    #         t.join()
    #     self.refresh_list_control()
    #     print('Recogs total time = ', self.queue_recog_total_time)
    #     print('Recogs # = ', self.queue_recog_num_of_recogs)
    #     print('Recogs avg time = ', self.queue_recog_total_time / self.queue_recog_num_of_recogs)
    #
    #     self.status_message('Suspects recognition recalculated successfully!')
    #     self.clearSplash()
    #
    # def consume_recog_queue(self, train_pars):
    #     recognizer_method = 'median_sum_accuracy'
    #     while True:
    #         frs = self.queue_recog.get()
    #         if frs is None:
    #             # self.queue_recog.task_done()
    #             break
    #         label_results_accum = {}
    #         label_results_count = {}
    #         for fr in frs:
    #             labels_results, time_exec = tti.invoke_test_file(train_pars, fr.filepath())
    #             self.queue_recog_num_of_recogs += 1
    #             self.queue_recog_total_time += time_exec
    #             # TODO create method for the code above and FaceRecognizer
    #             for person, result in labels_results.items():
    #                 if person in label_results_accum.keys():
    #                     label_results_accum[person] = label_results_accum[person] + result
    #                     label_results_count[person] += 1
    #                 else:
    #                     label_results_accum[person] = result
    #                     label_results_count[person] = 1
    #         pfr = frs[0].person_face_records
    #         pfrc.calculate_median_accuracy(recognizer_method, label_results_accum, pfr)
    #         self.queue_recog.task_done()


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication

    form = TensorFaceController()  # We set the form to be our ExampleApp (design)
    # debug = DebugUtils.get_instance(0, "/dados/tmp.txt")
    # debug.flush_file()
    # debug.close_file()
    form.show()  # Show the form
    sys.exit(app.exec_())


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()
