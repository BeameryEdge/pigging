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

The `Tracker` module will initalize with the location of a log file and a lock file to be created when you start your script. Then you can use the different methods check if the lock file exists, log ETL activity, and time your script.

#### Starting the ETL script

We can use `tracker.start()` method to tell the Tracker we have started the ETL script. The `.start()` method will do the following:

1. Check if a lock file exists. If there is no lock file it will create one that will remain in the location during the script run or if there is an error during the run.
2. Check if a log file exists. If there is no log file it will get created. If there is an old log file, it will remove it and create a clean one. We do this because the nature of this log files is to understand if there was a failure during the latest run.
3. Start an internal timer.

#### Logging ETL activity

We have also leveraged the `logging` library to track the activity across the ETL script. we can use `tracker.log("message")` to log activity at different point of the ETL script. We have also included the `tracker.log_exception(e)` method that will take in a `e` variable from a try catch exception to understand where our code fails.

#### Closing the ETL script

Finally, we can use the `tracker.stop()` method to stop the timer and log the final runtime as well as removing the lock file to avoid any errors during the next run.

#### Tracker example

```python
from pigging.tracker import Tracker

LOG_PATH = "./log_file.log"
LOCK_PATH = "./lock_file.lock"
tracker = Tracker(log_path=LOG_PATH, lock_path=LOCK_PATH)

# Create the log and lock files, and start timing the script
tracker.start()


# Code block
tracker.log("Printing hello world...")
try:
    # Your code here!
    print("Hello world!")
except Exception as e:
    tracker.log_exception(e)


# Remove the lock file and log the script time
tracker.stop()
```

### Connectors (_Under development_)

The `Connectors` module allows users to connect to their desired data sources to import and export data leveraging built in API objects.
