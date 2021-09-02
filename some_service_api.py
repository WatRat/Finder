class Counter:
    def __init__(self):
        self.count = 0

    def loop_counter(self):
        self.count = self.count + 1

    def get_counter(self):
        return self.count


class Output:
    def __init__(self, logfile):
        self.log = logfile
