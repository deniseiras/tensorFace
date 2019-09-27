from sqlalchemy import String, Integer, DateTime, Boolean, Float, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_dao import Model


class PersonFaceRecords(Model):

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey('experiment.id', ondelete='CASCADE'))
    experiment = relationship('Experiment', back_populates='person_face_records')
    suspect_name = Column(String(100))
    suspect_confidence = Column(Float())
    date_time = Column(DateTime())
    test_configuration_id = Column(Integer, ForeignKey('test_configuration.id'))
    test_configuration = relationship('TestConfiguration', back_populates='person_face_records')
    # suspect_db_dir = Column(String(1024))
    person_id = Column(Integer, ForeignKey('person.id', ondelete='CASCADE'))
    person = relationship('Person', back_populates='person_face_records')
    camera_id = Column(Integer, ForeignKey('camera.id'))
    camera = relationship('Camera')
    face_records = relationship("FaceRecord")

    def add_face_record(self, face_record):
        self.face_records.append(face_record)

    def remove_face_record(self, face_record):
        self.face_records.remove(face_record)

    def is_suspect(self):
        return self.person.is_suspect

    def suspect_db_dir(self):
        suspect_base_dir = self.experiment.suspect_dir()
        return '{}{}'.format(suspect_base_dir, self.person.nick)

