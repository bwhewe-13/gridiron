
import styling as sty

import pygame
import numpy as np

def create_dimensions(cells_x, cells_y, materials=0):
    WIDTH = 20
    HEIGHT = 20
    MARGIN = 3
    # Set the HEIGHT and WIDTH of the screen
    WINDOW_X = cells_x * (MARGIN + WIDTH) + MARGIN
    WINDOW_Y = (cells_y + (materials + 1)) * (MARGIN + HEIGHT) + MARGIN
    return [WINDOW_X, WINDOW_Y], (WIDTH, HEIGHT, MARGIN)

def create_grid(screen, grid, colors, spatial):
    rows, columns = grid.shape
    materials = len(colors)
    for row in range(rows):
        for column in range(columns):
            color = colors[grid[row, column]]
            pygame.draw.rect(screen, color, [(spatial[2] + spatial[1]) \
                * row + spatial[2], (spatial[2] + spatial[0]) * (column \
                + materials + 1) + spatial[2], spatial[1], spatial[0]])

def create_legend(screen, material_dict, colors, spatial):
    font = pygame.font.Font(sty.FONT, sty.FONT_SIZE)
    label_names = list(material_dict.keys())
    label_values = list(material_dict.values())
    materials = len(label_names)
    colors = sty.COLORS[:materials]
    for mat in range(materials):
        pygame.draw.rect(screen, colors[mat], [spatial[2], (spatial[2] \
            + spatial[1]) * mat + spatial[2], spatial[0], spatial[1]])
        text = font.render(label_names[mat], True, sty.WHITE, sty.BLACK)
        screen.blit(text, ((spatial[2] + spatial[0]) + spatial[2], \
            (spatial[2] + spatial[1]) * mat + spatial[2]))

def update_grid(px, py, grid, materials, spatial):
    xx = px // (spatial[1] + spatial[2])
    yy = py // (spatial[0] + spatial[2]) - (materials + 1)
    if yy < 0:
        return grid
    grid[xx, yy] += 1 if (xx, yy) < grid.shape else 0
    grid[grid > (materials - 1)] = 0
    return grid

class SaveButton():

    def __init__(self, text, location, spatial):
        self.text = text
        self.x, self.y = location
        self.width, self.height = spatial

    def draw(self, screen, color=sty.GRAY):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(sty.FONT, sty.FONT_SIZE)
        text = font.render(self.text, True, sty.WHITE, color)
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), \
                        self.y + (self.height / 2 - text.get_height() / 2)))

    def save_grid(self, px, py, grid, material_dict, save_name):
        in_width = (px > self.x) and (px < self.x + self.width)
        in_height = (py > self.y) and (py < self.y + self.height)
        if in_width and in_height:
            save_info = {"medium_map": np.flip(grid,axis=1),
                         "material_key": material_dict}
            np.savez(save_name, **save_info)
            return True
        return False