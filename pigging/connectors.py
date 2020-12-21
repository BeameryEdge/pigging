import pandas as pd
from retry import retry
from google.oauth2 import service_account
import gspread
import gspread_dataframe as gd


class googleBigQueryConnector(object):
    def __init__(self, google_big_query_credentials, retry_tries=3, retry_delay=3):
        self.retry_tries = retry_tries
        self.retry_delay = retry_delay
        self.google_big_query_credentials = (
            service_account.Credentials.from_service_account_file(
                google_big_query_credentials
            )
        )
        print("Successfully loaded Google BigQuery credentials")

    def import_data(self, query, project_id):
        @retry(tries=self.retry_tries, delay=self.retry_delay)
        def import_gcp_data(query, project_id):
            return pd.read_gbq(
                query=query,
                project_id=project_id,
                credentials=self.google_big_query_credentials,
            )
        return(import_gcp_data(query, project_id))

    def export_data(self, dataframe, table_destination, project_id, location, if_exists):
        @retry(tries=self.retry_tries, delay=self.retry_delay)
        def export_gcp_data(dataframe, table_destination, project_id, location, if_exists):
            dataframe.to_gbq(
                destination_table=table_destination,
                project_id=project_id,
                if_exists=if_exists,
                location=location,
                credentials=self.google_big_query_credentials,
            )

        export_gcp_data(dataframe, table_destination,
                        project_id, location, if_exists)
        print("Successfully exported data to Google BigQuery")


class googleSheetsConnector(object):
    def __init__(self, google_sheets_credentials, retry_tries=3, retry_delay=3):
        self.retry_tries = retry_tries
        self.retry_delay = retry_delay

        self.service_account_loaded = (
            service_account.Credentials.from_service_account_file(
                google_sheets_credentials
            )
        )
        print("Successfully started Google Sheets client")

    def export_data(self, dataframe, worksheet_id, worksheet_name):

        client = gspread.authorize(self.service_account_loaded.with_scopes(["https://spreadsheets.google.com/feeds",
                                                                            "https://www.googleapis.com/auth/drive"]))

        @retry(tries=self.retry_tries, delay=self.retry_delay)
        def export_gs_data(df, wid, wname):
            ws_1 = client.open_by_key(wid).worksheet(wname)
            gd.set_with_dataframe(worksheet=ws_1, dataframe=df, resize=True)

        export_gs_data(dataframe, worksheet_id, worksheet_name)
        print("Successfully exported data to Google Sheets")
