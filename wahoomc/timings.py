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

    def start_wall_time(self):
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
        self.log_duration(additional_info)

    def log_duration(self,additional_info=''):
        """Log the time taken"""
        log.info(self.get_text_summary(additional_info))

    def get_text_summary(self, additional_info='') -> str:
        """Get text summarizing the timings"""
        if additional_info:
            return f'{additional_info} {self.wall_time_end - self.wall_time_start:.2f} s'
        return f'took {self.wall_time_end - self.wall_time_start:.2f} s'
