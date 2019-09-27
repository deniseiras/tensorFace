from src.business.FaceRecord import FaceRecord

from src.dao.GenericDao import GenericDao


class FaceRecordDao(GenericDao):

    @classmethod
    def create_face_record(cls, filename):
        face_rec = FaceRecord(filename=filename)
        cls.update_object(face_rec)
        return face_rec

