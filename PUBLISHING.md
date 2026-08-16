# Publishing

## Protocol for package updates

1. Add a `git tag` for the new version.
2. Update the version in [README.md](./build/tikz-nfold/README.md).
3. Add a changelog entry to [tikz-nfold-doc.tex](./tikz-nfold-doc.tex) and recompile that file.
4. Run `python3 build/build.py`, make sure it passes without errors or warnings.
5. Unpack the final zip file in a temporary directory and copy the [tests](./tests/) there.
6. Build all the tests and check for build errors and visual glitches.
7. Make sure that the tests actually used the new artifact by introducing a syntax error in each unpacked file. The compilation must fail.
   - This is to prevent false negatives due to the TeX compiler using the published version installed on the system instead of the new build.
8. Go to <https://ctan.org/upload>, log in, select _Package Update_, and enter the details.
   - Add a plain-text version of the changelog from a previous step to _Announcement via mailing list and RSS_.

## Original CTAN submission for reference

- Summary: Triple, quadruple, and n-fold paths with TikZ
- Description: This library adds higher-order paths to TikZ and also fixes some graphical issues with TikZ' double paths, used e.g. in arrows with an Implies tip. It is also compatible with tikz-cd, adding support for triple and higher arrows.
- Suggested CTAN directory: `graphics/pgf/contrib`
- Announcement: This new library adds support for n-fold paths (double, triple, quadruple, ...) in TikZ. Contrary to the approach of TikZ' /tikz/double, this works by offsetting the path instead of superimposing paths of various thicknesses, fixing some rendering issues of /tikz/double. Basic layer pgf code for offsetting Bezier curves is also provided.
- License: The LaTeX Project Public License 1.3c
- Home page: `https://github.com/jonschz/tikz-nfold`
- Bug tracker: `https://github.com/jonschz/tikz-nfold/issues`
- Repository: `https://github.com/jonschz/tikz-nfold`
