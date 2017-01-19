import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors

WHITE = 0
GREEN = 1
BLUE = 2
RED = 3
GRAY = -1
vals = [GRAY, WHITE, RED, BLUE, GREEN, ]
# vals = [WHITE, GREEN]
cmap = colors.ListedColormap(['gray', 'white', 'green', 'blue', 'red'])
# cmap = colors.ListedColormap(['white', 'green'])
bounds = [GRAY-.5, WHITE-.5, GREEN-.5, BLUE-.5, RED-.5, RED+.5]
# bounds = [WHITE, GREEN/2, GREEN+1]
norm = colors.BoundaryNorm(bounds, cmap.N)

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.7, 0.1, 0.1, 0.1, 0.0]).reshape(N, N)
    # return np.random.choice(vals, N*N, p=[0.8, 0.2]).reshape(N, N)

def addGlider(i, j, grid):
    """adds glider with top left cell at (i, j)"""
    glider = np.array([[0, 0, 1],
                       [1, 0, 1],
                       [0, 1, 1]])
    grid[i:i+3, j:j+3] = glider

def addBlock(i, j, grid):
    """adds block with top left cell at (i, j)"""
    block = np.array([[1, 1],
                      [1, 1]])
    grid[i:i+2, j:j+2] = block

def addBlinker(i, j, grid):
    """adds blinker with top left cell at (i, j)"""
    blinker = np.array([[0, 1, 0],
                       [0, 1, 0],
                       [0, 1, 0]])
    grid[i:i+3, j:j+3] = blinker

def addToad(i, j, grid):
    """adds toad with top left cell at (i, j)"""
    toad = np.array([[0, 0, 1, 0],
                       [1, 0, 0, 1],
                       [1, 0, 0, 1],
                       [0, 1, 0, 0]])
    grid[i:i+4, j:j+4] = toad

