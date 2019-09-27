from src.dao.TrainExecutionDao import TrainExecutionDao
from src.business.TrainExecution import TrainExecution
dao = TrainExecutionDao


def create_train_execution(exp, train_cfg, commit=None):
    return dao.create_train_execution(exp, train_cfg, commit)


def get_object_by_id(q_id):
    return dao.get_object_by_id(TrainExecution, q_id)