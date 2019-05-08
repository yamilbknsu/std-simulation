import pygame
import copy
import numpy as np
import CellularAutomata as pyCA

WIDTH = 500
HEIGHT = 500

if __name__ == "__main__":

    def _update_function(old_grid):
        grid = copy.deepcopy(old_grid)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if i>=1 and j >=1 and i < grid.shape[0]-1 and j < grid.shape[1]-1:
                    if grid[i][j].state == 1:
                        if (np.sum(x.state for x in old_grid[i-1:i+2, j-1:j+2].reshape(9,)) - 1 >= 4 or
                           np.sum(x.state for x in old_grid[i-1:i+2, j-1:j+2].reshape(9,)) - 1 <= 1):
                            grid[i][j].state = 0
                    else:
                        if np.sum(x.state for x in old_grid[i-1:i+2, j-1:j+2].reshape(9,)) == 3:
                            grid[i][j].state = 1
        return grid

    model = pyCA.CellularAutomata((50,50), np.random.binomial(1,.3,(50,50)))
    model.set_update_function(_update_function)


    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    done = False


    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            
            model.grid = model.update_function(model.grid)

            pygame.draw.rect(screen, (22,32,41), pygame.Rect(0,0,WIDTH, HEIGHT))
            model.draw(screen, 500)
            pygame.display.flip()
            clock.tick(50)