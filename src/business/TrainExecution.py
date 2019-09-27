from sqlalchemy import String, Integer, Float, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_dao import Model


class TrainExecution(Model):

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    experiment_id = Column(Integer, ForeignKey('experiment.id', ondelete='CASCADE'))
    experiment = relationship('Experiment')
    UniqueConstraint('name', 'experiment', name='uniq_name_exp')
    train_configuration_id = Column(Integer, ForeignKey('train_configuration.id', ondelete='CASCADE'))
    train_configuration = relationship('TrainConfiguration')

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

    sub_case_dir = Column(String(1024))
    model_dir = Column(String(1024))
    summaries_dir = Column(String(1024))
    bottlenecks_dir = Column(String(1024))
    model_file = Column(String(1024))
    label_file = Column(String(1024))
    train_dir = Column(String(1024))
    test_dir = Column(String(1024))
    test_accuracy = Column(Float())
