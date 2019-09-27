from sqlalchemy import Integer, String, Boolean, Float, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_dao import Model

TYPE_ENTRANCE = 'Entrance'
TYPE_EXIT = 'Exit'
TYPE_AUXILIAR = 'Auxuliar'


class Camera(Model):
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey('experiment.id', ondelete='CASCADE'))
    experiment = relationship('Experiment', back_populates='cameras')
    name = Column(String(100))
    UniqueConstraint('name', 'experiment', name='uniq_name_exp')
    type = Column(String(10))
    # TODO history cam_str ?
    camera_string = Column(String(255))
    x_res = Column(Integer())
    y_res = Column(Integer())
    # in mm
    focal_distance = Column(Float())
    apperture_size = Column(Float())
    # mm
    sensor_size = Column(Float())
    # degrees
    horiz_angle = Column(Float())
    vert_angle = Column(Float())
    # in mm
    floor_height = Column(Float())
    capture_height = Column(Float())
    # extraction features
    back_sub_do = Column(Boolean())
    back_sub_roi_top_border = Column(Integer())
    back_sub_thresh_num = Column(Float())
    back_sub_roi_x_start = Column(Integer())
    back_sub_roi_x_res_reduction = Column(Integer())
    # TODO RENAME TO SECONDS
    reset_time_init_frame_millis = Column(Float())
    face_detection_do = Column(Boolean())
    face_border_increase_pct = Column(Float())
    # TODO
    face_capture_min_width_auto = Column(Boolean())
    face_capture_min_width_fixed = Column(Integer())
    face_capture_min_neighbors = Column(Integer())
    face_capture_scale_factor = Column(Float())

    face_capture_time_interval = Column(Float())
    recog_threads = Column(Integer())
    recog_save_timeout = Column(Float())
    recog_real_time = Column(Boolean())

    def make_default_values(self):
        self.type = TYPE_ENTRANCE
        self.camera_string = '0'
        self.x_res = 0
        self.y_res = 0
        self.focal_distance = 0
        self.apperture_size = 0
        self.sensor_size = 0
        self.horiz_angle = 0
        self.vert_angle = 0
        self.floor_height = 2250
        self.capture_height = 2250
        self.back_sub_do = True
        self.reset_time_init_frame_millis = 1800000
        self.back_sub_roi_top_border = 20
        self.back_sub_thresh_num = 75
        self.back_sub_roi_x_start = 0
        self.back_sub_roi_x_res_reduction = 0
        self.face_detection_do = True
        self.face_border_increase_pct = 0.0
        # TODO calculate
        self.face_capture_min_width_auto = True
        self.face_capture_min_width_fixed = 40
        self.face_capture_min_neighbors = 5
        self.reset_time_init_frame_millis = 360
        self.face_capture_time_interval = 0.67
        self.recog_threads = 6
        self.face_capture_scale_factor = 1.1
        self.recog_save_timeout = 5
        self.recog_real_time = False
