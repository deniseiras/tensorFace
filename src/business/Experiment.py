from sqlalchemy import Integer, Float, String, Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_dao import Model


class Experiment(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    tf_env_id = Column(Integer, ForeignKey('tensor_flow_env.id'))
    tf_env = relationship('TensorFlowEnv', uselist=False)
    # exp_root_dir = Column(String(1024))
    # face_records_dir = Column(String(1024))
    # log_dir = Column(String(1024))
    # trains_dir = Column(String(1024))
    # tests_dir = Column(String(1024))
    # suspect_dir = Column(String(1024))
    face_width = Column(Float())
    # person_face_records = relationship('PersonFaceRecords')
    cameras = relationship('Camera')
    persons = relationship('Person')
    person_face_records = relationship('PersonFaceRecords')

    def exp_root_dir(self):
        return self.tf_env.tf_files_dir + self.name + '/'

    def face_records_dir(self):
        return self.exp_root_dir() + 'face_records/'

    def log_dir(self):
        return self.exp_root_dir() + 'log/'

    def trains_dir(self):
        return self.exp_root_dir() + 'trains/'

    def tests_dir(self):
        return self.exp_root_dir() + 'to_test/'

    def suspect_dir(self):
        return self.exp_root_dir() + 'suspects/'

    def make_default_values(self):
        # TODO move to common environment
        self.face_width = 160.0
