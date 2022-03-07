import pytest
from connection import create_connection


class TestEmployee:
    @classmethod
    def setup_class(cls):
        print("\nSetting Up Class")

    @classmethod
    def teardown_class(cls):
        print("\nTearing Down Class")

    @pytest.fixture
    def setup(self):
        obj = create_connection()
        return obj

    def test_db_connection(self, setup):
        with pytest.raises(Exception):
            setup.get_connection(database="postgres", user="shobhit", password="none",
                                 host="localhost", port=5432)

    def test_engine(self, setup):
        with pytest.raises(Exception):
            setup.get_engine(user="unknown", password="none", host="localhost",
                             port=5432, database="postgres")
