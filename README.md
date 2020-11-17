# Pigging

Pigging is a Python library created by Beamery's Edge team that helps building robust, reliable and scalable data engineering pipelines.

#### About the name

> In pipeline transportation, pigging is the practice of using pipeline inspection gauges, devices generally referred to as pigs or scrapers, to perform various maintenance operations. This is done without stopping the flow of the product in the pipeline. [Wikipedia](https://en.wikipedia.org/wiki/Pigging)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pigging directly from Github.

```bash
pip install git+https://github.com/BeameryEdge/pigging
```

### Requirements

The repository also includes the `requirements.txt` file that includes the Python dependencies for the the pigging package.

## Usage

### Tracking

```python
from pigging import Tracker

LOG_PATH = "./log_file.log"
LOCK_PATH = "./lock_file.log"
tracker = Tracker(log_path=LOG_PATH, lock_path=LOCK_PATH)

# Create the log and lock files, and start timing the script
tracker.startup()

# Code block
tracker.log("Printing hello world...", "INFO")
try:
    # Your code goes here!
    print("Hello world!")
except Exception as e:
    tracker.log_exception(e)

# Remove the lock file and log the script time
tracker.close()
```

### Connectors

Right now we have enabled Google BigQuery import and export connectors.

```python
from pigging import importConnectors, exportConnectors

import_connector = importConnectors("./gcp_credentials.json")
export_connector = exportConnectors("./gcp_credentials.json")

# Import data
df = import_connector.google_big_query(QUERY, PROJECT_ID)

# Export data
export_connector.google_big_query(df, DESTINATION_TABLE, PROJECT_ID, IF_EXISTS)
```
