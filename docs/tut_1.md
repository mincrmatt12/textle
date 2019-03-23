# Getting Started

`textle` operates on the principle that the build process can be modelled as a pipeline, and a `textle` project is composed of a set of steps that when composed will create the target file.

These pipelines are represented in the following textual format:

```
tool[.subtype]:[filename[,filename2 ...]] [+ extra[.subtype]:filename ... ] -> ... -> sink:filename
```

For example, `xetex:my_tex_file.tex -> pdf:my_tex_file.pdf` tells `textle` to take `my_tex_file.tex`, send it through `xetex` and write the output to the PDF `my_tex_file.pdf`.
The final step in a pipeline is called the "sink", because it is where all of the files get merged into. It is also the only step where the filename is an output and not an input.

You could also chain `pandoc` to `xetex` with `pandoc.markdown:input.md -> xetex -> pdf:out.pdf`. Notice how we don't need to give `xetex` an input filename, as it comes from the 
previous step. You could also just send the output of `pandoc` to the `pdf` sink, and it will let `pandoc` invoke it's own PDF engine.

Steps can also have "extras" which are usually other tools that need invoking with them. The canonical example is `biber`, or any other `bibtex` driver.
For example, you could have `xetex:my_tex.tex + biber:my_bib.bib -> pdf:out.pdf`, which tells `textle` to also run `biber` properly, and to monitor changes on `my_bib.bib` as well.

## In practise

To actually get `textle` to do something, you have to create a `Textlefile`. You can do this by either creating it manually (see later on in this guide), or use `textle new`.

`textle new` takes first the list of pipelines you want to build in this project, as there can be more than one. It then takes options to pass to the steps themselves.

!!! note
	`textle new` does not support giving different steps with the same types in different pipelines different options, although the `Textlefile` format does.

For example,

```
$ textle new "xetex:my_file.tex + biber:bib.bib -> pdf:my_file.pdf"
```

which will create a `Textlefile` to do that pipeline.

You can also give options to the steps, but that will be in a later instalment of this guide.

## Building

You can build your `textle` project with either of the following two commands:

```
$ textle go
$ # or
$ textle live
```

The first will build the project once, and the second will sit and build the project whenever the source files change on disk.
