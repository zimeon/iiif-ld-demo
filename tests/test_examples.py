"""Check example outputs in tutorial.

In Git Flavored Markdown the three languages `sh`, `bash` and `shell` are treated as the
same (see: https://github.com/atom/language-gfm/blob/master/grammars/gfm.cson#L533-L549 ).
We will use `shell` to distinguish commands the represent things where the output is
intended to match the content of the next code block.
"""
from difflib import ndiff
import glob
import json
import json_delta
import misaka
import rdflib
import rdflib.compare
import re
try:
    from subprocess import getoutput  # py3
except:
    from commands import getoutput  # py2
import sys


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
    m = re.match(r'''([\w\-]+)\>\s+(\S.*)$''', command_line)
    if (not m):
        raise Exception("Bad command line: %s" % (command_line))
    return(m.group(1), m.group(2))


def compare_json(str1, str2):
    """Compare two JSON strings.

    Returns diff and changes required.
    """
    json1 = json.loads(str1)
    json2 = json.loads(str2)
    diff = json_delta.diff(json1, json2, minimal=True, verbose=False)
    if (len(diff) > 0):
        return(diff[0], diff[1])
    else:
        return('', '')


def compare_text(str1, str2, squash_space=True):
    """Compare two text strings, ignore space if squash_space is True.

    If squash_space then compact all whitespace to a single space and remove
    any blank lines. Return value is diff string, '' if match.
    """
    if (squash_space):
        str1 = re.sub(r'''([ \t\r\f\v]+)''', ' ', str1)
        str1 = re.sub(r'''([ \n]+)\n''', '', str1)
        str1 = str1.strip()
        str2 = re.sub(r'''([ \t\r\f\v]+)''', ' ', str2)
        str2 = re.sub(r'''([ \n]+)\n''', '', str2)
        str2 = str2.strip()
    return(''.join('' if l.startswith(' ') else l
           for l in ndiff(str1.splitlines(1), str2.splitlines(1))))


def check_markdown_file(filename):
    """Check markdown file for codeblock shell+output pairs."""
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
        elif (lang == 'sh' or lang == 'bash'):
            # A command we should not try to use
            command_line = None
        elif (command_line is not None):
            n += 1
            # Expect match from command in previous shell block
            (directory, command) = split_command_line(command_line)
            cmd = "cd %s && %s" % (directory, command)
            print("[%s %d] cmd: %s" % (filename, n, cmd))
            out = getoutput(cmd)
            if (lang == 'json'):
                (diff, changes) = compare_json(text, out)
                if (diff):
                    raise Exception("JSON output doesn't match:\n differences in %s\n changes to match %s" % (diff, changes))
            elif (lang == 'nt'):
                g1 = rdflib.Graph()
                g1.parse(data=text, format="nt")
                g2 = rdflib.Graph()
                g2.parse(data=out, format="nt")
                iso1 = rdflib.compare.to_isomorphic(g1)
                iso2 = rdflib.compare.to_isomorphic(g2)
                if (iso1 != iso2):
                    raise Exception("nt data doesn't match")
            else:
                diff = compare_text(text, out)
                if (diff):
                    raise Exception("Output strings don't match:\n" + diff)
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
print("%d/%d files passed (%d commands tested)" % (num_files - bad_files, num_files, commands))
if bad_files > 0:
    sys.exit(1)
