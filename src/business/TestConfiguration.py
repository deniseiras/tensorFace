from sqlalchemy import String, Integer, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_dao import Model


class TestConfiguration(Model):

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    experiment_id = Column(Integer, ForeignKey('experiment.id', ondelete='CASCADE'))
    experiment = relationship('Experiment')
    UniqueConstraint('name', 'experiment', name='uniq_name_exp')
    train_exec_id = Column(Integer, ForeignKey('train_execution.id'))
    train_exec = relationship('TrainExecution')
    face_records_dir = Column(String(255))
    person_face_records = relationship("PersonFaceRecords")

    def add_person_face_records(self, pfr):
        self.person_face_records.append(pfr)
