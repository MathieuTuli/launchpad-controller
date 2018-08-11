"""
Cleanup is a class for cleaning up your code upon 'control-c'-ing
"""
import sys
import signal
import time

class Cleanup():
    def __init__(self, settings):
        """
        :param setings = {
            'object_to_clean': object to be cleaned up. Object must have a method called 'cleanup'
            }
        """
        self.object_to_clean = settings['object_to_clean']
        signal.signal(signal.SIGINT, self.sigint_handler)

    def sigint_handler(self, segnum, frame):
        print("\n\nRunning user defined cleanup function.")
        cleanup_method = getattr(self.object_to_clean, "cleanup", None)
        if callable(cleanup_method):
            cleanup_method()
            print("Cleaned.\n")
        else:
            print("Error: your object does not have a method called 'cleanup'\n")
        sys.exit(0)
