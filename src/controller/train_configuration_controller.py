from src.dao.TrainConfigurationDao import TrainConfigurationDao
from src.business.TrainConfiguration import TrainConfiguration
dao = TrainConfigurationDao


def get_object_by_id(q_id):
    return dao.get_object_by_id(TrainConfiguration, q_id)


def create_train_configuration(steps, image_size, name=None):
    return dao.create_train_configuration(steps, image_size, name)


def set_image_size(train, image_size):
    dao.update_object(train, {'input_height': image_size, 'input_width': image_size})


def set_relative_size(train, relative_size):
    dao.update_object(train, {'relative_size': relative_size})