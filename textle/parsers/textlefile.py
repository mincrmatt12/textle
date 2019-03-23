from lark import Lark
from .pipeline import pipeline_raw

l = Lark("""
%import common.WS
%ignore WS
%ignore /^#.*$/m

%import common.ESCAPED_STRING
%import common.CNAME
%import common.LETTER
%import common.NUMBER

BOOLEAN: "true" | "false"
DEFAULT: "default"

?value: NUMBER
      | ESCAPED_STRING
      | BOOLEAN
      | DEFAULT

textlefile: version_decl options ("---" pipeline_i)+

version_decl: "version" NUMBER
options: (CNAME "=" value)*

pipeline_i: pipeline options (section options)*

section: "[" CNAME "]"
""" + pipeline_raw, start="textlefile")

VERSION = 1

