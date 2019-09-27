from src.dao.database.DatabaseController import DatabaseController
from src.controller import experiment_controller


# initialize database for real
def create_alfa_database():
    db_name = 'ALFA'
    db_url = 'mysql://root:sk8ordie@localhost:3306'
    dbc = DatabaseController.get_instance()
    dbc.connect(db_url)
    dbc.drop_database(db_name)
    dbc.create_database(db_name)
    dbc.disconnect()
    dbc.connect(db_url, use_db=db_name)
    dbc.create_tables()

    experiment_controller.create_tf_env('/dados/dev/tensorface_data_ALFA/')

    dbc.disconnect()


if __name__ == '__main__':  # if we're running file directly and not importing it
    create_alfa_database()
