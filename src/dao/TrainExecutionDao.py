from src.business.TrainExecution import TrainExecution
from src.dao.GenericDao import GenericDao
import datetime


class TrainExecutionDao(GenericDao):

    @classmethod
    def create_train_execution(cls, exp, train_cfg, commit=True):
        train = TrainExecution()
        datenow = datetime.datetime.now().strftime('%y/%m/%d %H:%M:%S')
        cls.update_object(train, {'experiment_id': exp.id,
                                  'train_configuration_id': train_cfg.id,
                                  'name': '{} - {}'.format(train_cfg.name, datenow),
                                  'train_steps': train_cfg.train_steps,
                                  'arch_name': train_cfg.arch_name,
                                  'input_height': train_cfg.input_height,
                                  'input_width': train_cfg.input_width,
                                  'input_mean': train_cfg.input_mean,
                                  'input_std': train_cfg.input_std,
                                  'relative_size': train_cfg.relative_size,
                                  'validation_percentage': train_cfg.validation_percentage,
                                  'testing_percentage': train_cfg.testing_percentage,
                                  'random_brightness': train_cfg.random_brightness,
                                  'random_scale': train_cfg.random_scale,
                                  'random_crop': train_cfg.random_crop}, commit=commit)
        return train
