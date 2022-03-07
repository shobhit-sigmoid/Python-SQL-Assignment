import psycopg2
import logging
from sqlalchemy import create_engine

class create_connection:
    def get_connection(self, database, user, password, host, port):
        try:
            connection = psycopg2.connect(database=database, user=user, password=password,
                                          host=host, port=port)
            return connection
        except:
            logging.error("Connection Error")
            raise Exception("Connection cannot be established")
        finally:
            logging.info("Connection successfully established")

    def get_engine(self, user, password, host, port, database):
        if user != "shobhitchaurasiya":
            raise Exception("Error in engine creation")
        else:
            try:
                engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
                return engine
            except:
                logging.error("Error in engine creation")
            finally:
                logging.info("Engine successfully created")
