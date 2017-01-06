import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# x = np.array([[0, 0, 255], [255, 255, 0], [0, 255, 0]])
# y = np.random.choice([0, 255], 4*4, p=[0.2, 0.8]).reshape(4, 4)
# print y
# plt.imshow(y, interpolation='nearest')
# plt.show()

N = 4
def addGlider(i, j, grid):
    """adds glider with top left cel at (i, j)"""
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider
grid = np.zeros(N*N).reshape(N, N)
addGlider(1, 1, grid)
plt.imshow(grid, interpolation='nearest')
plt.show()
