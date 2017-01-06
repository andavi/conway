<h1>Conway's Game of Life</h1>

With colors, toroidal boundary conditions, and starting options.

Green for newly generated cells, blue for cells with 2 neighbors last turn, and red for cells with 3 neighbors last turn. White cells are empty/dead.

Use flags: --glider, --block, --blinker, --toad, --rpentomino, --pulsar, <strong>or</strong> --gosper to see different starting patterns.

Use: --grid-size [int] and/or --interval [int] to change grid-size and/or update-interval.

Example:

<em>$ python life.py --grid-size=64 --interval 25 --gosper</em>
