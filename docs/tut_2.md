# The `Textlefile`

`textle` stores the pipelines and configuration for a project in a file called the `Textlefile`. This file looks a bit like an INI file, but with some key changes.

!!! note
	The formal grammars for both the pipeline format and textlefiles can be found in the source code under `textle/parsers`.

Lines starting with a `#` are ignored. The file always begins with a version declaration. The current version is 1.

Next, there are a set of `key=value` declarations that apply to the entire project -- these are called global options. The format of a value is either a `"string"`, an integer (`12`), or a boolean (`true` or `false`).
The key does not have quotes around it. Lists are created by specifying the same key multiple times, ordering is top to bottom.

Next are a set of pipeline declarations, each starting with the line `---`. Next is the pipeline in the same format as on the command line, and then a bunch of INI-style sections, with the same type of key value pairs as above.

A full example is reproduced below.

```
version 1

externals="/home/matthew/mla_template.tex"
---

pandoc.markdown:essay.md -> xetex + biber:bib.bib -> pdf:essay.pdf

[pandoc]
bib_source="biblatex"
template="mla_template.tex"
```

As you can see, the INI-style sections correspond to options per step type. A full list of options can be found in the [usage reference](ref_main.md).

## Specifying options to `textle new`

You can also specify options when running `textle new`, however all pipelines will get the same step options. To do this, you can pass options of the form `--<step or global>:<option name>:[<type>] <value>`.

The `<type>` is optional, and if not present will be guessed based on the text, otherwise it is `str`, `int`, or `bool`. `<step or global>` is either a step type or the word `global`, which sets global options.
As with the format itself, specifying the same option multiple times will create a list, ordered left to right.

For example, to create the `Textlefile` shown above:

```
$ textle new "pandoc:markdown:essay.md -> xetex + biber:bib.bib -> pdf:essay.pdf" --global:externals /home/matthew/mla_template.tex --pandoc:bib_source biblatex --pandoc:template mla_template.tex
```
