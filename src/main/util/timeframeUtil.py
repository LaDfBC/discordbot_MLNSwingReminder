from enum import Enum

class TimeFrame(Enum):
    MINUTES = [1, 'm', 'minutes']
    HOURS = [60, 'h', 'hours']

    def get_multiplier(self):
        return self.value[0]

    def get_abbreviation(self):
        return self.value[1]

    def get_name(self):
        return self.value[2]

if __name__ == '__main__':
    for time in TimeFrame:
        print(time[0])