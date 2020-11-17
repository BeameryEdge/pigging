import pytest
from pigging.tracker import Tracker
import os
import warnings

LOG_PATH = "./log.log"
LOCK_PATH = "./lock.lock"
tracker = Tracker(lock_path=LOCK_PATH, log_path=LOG_PATH)


class TestTrackerStartup(object):
    def test_lock_file_created(self):
        tracker.startup()
        assert os.path.isfile(
            LOCK_PATH) == True, "The LOCK_PATH file should exist"

        # Clean up
        os.remove(LOG_PATH)
        os.remove(LOCK_PATH)

    def test_log_file_created(self):
        tracker.startup()
        assert os.path.isfile(
            LOG_PATH) == True, "The LOG_PATH file should exist"

        # Clean up
        os.remove(LOG_PATH)
        os.remove(LOCK_PATH)

    def test_script_locked_raises_exception(self):
        tracker.startup()
        with pytest.raises(Exception):
            tracker.startup()

        # Clean up
        os.remove(LOG_PATH)
        os.remove(LOCK_PATH)


class TestTrackerClose(object):
    def test_lock_file_removed(self):
        tracker.startup()
        tracker.close()
        assert os.path.isfile(
            LOCK_PATH) == False, "The LOCK_PATH file should be removed"

        # Clean up
        os.remove(LOG_PATH)

    def test_script_end_time_was_recorded(self):
        tracker.startup()
        tracker.close()
        with open(LOG_PATH, 'r') as f:
            data = f.read()
            assert "TOTAL SCRIPT TIME" in data, "The LOG_PATH file should have TOTAL SCRIPT TIME after close"

        # Clean up
        os.remove(LOG_PATH)


class TestTrackerLog():
    def test_log_info(self):
        tracker.startup()
        tracker.log("This is an INFO log test", "INFO")

        with open(LOG_PATH, 'r') as f:
            data = f.read()
            assert "This is an INFO log test" in data, "The LOG_PATH file should have an INFO message"

        # Clean up
        os.remove(LOG_PATH)
        os.remove(LOCK_PATH)

    def test_log_warn(self):
        tracker.startup()
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        tracker.log("This is a WARN log test", "WARN")

        with open(LOG_PATH, 'r') as f:
            data = f.read()
            assert "This is a WARN log test" in data, "The LOG_PATH file should have an WARN message"

        # Clean up
        os.remove(LOG_PATH)
        os.remove(LOCK_PATH)

    def test_log_error(self):
        tracker.startup()
        tracker.log("This is an ERROR log test", "ERROR")

        with open(LOG_PATH, 'r') as f:
            data = f.read()
            assert "This is an ERROR log test" in data, "The LOG_PATH file should have an ERROR message"

        # Clean up
        os.remove(LOG_PATH)
        os.remove(LOCK_PATH)

    def test_log_raises_exception(self):
        tracker.startup()
        with pytest.raises(Exception):
            tracker.log("This is a log test", "NOT A CATEGORY")

        # Clean up
        os.remove(LOG_PATH)
        os.remove(LOCK_PATH)


class TestTrackerLogException():
    def test_log_exception_raises_exception(self):
        tracker.startup()
        with pytest.raises(Exception):
            tracker.log_exception("This is an exception")

        # Clean up
        os.remove(LOG_PATH)
        os.remove(LOCK_PATH)

    def test_log_exception_logs_error(self):
        tracker.startup()
        try:
            tracker.log_exception("This is an exception")
        except Exception:
            pass

        with open(LOG_PATH, 'r') as f:
            data = f.read()
            assert "This is an exception" in data, "The LOG_PATH file should have an ERROR message"

        # Clean up
        os.remove(LOG_PATH)
        os.remove(LOCK_PATH)
