from src.dao.database.DatabaseController import DatabaseController
from unittest.case import TestCase

class TestCaseWithDatabase(TestCase):

    db_url = 'mysql://root:sk8ordie@localhost:3306'

    def setUp(self):
        super().setUp()
        dbc = DatabaseController.get_instance()
        self.db_num = 1
        while True:
            try:
                self.db_name = 'TEST{}'.format(self.db_num)
                dbc.connect(self.db_url, use_db=self.db_name)
                self.db_num += 1
            except Exception as e:
                break

        dbc.disconnect()
        try:
            dbc.connect(self.db_url)
            dbc.create_database(self.db_name)
            dbc.disconnect()
            dbc.connect(self.db_url, use_db=self.db_name)
            dbc.create_tables()
        except Exception as e:
            pass

    # def setUp(self):
    #     super().setUp()
    #
    #     dbc = DatabaseController.get_instance()
    #     dbc.connect(self.db_url)
    #     try:
    #         dbc.drop_database(self.db_name)
    #     except Exception as e:
    #         pass
    #     dbc.create_database(self.db_name)
    #     dbc.disconnect()
    #     dbc.connect(self.db_url, use_db=self.db_name)
    #     dbc.create_tables()

    def reconnect(self):
        dbc = DatabaseController.get_instance()
        dbc.reconnect()

    def tearDown(self):
        super().tearDown()
        dbc = DatabaseController.get_instance()
        dbc.connect(self.db_url)
        dbc.drop_database(self.db_name)
        dbc.disconnect()

    def drop_all_databases(self):
        dbc = DatabaseController.get_instance()
        self.db_num = 1
        for self.db_num in range(1000):
            self.db_name = 'TEST{}'.format(self.db_num)
            dbc.connect(self.db_url)
            dbc.drop_database(self.db_name)
            dbc.disconnect()
            self.db_num += 1

# if __name__ == '__main__':
#     t = TestCaseWithDatabase()
#     t.drop_all_databases()