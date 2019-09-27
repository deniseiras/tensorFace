from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_dao import Model


class FaceRecord(Model):

    id = Column(Integer, primary_key=True)
    filename = Column(String(1024))
    person_id = Column(Integer, ForeignKey('person.id', ondelete='CASCADE'))
    person = relationship('Person', back_populates='face_records')
    person_face_records_id = Column(Integer, ForeignKey('person_face_records.id', ondelete='CASCADE'))
    person_face_records = relationship('PersonFaceRecords') # , back_populates='face_records')

    def filepath(self):
        if self.person is None:
            return '{}/{}'.format(self.person_face_records.suspect_db_dir(), self.filename)
        else:
            return '{}/{}'.format(self.person.person_db_dir(), self.filename)
