from src.business.TestConfiguration import TestConfiguration
from src.dao.database.DatabaseController import DatabaseController
from src.dao.GenericDao import GenericDao


class TestConfigurationDao(GenericDao):

    @classmethod
    def create_test_configuration(cls, name, exp, face_records_dir, train_exec):
        test_cfg = TestConfiguration()
        test_cfg.name = name
        test_cfg.experiment = exp
        test_cfg.face_records_dir = face_records_dir
        test_cfg.train_exec = train_exec
        cls.update_object(test_cfg)
        return test_cfg
