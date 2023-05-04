# TODO

## Known issue
- Closed paths are not yet rendered correctly when the final (`\pgfpathclose`) segment is an edge case. There are multiple reasons for this:
  1. `invisibleline` and `closepath` segments must be checked for the edge case, which is not implemented yet
  1. `invisibleline` and `closepath` segments must be shortened on *both* ends, so their start *and* end angles must be set correctly. Furthermore, they must be shortened even though their previous/subsequent segment is formally invisible. Neither is implemented
  1. If the above were implemented, there may still be issues left to solve

## Near future
- consider splitting `tikzlibrarynfold.code.tex` into a pgf and a TikZ library, as most of it does not need TikZ
- look for potential issues with large paper sizes

## Structure
- pull request to TikZ/pgf to simplify code injection

## Features
- `angle too sharp` detection: Is there a better way to detect if we move a point back too far?
  - May be possible for lines but very hard for curves
- do curvature checks and throw warnings at the start and end of offset segments

## Performance
- remove direct and indirect `\pgfmathparse` calls, mostly in the joins
  - check if `\pgf@nfold@roundjoin` can be simplified before optimising
- add `\else` in various places (likely better performance)
- the `A1A4` length is computed for every offset; this is something we could cache from the subdivision phase
- faster, less precise `veclen@` -> this is being used a lot
  - if `x > y`, compute `x*(1+(y/x)^2)^(1/2) approx x*(A+B*(y/x)^2)`; optimize `A=1.` and `B=.5` over the unit circle
  - could copy a lot of the existing veclen code; maybe skip the "scaling for precision" steps?
- rendering: are quick commands an option? `qmoveto`, `qlineto` etc.?