# from examples.performance import Profiler
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# from sqlalchemy_dao.model import create_model_base
# from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import OperationalError
from sqlalchemy_dao import Model
from sqlalchemy_dao import Dao, POOL_DISABLED
from src.debug.debugutils import DebugUtils
from sqlalchemy.sql import text
debug = DebugUtils.get_instance()


class DatabaseController:

    instance = None

    def __init__(self):
        self.is_test_db = None
        self.db_url = None
        self.db_name = None
        self.dao = None
        self.session = None
        # for use with pure sqlalchemy
        # self.engine = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = DatabaseController()
        return cls.instance

    def disconnect(self):
        self.session.close()
        self.dao = None

    def connect(self, db_url, is_test_db=False, use_db=None):
        self.is_test_db = is_test_db
        if self.is_test_db:
            self.db_url = 'sqlite://'
        else:
            if use_db:
                self.db_url = db_url + '/' + use_db
            else:
                self.db_url = db_url

        self.create_dao()
        self.use_database(use_db)

    def use_database(self, use_db):
        if use_db is not None:
            statement = text("""use {};""".format(use_db))
            self.get_session().execute(statement)
            self.db_name = use_db

    def create_dao(self):
        # if self.dao is None:
        if self.is_test_db:
            self.dao = Dao(self.db_url, pool_size=POOL_DISABLED)
        else:
            self.dao = Dao(self.db_url)

    def reconnect(self):
        dbc = DatabaseController.get_instance()
        dbc.disconnect()
        self.create_dao()
        self.use_database(self.db_name)


    def create_database(self, db_name):
        if not self.is_test_db:
            session = self.get_session()
            statement = text("""create database {};""".format(db_name))
            session.execute(statement)
            statement = text("""ALTER DATABASE {} CHARACTER SET utf8;""".format(db_name))
            session.execute(statement)

    def create_tables(self):
        # guarantees all tables are defined before create them.
        # the order matters
        from src.business.Person import Person
        from src.business.FaceRecord import FaceRecord
        from src.business.PersonFaceRecords import PersonFaceRecords
        from src.business.Camera import Camera
        from src.business.TensorFlowEnv import TensorFlowEnv
        from src.business.Experiment import Experiment
        from src.business.TrainConfiguration import TrainConfiguration
        from src.business.TestConfiguration import TestConfiguration
        from src.business.TrainExecution import TrainExecution
        # Model.metadata.create_all(self.engine)
        # TODO Is there better method to create all?
        Model.metadata.create_all(self.dao._engine)

    def drop_database(self, db_name):
        from sqlalchemy.sql import text
        # memory db doesnt need to drop
        if not self.is_test_db:
            statement = text("""drop database {};""".format(db_name))
            try:
                self.get_session().execute(statement)
            except OperationalError as e:
                debug.msg('{} ... continuing'.format(str(e)))
                pass

    def get_session(self):
        if self.session is None:
            # session actually created with dao creation
            self.session = self.dao.create_session()
            # self.session.connection()
        return self.session

    # def get_session(self):
    #     if self.session is None:
    #         self.session = Session(self.engine)
    #         # pre-connect so this part isn't profiled (if we choose)
    #         self.session.connection()
    #     return self.session
