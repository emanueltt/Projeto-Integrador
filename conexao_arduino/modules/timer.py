import time


class TimerSeconds:
    def __init__(self):
        self.start_time = time.time_ns()

    def elapsed_time(self):
        elapsed = (self.__get_current_time() - self.start_time) / 1e9
        return elapsed

    def reset(self):
        self.start_time = time.time_ns()

    def __get_current_time(self):
        return time.time_ns()
