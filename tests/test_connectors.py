import pytest
from pigging.connectors import googleBigQueryConnector, googleSheetsConnector
import os
import warnings
import pandas as pd

### Credentials ###
CREDENTIALS_PATH = os.environ.get('CREDENTIALS_PATH')


### Google Big Query ###
SELECT_QUERY = os.environ.get('SELECT_QUERY')
PROEJCT_ID = os.environ.get('PROEJCT_ID')
TABLE_DESTINATION = os.environ.get('TABLE_DESTINATION')
gbq_connector = googleBigQueryConnector(CREDENTIALS_PATH)


class TestGoogleBigQueryConnector(object):
    def test_connected(self, capsys):
        gbq_connector = googleBigQueryConnector(CREDENTIALS_PATH)
        captured = capsys.readouterr()
        assert captured.out == "Successfully loaded Google BigQuery credentials\n"

    def test_data_import_successfull(self):
        df = gbq_connector.import_data(SELECT_QUERY, PROEJCT_ID)
        assert len(df) > 0, "There should be a df"

    def test_data_export_successful(self, capsys):
        df = gbq_connector.import_data(SELECT_QUERY, PROEJCT_ID)
        gbq_connector.export_data(
            df, TABLE_DESTINATION, PROEJCT_ID, "EU", 'replace')
        captured = capsys.readouterr()
        assert captured.out == "Successfully exported data to Google BigQuery\n"


### Google Sheets ###
WORKSHEET_ID = os.environ.get('WORKSHEET_ID')
WORKSHEET_NAME = os.environ.get('WORKSHEET_NAME')
DF = pd.DataFrame(["test value"], columns=['Test col'])
gs_connector = googleSheetsConnector(CREDENTIALS_PATH)


class TestGoogleSheetsConnector(object):
    def test_connected(self, capsys):
        gs_connector = googleSheetsConnector(CREDENTIALS_PATH)
        captured = capsys.readouterr()
        assert captured.out == "Successfully started Google Sheets client\n"

    def test_data_export_successful(self, capsys):
        gs_connector.export_data(DF, WORKSHEET_ID, WORKSHEET_NAME)
        captured = capsys.readouterr()
        assert captured.out == "Successfully exported data to Google Sheets\n"
