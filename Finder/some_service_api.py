class Counter:
    def __init__(self):
        self.count = 0

    def loop_counter(self):
        self.count = self.count + 1

    def get_counter(self):
        return self.count


class Logger:
    def __init__(self, logfile='log', main_title="default title"):
        if not 'txt' in logfile:
            logfile +='.txt'
        self.log = open(logfile, 'w')
        print(main_title, file=self.log)

    def write_dual(self, title, data):
        print(title, file=self.log)
        for i in range(len(data)):
            print(data[i][0], file=self.log, end='\t')
            print(data[i][1], file=self.log)

    def write(self, title, data):
        print(title, file=self.log)
        if not len(data) == 0:
            for i in range(len(data)):
                print(data[i], file=self.log)
        else:
            print("Nothing found", file=self.log)

    def write_only_title(self, title):
        print(title, file=self.log)