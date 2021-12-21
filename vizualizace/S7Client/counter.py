import json


class Counter:
    def __init__(self):

        self.counter_filename = "counter.txt"
        self.init_counter()

    def init_counter(self):
        try:
            with open(self.counter_filename, "r") as f:
                self.value = json.loads(f.read())
        except Exception as e:
            print(e)
            self.value = 0

    @property
    def value(self):
        return self._counter

    @value.setter
    def value(self, counter):
        s = json.dumps(counter, indent=4)
        try:
            with open(self.counter_filename, "w") as f:
                f.write(s)
        except Exception as e:
            print(e)
        self._counter = counter