def addPulsar(i, j, grid):
    """adds pulsar with top left cell at (i, j)"""
    pulsar = np.array([[0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                       [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                       [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                       [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]])
    grid[i:i+13, j:j+13] = pulsar

def addRPentomino(i, j, grid):
    """adds R-pentomino"""
    pentomino = np.array([[0, 1, 1],
                       [1, 1, 0],
                       [0, 1, 0]])
    grid[i:i+3, j:j+3] = pentomino

def addGosperGliderGun(i, j, grid):
    """adds a Gosper Glider Gun with top left cell at (i, j)"""
    gun = np.zeros(11*38).reshape(11, 38)

    gun[5][1] = gun[5][2] = 1
    gun[6][1] = gun[6][2] = 1

    gun[3][13] = gun[3][14] = 1
    gun[4][12] = gun[4][16] = 1
    gun[5][11] = gun[5][17] = 1
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 1
    gun[7][11] = gun[7][17] = 1
    gun[8][12] = gun[8][16] = 1
    gun[9][13] = gun[9][14] = 1

    gun[1][25] = 1
    gun[2][23] = gun[2][25] = 1
    gun[3][21] = gun[3][22] = 1
    gun[4][21] = gun[4][22] = 1
    gun[5][21] = gun[5][22] = 1
    gun[6][23] = gun[6][25] = 1
    gun[7][25] = 1

    gun[3][35] = gun[3][36] = 1
    gun[4][35] = gun[4][36] = 1

    grid[i:i+11, j:j+38] = gun

def alive(i, j, grid):
    return int(grid[i, j] > 0)

def update(frameNum, img, grid, N, inspect):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line
    newGrid = grid.copy()
    if not inspect:
        for i in range(N):
            for j in range(N):
                # compute 8 neighbors
                total = int(alive(i, (j-1)%N, grid) + alive(i, (j+1)%N, grid) +
                        alive((i-1)%N, j, grid) + alive((i+1)%N, j, grid) +
                        alive((i-1)%N, (j-1)%N, grid) + alive((i-1)%N, (j+1)%N, grid) +
                        alive((i+1)%N, (j-1)%N, grid) + alive((i+1)%N, (j+1)%N, grid))
                # apply rules
                if alive(i, j, grid):

                    if (total < 2) or (total > 3):
                        newGrid[i, j] = WHITE
                    elif (total == 2):
                        newGrid[i, j] = BLUE
                        # inspect.add((i, j))
                        # for m in range(-1,2):
                        #     for n in range(-1,2):
                        #         inspect.add(((i+m)%N, (j+n)%N))
                    else:
                        newGrid[i, j] = RED
                        # for m in range(-1,2):
                        #     for n in range(-1,2):
                        #         inspect.add(((i+m)%N, (j+n)%N))
                    for m in range(-1,2):
                        for n in range(-1,2):
                            inspect.add(((i+m)%N, (j+n)%N))
                            if newGrid[(i+m)%N, (j+n)%N] == WHITE:
                                newGrid[(i+m)%N, (j+n)%N] = GRAY
                else:
                    if total == 3:
                        newGrid[i, j] = GREEN
                        for m in range(-1,2):
                            for n in range(-1,2):
                                inspect.add(((i+m)%N, (j+n)%N))
                                if newGrid[(i+m)%N, (j+n)%N] == WHITE:
                                    newGrid[(i+m)%N, (j+n)%N] = GRAY

    else:
        nextInspect = inspect.copy()
        for i, j in nextInspect:
            # compute 8 neighbors
            total = int(alive(i, (j-1)%N, grid) + alive(i, (j+1)%N, grid) +
                    alive((i-1)%N, j, grid) + alive((i+1)%N, j, grid) +
                    alive((i-1)%N, (j-1)%N, grid) + alive((i-1)%N, (j+1)%N, grid) +
                    alive((i+1)%N, (j-1)%N, grid) + alive((i+1)%N, (j+1)%N, grid))
            # apply rules
            if alive(i, j, grid):
                if (total < 2) or (total > 3):
                    newGrid[i, j] = WHITE
                    # inspect.remove((i, j))
                elif (total == 2):
                    newGrid[i, j] = BLUE
                    # for m in range(-1,2):
                    #     for n in range(-1,2):
                    #         inspect.add(((i+m)%N, (j+n)%N))
                    #         if newGrid[(i+m)%N, (j+m)%N] == WHITE:
                    #             newGrid[(i+m)%N, (j+m)%N] = GRAY
                else:
                    newGrid[i, j] = RED
                    # for m in range(-1,2):
                    #     for n in range(-1,2):
                    #         inspect.add(((i+m)%N, (j+n)%N))
                    #         if newGrid[(i+m)%N, (j+m)%N] == WHITE:
                    #             newGrid[(i+m)%N, (j+m)%N] = GRAY
                for m in range(-1,2):
                    for n in range(-1,2):
                        inspect.add(((i+m)%N, (j+n)%N))
                        if newGrid[(i+m)%N, (j+n)%N] == WHITE:
                            newGrid[(i+m)%N, (j+n)%N] = GRAY
            else:
                if total == 3:
                    newGrid[i, j] = GREEN
                    for m in range(-1,2):
                        for n in range(-1,2):
                            inspect.add(((i+m)%N, (j+n)%N))
                            if newGrid[(i+m)%N, (j+n)%N] == WHITE:
                                newGrid[(i+m)%N, (j+n)%N] = GRAY
            # print len(inspect)

        # inspect = inspect.union(inspect)
    print len(inspect)
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--block', action='store_true', required=False)
    parser.add_argument('--blinker', action='store_true', required=False)
    parser.add_argument('--toad', action='store_true', required=False)
    parser.add_argument('--rpentomino', action='store_true', required=False)
    parser.add_argument('--pulsar', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()

    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # declare grid
    grid = np.array([])
    inspect = set()
    # check for glider flag
    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(1, 1, grid)
    elif args.block:
        grid = np.zeros(N*N).reshape(N, N)
        addBlock(N/2-1, N/2-1, grid)
    elif args.blinker:
        grid = np.zeros(N*N).reshape(N, N)
        addBlinker(N/2-2, N/2-2, grid)
    elif args.toad:
        grid = np.zeros(N*N).reshape(N, N)
        addToad(N/2-2, N/2-2, grid)
    elif args.rpentomino:
        grid = np.zeros(N*N).reshape(N, N)
        addRPentomino(N/2-2, N/2-2, grid)
    elif args.pulsar:
        if N < 16:
            N = 16
        grid = np.zeros(N*N).reshape(N, N)
        addPulsar(N/2-7, N/2-7, grid)
    elif args.gosper:
        if N < 39:
            N = 39
        grid = np.zeros(N*N).reshape(N, N)
        addGosperGliderGun(N/2-6, N/2-19, grid)
    else:
        # randomize grid
        grid = randomGrid(N)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest', cmap=cmap, norm=norm)
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, inspect,),
                                  frames=10000,
                                  interval=updateInterval,
                                  save_count=50)

    # number of frames?
    # set the output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()

# call main
if __name__ == '__main__':
    main()
