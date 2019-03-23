from ..pipeline import Step
from ..fileref import FileRef, FileUse
from .shell_help import MV

class TeXStep(Step):
    """
    The generic TeX step.
    
    The option for this is the tex driver to use, e.g xetex or pdftex

    """

    name = "tex"

    def handles_extra_type(self, et):
        return et == "biblatex"

    def __init__(self, files, subtype, extras, options):
        super().__init__(files, subtype, extras, options)


        self.has_bib = False
        self.driver = "xetex" if subtype is None else subtype

        for x in extras:
            print(x.name)

        # this is a thingy
        for extra in self.extras:
            # interpret options
            if extra.name == "biblatex":
                if not extra.files:
                    raise ValueError("Extra biblatex must have a source")
                self.has_bib = True
                self.bib_options = extra.options
                self.bib_source = extra.files[0]
                self.bib_driver = "biber" if extra.subtype is None else extra.subtype
        
    def get_input_types_valid(self):
        return ["tex"]

    def get_output_type(self):
        return "pdf"

    def get_products(self):
        if self.has_bib:
            return super().get_products() + [
                FileRef(self.input.tag, "bcf", FileUse.GENERATED),
                FileRef(self.input.tag, "bbl", FileUse.GENERATED),
            ]
        else:
            return super().get_products()

    def get_dependencies_for(self, product):
        # Ignores has bib because we can just generate it

        if product.ext == "pdf" and not self.has_bib:
            return self.files
        elif product.ext == "pdf":
            return self.files + [
                FileRef(self.input.tag, "bbl", FileUse.GENERATED),
            ]
        elif product.ext == "bbl":
            return [
                FileRef(self.input.tag, "bcf", FileUse.GENERATED),
            ]
        elif product.ext == "bcf":
            return self.files + [self.bib_source]

    def solve_inout(self):
        pass

    def get_command_for(self, product):
        pdf = self.output
        bcf = FileRef(self.input.tag, "bcf", FileUse.GENERATED)
        bbl = FileRef(self.input.tag, "bbl", FileUse.GENERATED)

        if product == pdf:
            return ([self.driver, "-interaction=batchmode", self.input],[MV, FileRef(self.input.tag, "pdf", FileUse.GENERATED), pdf]) 
        elif product == bbl:
            return ([self.bib_driver, FileRef(self.input.tag, None, FileUse.GENERATED)],)
        elif product == bcf:
            return ([self.driver, self.input],)

