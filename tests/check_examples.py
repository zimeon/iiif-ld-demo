"""

In Git Flavored Markdown the three languages `sh`, `bash` and `shell` are treated as the
same (see: https://github.com/atom/language-gfm/blob/master/grammars/gfm.cson#L533-L549 ).
We will use `shell` to distinguish commands the represent things where the output is 
intended to match the content of the next code block.
"""
import misaka

class CodeExtracter(misaka.HtmlRenderer):

    """Rendered class for Mikasa that extracts code blocks."""

    def __init__(self, **kwargs):
        """Initialize with added self.codeblocks list."""
        super(CodeExtracter,self).__init__(**kwargs )
        self.codeblocks = []

    def blockcode(self, text, lang):
        """Append text and lang of code block in self.codeblocks."""
        self.codeblocks.append([text,lang])

def extract_codeblocks(md_file):
    md = open(md_file,'r').read()
    ce = CodeExtracter()
    msk = misaka.Markdown(ce, extensions=('fenced-code',))
    msk(md)
    return(ce.codeblocks)

codeblocks = extract_codeblocks('image-api/section_read_image_info.md')
command = None
for codeblock in codeblocks:
    (text, lang) = codeblock
    if (lang == 'shell'):
        if (command is not None):
            raise Exception("Consecutive command blocks, (%s) and (%s)" % (command, text.strip()))
        command = text.strip()
        print("Got command to match: ",command)
    elif (command is not None):
        # Expect match from command in previous shell block
        print("command: ", command)
        print("expected match: ", text)
        command = None
if (command is not None):
    raise Exception("Trailing command (%s) with no expected output to check" % (command))
