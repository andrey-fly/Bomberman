import pygame

from src.blocks.cell import Cell



class Bomberman(Cell):
    image = pygame.image.load("img/bomberman/stand/Front.png")

    def __init__(self, x=50, y=125):
        super().__init__(x, y)
        self.shift_x_left = 0
        self.shift_x_right = 0
        self.shift_y_up = 0
        self.shift_y_down = 0
        self.shift_x = 0
        self.shift_y = 0
        self.speed = 5
        self.can_move_Right = True
        self.can_move_Left = True
        self.can_move_Up = True
        self.can_move_Down = True
        # for bonus:
        self.max_count_bombs = 1
        self.long_fire = 2

    def process_draw(self, screen, camera, x=0, y=75):
        screen.blit(self.image, camera.apply(self))

    def process_logic(self, height):
        if self.rect.x + self.shift_x < 50:
            self.shift_x_left = 0
        if self.rect.y + self.shift_y < 125:
            self.shift_y_up = 0
        if self.rect.y + self.shift_y > height - 25:
            self.shift_y_down = 0

    def move(self):
        if self.shift_x > 0 and self.can_move_Right:
            self.rect.move_ip(self.shift_x, 0)
        if self.shift_x < 0 and self.can_move_Left:
            self.rect.move_ip(self.shift_x, 0)
        if self.shift_y > 0 and self.can_move_Down:
            self.rect.move_ip(0, self.shift_y)
        if self.shift_y < 0 and self.can_move_Up:
            self.rect.move_ip(0, self.shift_y)
