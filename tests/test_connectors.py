import pytest
from pigging.connectors import googleBigQueryConnector
import os
import warnings

CREDENTIALS_PATH = os.environ.get('CREDENTIALS_PATH')
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
        gbq_connector.export_data(df, TABLE_DESTINATION, PROEJCT_ID, 'replace')
        captured = capsys.readouterr()
        assert captured.out == "Successfully exported data to Google BigQuery\n"
