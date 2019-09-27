from src.business.PersonFaceRecords import PersonFaceRecords
from src.business.Person import Person
from src.dao.database.DatabaseController import DatabaseController
from datetime import datetime

from src.dao.GenericDao import GenericDao


class PersonFaceRecordsDao(GenericDao):

    @classmethod
    def create_person_face_records(cls, experiment, name, camera, is_suspect=False, person=None):
        if person is None:
            p1 = Person(name=name)
        else:
            p1 = person
        p1.is_suspect = is_suspect
        p1.experiment = experiment
        # if is_suspect:
        pfr = PersonFaceRecords(person=p1, suspect_name=name, camera=camera, experiment=experiment, date_time=datetime.now())
        # pfr.date_time = datetime.now()
        p1.add_person_face_records(pfr)
        cls.update_object(pfr)

        return pfr


    @classmethod
    def create_person(cls, name, experiment):
        p1 = Person(name=name)
        p1.experiment = experiment
        p1.is_suspect = False
        return p1

    @classmethod
    def delete_person(cls, person):
        for pfr in person.person_face_records:
            cls.delete_person_face_records(pfr)
        for face in person.face_records:
            cls.delete_object(face, commit=False)
        cls.delete_object(person)

    @classmethod
    def delete_person_face_records(cls, pfr):
        if pfr is not None:
            for face in pfr.face_records:
                cls.delete_object(face, commit=False)
            cls.delete_object(pfr, commit=False)
            cls.commit()
