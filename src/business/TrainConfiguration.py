from sqlalchemy import String, Integer, Float, Column
from sqlalchemy_dao import Model


class TrainConfiguration(Model):

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    train_steps = Column(Integer())
    arch_name = Column(String(100))
    input_height = Column(Integer())
    input_width = Column(Integer())
    input_mean = Column(Integer())
    input_std = Column(Integer())
    relative_size = Column(String(4))
    validation_percentage = Column(Float())
    testing_percentage = Column(Float())
    random_brightness = Column(Float())
    random_scale = Column(Float())
    random_crop = Column(Float())

    def make_default_values(self):
        self.train_steps = 20
        self.arch_name = 'mobilenet'
        self.input_height = 128
        self.input_width = 128
        self.input_mean = 128  # 128 default
        self.input_std = 128  # 128 default
        self.relative_size = '1.0'
        self.validation_percentage = 10  # 10 default
        self.testing_percentage = 10  # 10 default
        self.random_brightness = 0  # 0 default
        self.random_scale = 0  # 0 default
        self.random_crop = 0  # 0 default

    def get_architecture(self):
        return "{}_{}_{}".format(self.arch_name, self.relative_size, self.input_width)

    def set_size(self, size):
        self.input_height = size
        self.input_width = size

    @classmethod
    def get_architecture_names(cls):
        return ['mobilenet', 'incepton']

    @classmethod
    def get_architecture_sizes(cls):
        return ['128', '160', '192', '224']

    @classmethod
    def get_architecture_relative_sizes(cls):
        return ['0.25', '0.50', '0.75', '1.0']