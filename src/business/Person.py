from sqlalchemy import String, Integer, Boolean, Float, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_dao import Model


class Person(Model):

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    nick = Column(String(100))
    is_suspect = Column(Boolean)
    experiment_id = Column(Integer, ForeignKey('experiment.id', ondelete='CASCADE'))
    experiment = relationship('Experiment', back_populates='persons')
    UniqueConstraint('name', 'experiment', name='uniq_name_exp')
    UniqueConstraint('nick', 'experiment', name='uniq_nick_exp')
    person_face_records = relationship('PersonFaceRecords', back_populates='person')
    face_records = relationship("FaceRecord")
    threshold = Column(Float)

    def person_db_dir(self):
        face_db_base_dir = self.experiment.face_records_dir()
        return '{}{}'.format(face_db_base_dir, self.nick)

    def add_face_record(self, face_record):
        self.face_records.append(face_record)

    def remove_face_record(self, face_record):
        self.face_records.remove(face_record)

    def add_person_face_records(self, pfr):
        self.person_face_records.append(pfr)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()




