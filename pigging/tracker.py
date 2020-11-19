import logging
import os
from datetime import datetime


class Tracker(object):
    def __init__(self, log_path, lock_path):
        self.LOG_PATH = log_path
        self.LOCK_PATH = lock_path
        self.script_start = datetime.utcnow()

    def start(self):
        if os.path.exists(self.LOCK_PATH):
            with open(self.LOG_PATH, "a") as myfile:
                myfile.write(
                    f"""{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} | ERROR: Locked \n"""
                )
            raise Exception(
                "Your script is locked. Manually delete the lock file")
            # os.sys.exit(1)
        else:
            open(self.LOCK_PATH, "x")

        if os.path.exists(self.LOG_PATH):
            # print("Removing old log file...")
            os.remove(self.LOG_PATH)
            with open(self.LOG_PATH, "a") as myfile:
                myfile.write(
                    f"""{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} | INFO: Starting logging \n"""
                )

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s: %(message)s")
        file_handler = logging.FileHandler(filename=self.LOG_PATH)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, message, level="INFO"):
        if level == "INFO":
            self.logger.info(message)
        elif level == "WARN":
            self.logger.warn(message)
        elif level == "ERROR":
            self.logger.error(message)
        else:
            raise Exception("Logging level should be INFO, WARN or ERROR")

    def log_exception(self, exception):
        self.log(exception, "ERROR")
        raise Exception(exception)
        # os.sys.exit(1)

    def stop(self):
        script_stop = datetime.utcnow()
        self.logger.info(
            f"TOTAL SCRIPT TIME: {script_stop - self.script_start}")
        print(f"TOTAL SCRIPT TIME: {script_stop - self.script_start}")
        os.remove(self.LOCK_PATH)
