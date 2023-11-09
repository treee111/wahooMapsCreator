"""
functions for timing sections of code, and output results in log lines
"""
#!/usr/bin/python

# import official python packages
import time
import logging

log = logging.getLogger('main-logger')


class Timings:
    """Class for starting the wall time, and logging when done"""
    wall_time_start = None
    wall_time_end = None

    def __init__(self):
        """Start the wall time"""
        self.wall_time_start = time.perf_counter()

    def stop_wall_time(self):
        """Stop the wall time"""
        self.wall_time_end = time.perf_counter()

    def stop_and_return(self, additional_info='') -> str:
        """Stop and return text"""
        self.stop_wall_time()
        return self.get_text_summary(additional_info)

    def stop_and_log(self, additional_info=''):
        """Log the time taken"""
        self.stop_wall_time()
        log.info('-' * 80)
        log.info(self.get_text_summary(additional_info))

    def get_text_summary(self, additional_info='') -> str:
        """Get text summarizing the timings"""
        time_taken_msg = f'{self.wall_time_end - self.wall_time_start:.3f} s'
        if additional_info:
            return f'{additional_info} {time_taken_msg}'
        return f'took {time_taken_msg}'
