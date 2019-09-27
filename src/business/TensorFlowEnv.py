from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from sqlalchemy_dao import Model


class TensorFlowEnv(Model):

    id = Column(Integer, primary_key=True)
    root_dir = Column(String(1024), unique=True)
    tf_files_dir = Column(String(1024))
    summaries_dir = Column(String(1024))
    model_dir = Column(String(1024))
    experiment = relationship('Experiment')

    def make_default_values(self):
        self.tf_files_dir = self.root_dir + 'experiments/'
        self.summaries_dir = self.root_dir + 'training_summaries/'
        self.model_dir = self.root_dir + 'models/'
