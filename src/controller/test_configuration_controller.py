from src.dao.TestConfigurationDao import TestConfigurationDao

dao = TestConfigurationDao


def create_test_configuration(name, exp, face_records_dir, train_exec):
    face_records_dir = exp.tests_dir() + face_records_dir
    return dao.create_test_configuration(name, exp, face_records_dir, train_exec)
