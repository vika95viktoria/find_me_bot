import os
import pg8000
import sqlalchemy
from google.cloud.sql.connector import Connector


class DbConnector:
    def __init__(self):
        self.db_user = os.environ.get("DB_USER", "")
        self.instance_connection_name = os.environ['INSTANCE_CONNECTION_NAME']
        self.db_pass = os.environ["DB_PASS"]
        self.db_name = os.environ["DB_NAME"]
        self.connector = Connector()

    def get_engine(self) -> sqlalchemy.engine.base.Engine:
        """
        Initializes a connection pool for a Cloud SQL instance of SQL Server.
        Uses the Cloud SQL Python Connector package.
        """

        def get_connection() -> pg8000.Connection:
            return self.connector.connect(
                self.instance_connection_name,
                "pg8000",
                user=self.db_user,
                password=self.db_pass,
                db=self.db_name,
                enable_iam_auth=True
            )

        return sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=get_connection
        )
