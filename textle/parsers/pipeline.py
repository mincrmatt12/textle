from lark import Lark

pipeline_raw = """
FNAME: /[^ '"@]+/

pipeline: a_step ("->" a_step)+

a_step: step ("+" step)*
step: name_options [":" fileref ("," fileref)*]

fileref: FNAME -> fname
       | "@" FNAME -> placeholder

name_options: CNAME ("." CNAME)*
"""

l = Lark("""
%import common.WS
%ignore WS

%import common.ESCAPED_STRING
%import common.CNAME
%import common.LETTER""" + pipeline_raw, start="pipeline")
