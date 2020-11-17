import pandas as pd
from retry import retry
from google.oauth2 import service_account


class exportConnectors(object):
    def __init__(self, google_big_query_credentials=None):
        if google_big_query_credentials is not None:
            self.google_big_query_credentials = (
                service_account.Credentials.from_service_account_file(
                    google_big_query_credentials
                )
            )
            print("Successfully connected to Google BigQuery export module")

    @retry(tries=3, delay=3)
    def google_big_query(self, dataframe, table_destination, project_id, if_exists):
        dataframe.to_gbq(
            destination_table=table_destination,
            project_id=project_id,
            if_exists=if_exists,
            credentials=self.google_big_query_credentials,
        )
        print("Pushed dataframe to Google BigQuery")
