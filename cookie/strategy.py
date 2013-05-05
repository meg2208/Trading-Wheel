

class Strategy:

    def __init__(self, name, allocation, triggers=None):
        self.name = name
        self.allocation = allocation
        if triggers:
            self.triggers = triggers
        else:
            self.triggers = []

    def __str__(self):
        to_string = 'strategy: {}\nstarted w/: {}\ntriggers:{}\n'.format(
            self.name, self.allocation, self.triggers)
        return to_string
