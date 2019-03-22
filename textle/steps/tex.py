from ..pipeline import Step

class TeXStep(Step):
    """
    The generic TeX step.
    
    The option for this is the tex driver to use, e.g xetex or pdftex

    """

    def handles_extra_type(self, et):
        return et == "biblatex"

    def __init__(self, files, subtype, extras, options):
        super().__init__(files, subtype, extras, options)

        # this is a thingy

