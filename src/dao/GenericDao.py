from src.dao.database.DatabaseController import DatabaseController


class GenericDao:

    @staticmethod
    def session():
        return DatabaseController.get_instance().get_session()

    @staticmethod
    def add_to_session(model_obj):
        GenericDao.session().add(model_obj)

    @staticmethod
    def commit():
        GenericDao.session().commit()

    @staticmethod
    def get_object_by_id(model_class, q_id):
        return GenericDao.session().query(model_class).get(q_id)

    @staticmethod
    def update_object(obj, dict=None, commit=True):
        session = GenericDao.session()
        if dict is not None:
            obj.update(dict)
        session.add(obj)
        if commit:
            session.commit()

    @staticmethod
    def delete_object(obj, commit=True):
        session = GenericDao.session()
        session.delete(obj)
        if commit:
            session.commit()
