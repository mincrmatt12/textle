# bare tex

`textle new "xetex:in.tex -> pdf:out.pdf"`

# tex and bib

`textle new "xetex:in.tex + biber:test.bib -> pdf:out.pdf"`

# pandoc to tex to bib

`textile new "pandoc.markdown:in.md -> xetex + biber:test.bib -> pdf:out.pdf"`

## pipeline format:

```
tool[.option]:[filename[,filename2 ...]] [+ helper[.option]:filename ... ] -> ... -> sink:filename

currently there's only a "pdf" sink, which xetex/pdftex can generate directly

tex.[driver]

xetex is alias to tex.xelatex
pdftex is alias to tex.pdftex

tex picks best option

pandoc.[infiletype]

runs output from pandoc.

if a tool doesn't take a filename it takes the output of the previous
likewise, the output of a tool can read what it must satisfy, allowing pandoc.markdown -> tex to work out that it needs to output tex.
if it was

pandoc.markdown:test.md -> pdf:direct.pdf

it would just tell pandoc to make the pdf itself

biber is alias to bibtex.biber
biblatex is alias to bibtex.biblatex

biber takes a .bib file (which is only used for dependency checking, unless called with pandoc in which it is an alias for --bibliography)
it runs biber on the tex file, sometimes running it multiple times
```

## other arguments

These relate to a multitude of options. Specific tool options can be configured with this syntax:

`--[toolname]:[paramname]`

Some global tool options are:
	
- `needs files,that,this,step,needs,to,be,in,the,current,dir,while,building`

## templates

`textle new mla_markdown:in.md -> pdf:test.pdf`

templates are defined by either:

- using `textle template new mla_markdown "pandoc.markdown:@infile1 -> xetex + biber:@infile2" --pandoc:template /home/matthew/my-mla.tex --pandoc:biblatex --xetex:needs /home/matthew/my-mla.bbx`
- or using `textle template new mla_markdown --from-textlefile Textfile.template` where that textlefile uses `@references` instead of files, and there is no [sink] section

they are stored in the same format as described in the second case in the directories /etc/textle/templates and ~/.textle/templates.

use in a new

`textle new mla_markdown:test.md,test.bib -> pdf:out.pdf --use-template mla_markdown` or `--use-template /path/to/template/textlefile`

# compilation

`textle go` will compile the entire project, building what is up to date

`textle live` will continue to compile the project as changes are made, as well as running the appropriate software (configurable in .textle/config.json) to view the result.

NOTE: textle live _blocks_ so you should run it in the background using your particular shell's capabilities to do so -- it won't output anything to stdout unless you use `--verbose`
