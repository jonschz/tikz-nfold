from dataclasses import dataclass
import functools
from pathlib import Path
import re
from datetime import date
import shutil
import subprocess
from typing import Final
from zipfile import ZipFile, ZIP_DEFLATED

EXCLUDED_FILES = ["testfile.tex"]
OUTPATH = Path("./build")
PROJECTNAME = "tikz-nfold"
ASSEMBLE_PATH = OUTPATH.joinpath(PROJECTNAME)

@dataclass
@functools.total_ordering # due to the suffix, this is technically not a total ordering
class Version:
    major: int
    minor: int
    subminor: int
    suffix: str
    
    TAG_RE: Final[re.Pattern] = re.compile(r'(\d+)\.(\d+)\.(\d+)(\S*)')

    def __init__(self, version_str: str):
        match = self.TAG_RE.search(version_str)
        if not match:
            raise ValueError("Does not contain a version string")
        groups = match.groups()
        self.major = int(groups[0])
        self.minor = int(groups[1])
        self.subminor = int(groups[2])
        self.suffix = groups[3]
    
    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.subminor}{self.suffix}"
    
    def __ge__(self, other) -> bool:
        if self.major != other.major:
            return self.major >= other.major
        elif self.minor != other.minor:
            return self.minor >= other.minor
        else:
            return self.subminor >= other.subminor

# regex to remove comments
comment_re = re.compile(r'^([^%]*%).*$')
# a line that has only a comment and no code
comment_line_re = re.compile(r'^\s*%')

def process_file(file_list: list[Path], filename_in: Path):
    year = date.today().year
    header = f"""%% {filename_in.name}
%% Copyright {year} Jonathan Schulz
%
% This work may be distributed and/or modified under the
% conditions of the LaTeX Project Public License, either version 1.3c
% of this license or (at your option) any later version.
% The latest version of this license is in
% http://www.latex-project.org/lppl.txt
% and version 1.3c or later is part of all distributions of LaTeX
% version 2008-05-04 or later.
%
% This work has the LPPL maintenance status 'maintained'.
%
% The Current Maintainer of this work is Jonathan Schulz.
%
% This work consists of the files
% {", ".join(f.name for f in file_list)}, tikz-nfold-doc.tex, and tikz-nfold-doc.pdf.
%
%
% A commented version of this file can be found on https://github.com/jonschz/tikz-nfold .
%
"""
    filename_out = ASSEMBLE_PATH.joinpath(filename_in.name)
    with filename_in.open('r') as infile, filename_out.open('w') as outfile:
        outfile.write(header)
        for line in infile.readlines():
            # remove full line comments
            if comment_line_re.match(line):
                continue
            # remove comments the end of lines, leave the '%' in
            comment_match = comment_re.match(line)
            if comment_match:
                groups = comment_match.groups()
                line = groups[0]

            if line.endswith('\n'):
                outfile.write(line[:-1])
            else:
                outfile.write(line)
            outfile.write('\n')
            

def main():
    
    # Find the new revision according to the README.md
    with ASSEMBLE_PATH.joinpath("README.md").open('r') as readme_file:
        readme_file.readline()
        second_line = readme_file.readline() # the version is in the second line
        readme_version = Version(second_line)

    # Find the existing git tags
    tag_output_bytes = subprocess.run("git tag", capture_output=True)
    tags = tag_output_bytes.stdout.decode('ascii').splitlines()
    tags = [Version(tag) for tag in tags]
    tags.sort(reverse=True)
    latest_git_version = tags[0]

    # Check if the README.md has a new version number
    if readme_version <= latest_git_version:
        print(f"Error: Version in README.md not updated (README: {readme_version}, git: {latest_git_version})")
        return 1
    
    print(f"Current README version: v{readme_version}; latest git version: v{latest_git_version}")

    # Check if there is a change log in tikz-nfold-doc.tex
    with Path("tikz-nfold-doc.tex").open('r') as docfile:
        cont = docfile.read()
        assert len(docfile.read()) == 0
        if cont.find("\\textbf{v%s}" % readme_version) < 0:
            print(f"Error: Missing changelog entry for version v{readme_version}")
            return 1

    # empty the assembly directory
    for filename in ASSEMBLE_PATH.iterdir():
        if filename.name != "README.md":
            filename.unlink()
    
    print("Compiling the documentation...")
    compile_doc = subprocess.run(["pdflatex", "tikz-nfold-doc.tex"], capture_output=True)
    if compile_doc.returncode != 0:
        print("Compiling the documentation was not successful, see the log for details")
        return 1
    shutil.copy("tikz-nfold-doc.pdf", ASSEMBLE_PATH.joinpath("tikz-nfold-doc.pdf"))
    print("Done.")
    
    print("Removing comments from the source files...")
    file_list = [f for f in Path(".").iterdir() if f.suffix == '.tex' and f.name not in EXCLUDED_FILES]
    for filename in file_list:
        process_file(file_list, filename)
    print("Done.")

    print("Generating the zip file...")
    with ZipFile(OUTPATH.joinpath(f"tikz-nfold-v{readme_version}.zip"), 'w', compression=ZIP_DEFLATED, compresslevel=5) as zipfile:
        for filename in ASSEMBLE_PATH.iterdir():
            zipfile.write(filename, f"tikz-nfold/{filename.name}")
    print("Done")


if __name__ == '__main__':
    main()