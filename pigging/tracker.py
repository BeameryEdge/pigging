import logging
import os
from datetime import datetime

"""Tracks the ETL script from start to finish.

Allows users to track timing of a ETL script, create a lock file
to avoid running the script twice of something fails, and creates a 
log file to track the activity and critical failure errors.

Typical usage example:

tracker = Tracker(lock_path = "./lock.lock", log_path="./log.log")
tracker.start()

tracker.log("This is a block of code", "INFO")
try:
    print("Hello world!")
except Exception as e:
    tracker.log_exception(e)

tracker.stop()
"""


class Tracker(object):
    """Tracks creates a log and a lock file to track ETL activity and time.

    The Tracker will initalize with the location of a log file and a lock 
    file to be created when you start your script. Then you can use the
    different methods to start timing, check if the lock file exists,
    log activity, remove the lock file and time your script.

    Attributes:
        LOG_PATH: A string containing a path to the log file.
        LOCK_PATH: A string containing a path to the lock file.
        script_start: A datetime object of the current runtime.
    """

    def __init__(self, log_path, lock_path):
        """Inits Tracker with log_path and lock_path, and starts a script timer."""
        self.LOG_PATH = log_path
        self.LOCK_PATH = lock_path
        self.script_start = datetime.utcnow()

    def start(self):
        """Creates lock file and resets log file.

        The script checks if a lock file exists. If it does it will raise an
        Exception, else it will get created, then it will check if a log file
        exists. If it does, it will remove it and create a new log file. Then
        it will start the logger a specific format.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: An error if the script is already locked on double runs.
        """

        log_script_start = self.script_start.strftime(
            " % Y-%m-%d % H: % M: % S")

        if os.path.exists(self.LOCK_PATH):
            with open(self.LOG_PATH, "a") as myfile:
                myfile.write(f"{log_script_start} | ERROR: Locked \n")
            raise Exception("Locked. Manually delete the lock file")
        else:
            open(self.LOCK_PATH, "x")

        if os.path.exists(self.LOG_PATH):
            os.remove(self.LOG_PATH)
            with open(self.LOG_PATH, "a") as myfile:
                myfile.write(f"{log_script_start} | INFO: Starting logging \n")

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s: %(message)s")
        file_handler = logging.FileHandler(filename=self.LOG_PATH)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, message, level="INFO"):
        """Writes message to log file.

        Will log activity into the log file at different levels including
        INFO, WARN or ERROR. If the level is not specified, the method 
        will write at a INFO level.

        Args:
            message:
                A message that will be written in your log file.
            level: 
                The level of the message including INFO, WARN or ERROR.

        Returns:
            None

        Raises:
            Exception: An error if there is no acceptable logging level.
        """
        if level == "INFO":
            self.logger.info(message)
        elif level == "WARN":
            self.logger.warn(message)
        elif level == "ERROR":
            self.logger.error(message)
        else:
            raise Exception("Logging level should be INFO, WARN or ERROR")

    def log_exception(self, exception):
        """Logs an error message.

        Logs an ERROR message with an exception passed directly from the 
        try catch block where we typically use 'except Exception as e`.

        Args:
            exception:
                This should be the exception passed from the except function.

        Returns:
            None

        Raises:
            Exception: An error on the try catch block if something fails during
            execution.
        """
        self.log(exception, "ERROR")
        raise Exception(exception)

    def stop(self):
        """Closes the ETL run script.

        Logs the TOTAL SCRIPT TIME and removes the lock file.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        script_stop = datetime.utcnow()
        time_diff = script_stop - self.script_start
        message = f"Stopped logging. Total script runtime is {time_diff}"
        self.logger.info(message)
        print(message)
        os.remove(self.LOCK_PATH)
