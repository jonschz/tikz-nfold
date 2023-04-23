# TODO

## Near future
- consider splitting `tikzlibrarynfold.code.tex` into a pgf and a TikZ library, as most of it does not need TikZ
- look for potential issues with large paper sizes

## Structure
- pull request to TikZ/pgf to simplify code injection

## Features
- properly implement `\pgfclosepath`
- `angle too sharp` detection: Is there a better way to detect if we move a point back too far?
  - May be possible for lines but very hard for curves
- do curvature checks and throw warnings at the start and end of offset segments

## Performance
- remove direct and indirect `\pgfmathparse` calls, mostly in the joins
  - check if `\pgf@nfold@roundjoin` can be simplified before optimising
- Reuse results of tangent and angle computations
  - at the moment, the start/end tangents and angles of segments are computed 3 (?) times
  - `sin(deltaphi)`, `cos(deltaphi)` and `tan(deltaphi)` are also computed multiple times
- add `\else` in various places (likely better performance)
- Do the subdivision of Bezier curves while parsing the soft path -> saves a lot of redundant calls
