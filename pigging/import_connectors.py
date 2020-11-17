import pandas as pd
from retry import retry
from google.oauth2 import service_account


class importConnectors(object):
    def __init__(self, google_big_query_credentials=None):
        if google_big_query_credentials is not None:
            self.google_big_query_credentials = (
                service_account.Credentials.from_service_account_file(
                    google_big_query_credentials
                )
            )
            print("Successfully connected to Google BigQuery import module")

    @retry(tries=3, delay=3)
    def google_big_query(self, query, project_id):
        return pd.read_gbq(
            query=query,
            project_id=project_id,
            credentials=self.google_big_query_credentials,
        )
