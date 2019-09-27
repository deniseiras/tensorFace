from src.business.TrainConfiguration import TrainConfiguration
from src.dao.database.DatabaseController import DatabaseController
from src.dao.GenericDao import GenericDao


class TrainConfigurationDao(GenericDao):

    @classmethod
    def create_train_configuration(cls, steps, image_size, name=None):
        train = TrainConfiguration()
        train.name = name
        train.make_default_values()
        cls.update_object(train, {'train_steps': steps, 'input_height': image_size, 'input_width': image_size})
        return train
