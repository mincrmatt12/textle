from lark import Lark

l = Lark("""
%import common.WS
%ignore WS

%import common.ESCAPED_STRING
%import common.CNAME
%import common.LETTER

FNAME: ("."|LETTER)+

pipeline: a_step ("->" a_step)+

a_step: step ("+" step)*
step: name_options [":" FNAME ("," FNAME)*]

name_options: CNAME ("." CNAME)*
""", start="pipeline")

