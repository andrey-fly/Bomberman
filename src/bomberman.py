import pygame

from src.cell import Cell


class Bomberman(Cell):
    image = pygame.image.load("img/bomberman.png")

    def __init__(self, x=50, y=125):
        super().__init__(x, y)
        self.shift_x = 0
        self.shift_y = 0
        self.speed = 5
        self.can_move_Right = True
        self.can_move_Left = True
        self.can_move_Up = True
        self.can_move_Down = True

    def process_draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self, 5))

    def process_logic(self, width, height, area):
        if self.rect.x + self.shift_x < 50:
            self.shift_x = 0
        if self.rect.y + self.shift_y < 125:
            self.shift_y = 0
        if self.rect.y + self.shift_y > height - 25:
            self.shift_y = 0
        if self.rect.left < 50:
            self.rect.left = 50
        if self.rect.top < 125:
            self.rect.top = 125
        if self.rect.left < 50:
            self.rect.right = 50

    def move(self):
        if self.shift_x > 0 and self.can_move_Right:
            self.rect.move_ip(self.shift_x, 0)
        if self.shift_x < 0 and self.can_move_Left:
            self.rect.move_ip(self.shift_x, 0)
        if self.shift_y > 0 and self.can_move_Down:
            self.rect.move_ip(0, self.shift_y)
        if self.shift_y < 0 and self.can_move_Up:
            self.rect.move_ip(0, self.shift_y)