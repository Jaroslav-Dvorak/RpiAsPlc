from resettabletimer import ResettableTimer


class TOF:
    def __init__(self, t):
        self.Q = False
        self.T = ResettableTimer(t, self.time_reached)
        self.T.start()

    def trig(self):
        self.Q = True
        self.T.reset()

    def time_reached(self):
        self.Q = False


my_timer = TOF(5)
