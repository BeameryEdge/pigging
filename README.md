![](./coverage.svg)

# Pigging

Pigging is a Python library created by Beamery's Edge team that helps building robust, reliable and scalable data engineering pipelines.

#### About the name

> Pigging refers to the practice of using mechanical devices known as 'pigs' to perform maintenance operations in pipelines; scrubbing the insides of the lines in order to clean them. [Source](https://www.ftl.technology/news/engineering-news/what-is-pipeline-pigging-and-how-does-it-work#:~:text=Pigging%20refers%20to%20the%20practice,in%20order%20to%20clean%20them.)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pigging directly from Github.

```bash
pip3 install git+https://github.com/BeameryEdge/pigging
```

### Requirements

The repository also includes the `requirements.txt` file that includes the Python dependencies for the pigging package.

## Usage

### Tracking

```python
from pigging.tracker import Tracker

LOG_PATH = "./log_file.log"
LOCK_PATH = "./lock_file.lock"
tracker = Tracker(log_path=LOG_PATH, lock_path=LOCK_PATH)

# Create the log and lock files, and start timing the script
tracker.start()


# Code block
tracker.log("Printing hello world...", "INFO")
try:
    # Your code here!
    print("Hello world!")
except Exception as e:
    tracker.log_exception(e)


# Remove the lock file and log the script time
tracker.stop()
```

<!-- ### Connectors

Right now we have enabled Google BigQuery import and export connectors.

```python
from pigging.import_connectors import importConnectors
from pigging.export_connectors import exportConnectors

import_connector = importConnectors("./gcp_credentials.json")
export_connector = exportConnectors("./gcp_credentials.json")

# Import data
df = import_connector.google_big_query(QUERY, PROJECT_ID)

# Export data
export_connector.google_big_query(df, DESTINATION_TABLE, PROJECT_ID, IF_EXISTS)
``` -->
