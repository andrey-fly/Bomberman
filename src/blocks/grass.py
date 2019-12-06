import pygame

from src.blocks.cell import Cell


class Grass(Cell):
    image = pygame.image.load(".././img/blocks/grass.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = "Grass"
