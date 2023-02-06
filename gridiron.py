

import styling as sty
import util

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "0"
import pygame
import numpy as np

def mapping(cells_x, cells_y, dictionary, save_name):
    # Format input data
    materials = len(dictionary.keys())
    WINDOW_SIZE, spatial = util.create_dimensions(cells_x, cells_y, materials)
    grid = np.zeros((cells_x, cells_y), dtype=np.int32)
    colors = sty.COLORS[:materials]
    # Create Save Buttom
    save_width = 100
    save_loc = (WINDOW_SIZE[0] - save_width - spatial[2], spatial[2])
    save_size = (save_width, 40)
    save_button = util.SaveButton("Save Grid", save_loc, save_size)
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("2D Material Mapping")
    clock = pygame.time.Clock()
    done = False
    saved = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                px, py = pygame.mouse.get_pos()
                grid = util.update_grid(px, py, grid, materials, spatial)
                saved = save_button.save_grid(px, py, grid, dictionary, save_name)
        screen.fill(sty.BLACK)
        util.create_grid(screen, grid, colors, spatial)
        util.create_legend(screen, dictionary, colors, spatial)
        if saved:
            save_button.draw(screen, sty.GREEN)
            saved = False
        else:
            save_button.draw(screen)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    cells_x = 10
    cells_y = 10
    dictionary = {"uranium": 0, "plutonium": 1, "carbon": 2}
    save_name = "medium_map_test"
    mapping(cells_x, cells_y, dictionary, save_name)

