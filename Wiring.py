# A file where all the "wiring" is done, i.e. all the hardware related stuff.
# Kind of a hardware abstraction layer (HAL).


class Display(object):

    def __init__(self, name, hardware):
        self.name = name


