import pygame
import numpy as np

class CellularAutomata():

    def __init__(this, shape, initial_states = None, update_function = None):
        this.shape = shape

        if initial_states.any():
            if initial_states.shape == shape:
                this.grid = []
                for i in range(shape[0]):
                    alist = []
                    for j in range(shape[1]):
                        alist.append(cell(initial_states[i,j]))
                    this.grid.append(alist)
            else:
                raise ValueError("Grid shape and initial state inconsistent shapes.")
        else:
            this.grid = []
            for i in range(shape[0]):
                alist = []
                for j in range(shape[1]):
                    alist.append(cell())
                this.grid.append(alist)
        this.grid = np.array(this.grid)

    def set_update_function(this, f):
        this.update_function = f

    def draw(this, screen, size, margin = 20, x_offset = 0, y_offset = 0):

        cell_size = (int)((size-2*margin)/this.shape[0]) if this.shape[0] > this.shape[1] else (int)((size-2*margin)/this.shape[1])

        # Drawing the grid
        for i in range(this.shape[0]-1):
            pygame.draw.line(screen, (107,107,107), (x_offset + margin, y_offset + margin + (i+1)*cell_size),
                                                    (x_offset + margin + cell_size*this.shape[0], y_offset + margin + (i+1)*cell_size))
        for j in range(this.shape[1]-1):
            pygame.draw.line(screen, (107,107,107), (x_offset + margin + (j+1)*cell_size, y_offset + margin),
                                                    (x_offset + margin + (j+1)*cell_size, y_offset + margin + this.shape[1]*cell_size))
        
        # Draw the cells
        for i in range(this.shape[0]):
            for j in range(this.shape[1]):
                ##TODO Implement alpha channel
                if this.grid[i][j].state == 1:
                    pygame.draw.rect(screen, (255,255,255), pygame.Rect(x_offset + margin + cell_size*i, y_offset + margin + cell_size*j, cell_size, cell_size))

class cell():

    def __init__(this, init_state = None, properties = None):
        if init_state:
            this.state = init_state
        else:
            this.state = 0
        
        this.properties = properties
    
    def update_property(this, index, value):
        this.properties[index] = value
        