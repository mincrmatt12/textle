from lark import Lark, Tree
from ..pipeline import steps, Pipeline
from ..fileref import FileRef, FileUse
import os

pipeline_raw = """
FNAME: /[^ '"@]+/

pipeline: a_step ("->" a_step)+

a_step: step ("+" step)*
step: name_options [":" fileref ("," fileref)*]

fileref: FNAME -> fname
       | "@" FNAME -> placeholder

name_options: CNAME ["." CNAME]
"""

l = Lark("""
%import common.WS
%ignore WS

%import common.ESCAPED_STRING
%import common.CNAME
%import common.LETTER""" + pipeline_raw, start="pipeline")

def string_to_pipeline(string):
    return tree_to_pipeline(l.parse(string))

def _construct_params(s_obj_tree):
    name_options = s_obj_tree.children[0]
    if len(name_options.children) == 1:
        name = name_options.children[0].value
        subtype = ""
    else:
        name = name_options.children[0].value
        subtype = name_options.children[1].value

    if len(s_obj_tree.children) > 1:
        frefs = s_obj_tree.children[1:]
        files = []

        for fref in frefs:
            if fref.data == "placeholder":
                raise NotImplementedError("placeholder")
            fname = fref.children[0].value
            tag, ext = os.path.splitext(fname)
            files.append(FileRef(tag, ext, FileUse.INPUT))
    else:
        files = []

    return name, subtype, files

def _construct(name, *args):
    try:
        cls = (x for x in steps if x.name == name).next()
        return cls(*args)
    except StopIteration:
        raise ValueError("Invalid step/sink type {}".format(name))

def tree_to_pipeline(tree: Tree, root):
    # Generate steps
    step_objs = []
    for step in tree.children:
        s_obj, *extras = step.children

        extras = [
            _construct(*(_construct_params(x) + ([],))) for x in extras
        ]

        step_objs.append(_construct(*(_construct_params(s_obj) + (extras,))))
    
    return Pipeline(step_objs, root)
