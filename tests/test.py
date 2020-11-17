# %%
from pigging import Tracker, importConnectors, exportConnectors

# %%
tracker = Tracker(log_path="./test.log", lock_path="./test.lock")
tracker.startup()


import_conn = importConnectors("./gcp_credentials.json")
export_conn = exportConnectors("./gcp_credentials.json")
# %%

data = import_conn.google_big_query(
    "SELECT * FROM Salesforce.beamery_companies", "beamery-data"
)
data.head()
# %%

export_conn.google_big_query(
    data, "Salesforce.beamery_companies", "beamery-data", "replace"
)

# %%
tracker.log("hi", "INFO")
try:
    print("hello")
except Exception as e:
    tracker.log_exception(e)

tracker.log("this is a warning", "WARN")
tracker.log("this is an erroor", "ERROR")


# %%
tracker.close()

# %%
