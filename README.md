# tikz-nfold – higher order paths in TikZ

This library adds higher-order paths to [TikZ][pgf] and also fixes some graphical issues with TikZ' `double` paths, used e.g. in wide arrows. It is also compatible with [tikz-cd][tikz-cd], adding support for triple and higher arrows. See the [documentation](tikz-nfold-doc.pdf) for full details.

[pgf]: https://ctan.org/pkg/pgf
[tikz-cd]: https://ctan.org/pkg/tikz-cd

## Installation

This package is available on TeX Live,  MiKTeX and [CTAN](https://ctan.org/pkg/tikz-nfold). If you choose to install this package manually, copy all files except `tikz-nfold-doc.tex` and `tikz-nfold-doc.pdf` into your `tex` folder.

## License

This work may be distributed and/or modified under the conditions of the LaTeX Project Public License, either version 1.3c of this license or (at your option) any later version.

## Contributing

Any kind of help is welcome! Feel free to test the library, report issues, and open pull requests. In the latter case, be sure to compile the [unit tests](https://github.com/jonschz/tikz-nfold/tree/main/tests) before and after your changes and look for deviations.

## Impressions

![tikz-cd](./images/screenshot_tikzcd.png)

![rainbow](./images/screenshot_rainbow.png)

![joins](./images/screenshot_join.png)
