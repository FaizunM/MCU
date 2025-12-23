class BoardPower:
    def __init__(self):
        self.is_plugged = False

    def get_5V(self):
        return 5.0 if self.is_plugged else 0.0

    def get_3V3(self):
        return 3.3 if self.is_plugged else 0.0

    def plug_power(self):
        self.is_plugged = True

    def unplug_power(self):
        self.is_plugged = False
