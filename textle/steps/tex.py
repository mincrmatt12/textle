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
        return et in ("biblatex", "glossaries")

    def __init__(self, files, subtype, extras, options):
        super().__init__(files, subtype, extras, options)


        self.has_bib = False
        self.has_glossary = False
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
            if extra.name == "glossaries":
                self.has_glossary = True
        
    def get_input_types_valid(self):
        return ["tex"]

    def get_output_type(self):
        return "pdf"

    def get_products(self):
        return super().get_products() + [
            FileRef(self.input.tag, "bcf", FileUse.GENERATED),
            FileRef(self.input.tag, "bbl", FileUse.GENERATED),
        ] if self.has_bib else [] + [FileRef(self.input.tag, "glo", FileUse.GENERATED)] if self.has_glossary else []

    def get_dependencies_for(self, product):
        # Ignores has bib because we can just generate it

        pdf_output = self.files
        if self.has_bib:
            pdf_output.append(FileRef(self.input.tag, "bbl", FileUse.GENERATED))
        if self.has_glossary:
            pdf_output.append(FileRef(self.input.tag, "glo", FileUse.GENERATED))

        if product.ext == "pdf":
            return pdf_output
        elif product.ext == "bbl":
            return [
                FileRef(self.input.tag, "bcf", FileUse.GENERATED),
            ]
        elif product.ext == "bcf":
            return self.files + [self.bib_source]
        elif product.ext == "glo":
            return self.files

    def solve_inout(self):
        pass

    def get_command_for(self, product):
        pdf = self.output
        bcf = FileRef(self.input.tag, "bcf", FileUse.GENERATED)
        bbl = FileRef(self.input.tag, "bbl", FileUse.GENERATED)
        glo = FileRef(self.input.tag, "glo", FileUse.GENERATED)

        if product == pdf:
            return ([self.driver, "-interaction=batchmode", self.input],[MV, FileRef(self.input.tag, "pdf", FileUse.GENERATED), pdf]) 
        elif product == bbl:
            return ([self.bib_driver, FileRef(self.input.tag, None, FileUse.GENERATED)],)
        elif product == bcf:
            return ([self.driver, self.input],)
        elif product == glo:
            return (["makeglossaries", FileRef(self.input.tag, None, FileUse.GENERATED)],)

