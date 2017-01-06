import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors

GREEN = 255
BLUE = 170
RED = 85
WHITE = 0
vals = [WHITE, RED, BLUE, GREEN]
# vals = [WHITE, GREEN]
cmap = colors.ListedColormap(['white', 'red', 'blue', 'green'])
# cmap = colors.ListedColormap(['white', 'green'])
bounds = [WHITE, RED-1, BLUE-1, GREEN-1, GREEN]
# bounds = [WHITE, GREEN/2, GREEN+1]
norm = colors.BoundaryNorm(bounds, cmap.N)

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.7, 0.1, 0.1, 0.1]).reshape(N, N)
    # return np.random.choice(vals, N*N, p=[0.8, 0.2]).reshape(N, N)

def addGlider(i, j, grid):
    """adds glider with top left cel at (i, j)"""
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider

def addBlock(i, j, grid):
    """adds block with top left at (i, j)"""
    block = np.array([[255, 255],
                      [255, 255]])
    grid[i:i+2, j:j+2] = block

def addBlinker(i, j, grid):
    """adds blinker with top left cel at (i, j)"""
    blinker = np.array([[0, 255, 0],
                       [0, 255, 0],
                       [0, 255, 0]])
    grid[i:i+3, j:j+3] = blinker

def alive(i, j, grid):
    return int(grid[i, j] > 0)

def update(frameNum, img, grid, N):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line
    newGrid = grid.copy()
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
                else:
                    newGrid[i, j] = RED
            else:
                if total == 3:
                    newGrid[i, j] = GREEN

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
    # check for glider flag
    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(1, 1, grid)
    elif args.block:
        grid = np.zeros(N*N).reshape(N, N)
        addBlock(1, 1, grid)
    elif args.blinker:
        grid = np.zeros(N*N).reshape(N, N)
        addBlinker(1, 1, grid)
    else:
        # randomize grid
        grid = randomGrid(N)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest', cmap=cmap, norm=norm)
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)

    # number of frames?
    # set the output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'livx264'])

    plt.show()

# call main
if __name__ == '__main__':
    main()
