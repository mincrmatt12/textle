import enum

class FileUse(enum.enum):
    INPUT = 1,
    GENERATED = 2,
    OUTPUT = 3


class FileRef:
    def __init__(self, tag, ext, use, output_step=None):
        self.tag = tag
        self.output_step = None
        self.ext = ext
        self.use = use
