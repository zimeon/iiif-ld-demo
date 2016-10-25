"""Check example outputs in tutorial.

In Git Flavored Markdown the three languages `sh`, `bash` and `shell` are treated as the
same (see: https://github.com/atom/language-gfm/blob/master/grammars/gfm.cson#L533-L549 ).
We will use `shell` to distinguish commands the represent things where the output is
intended to match the content of the next code block.
"""
import glob
import json
import json_delta
import misaka
import re
import subprocess


class CodeExtracter(misaka.HtmlRenderer):
    """Rendered class for Mikasa that extracts code blocks."""

    def __init__(self, **kwargs):
        """Initialize with added self.codeblocks list."""
        super(CodeExtracter, self).__init__(**kwargs)
        self.codeblocks = []

    def blockcode(self, text, lang):
        """Append text and lang of code block in self.codeblocks."""
        self.codeblocks.append([text, lang])


def extract_codeblocks(md_file):
    """Extract all codeblocks, returning list of [text, lang]."""
    md = open(md_file, 'r').read()
    ce = CodeExtracter()
    msk = misaka.Markdown(ce, extensions=('fenced-code', ))
    msk(md)
    return(ce.codeblocks)

def split_command_line(command_line):
    """Split the directory and actual command from example start."""
    m = re.match(r'''([\w\-]+)\>\s+(\S.*)''', command_line)
    if (not m):
        raise Exception("Bad command line: %s" % (command_line))
    return(m.group(1), m.group(2))

def check_markdown_file(filename):
    codeblocks = extract_codeblocks(filename)
    command_line = None
    n = 0
    for codeblock in codeblocks:
        (text, lang) = codeblock
        if (lang == 'shell'):
            if (command_line is not None):
                raise Exception("Consecutive command blocks, (%s) and (%s)" % (command, text.strip()))
            command_line = text.strip()
            print("Got command to match: ", command_line)
        elif (command_line is not None):
            n += 1
            # Expect match from command in previous shell block
            (directory, command) = split_command_line(command_line)
            cmd = "cd %s && %s" % (directory, command)
            print("[%s %d] cmd: %s" % (filename, n, cmd))
            out = subprocess.getoutput(cmd)
            if (lang == 'json'):
                json1 = json.loads(text)
                json2 = json.loads(out)
                diff = json_delta.diff(json1, json2, minimal=True ,verbose=False)
                if (len(diff)>0):
                    raise Exception("JSON output doesn't match:\n errors in %s\n changes to match %s" % (diff[0], diff[1]))
            else:
                print("output: ", out)
                print("expected match: ", text)
                if (out != text):
                    raise Exception("Output strings don't match")
            command_line = None
    if (command_line is not None):
        raise Exception("Trailing command (%s) with no expected output to check" % (command))
    return n

# Loop over and test all markdown files
num_files = 0
bad_files = 0
commands = 0
for filename in glob.glob("*/*.md"):
    num_files += 1
    print("[%s] ..." % (filename))
    try:
        commands += check_markdown_file(filename)
    except Exception as e:
        bad_files += 1
        print("[%s] Tests failed: %s" % (filename, str(e)))
print("%d/%d files passed (%d commands tested)" % (num_files-bad_files, num_files, commands))
exit(1 if bad_files > 0 else 0)
