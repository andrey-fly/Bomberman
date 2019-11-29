import sys
import pygame
import time
from random import randint

from src.blocks.grass import Grass
from src.bomb.bomb import Bomb
from src.bomb.fires.firehoriz import FireHorizontal
from src.bomb.fires.firemid import FireMiddle
from src.bomb.fires.firevert import FireVertical
from src.charachters.bomberman import Bomberman
from src.field.area import Area
from src.field.camera import Camera, camera_func
from src.field.score import Player_Score


# class Sound_left:
#     file = 'sounds/in_field/right-left.ogg'
#
#     def __init__(self, play):
#         self.play = play
#
#     def stop_sound(self, stop):
#         self.play = stop
#         if self.play:
#             pygame.mixer.Sound('sounds/in_field/right-left.ogg').play()
#     # def __init__(self, bomberman_x):
#     #     pygame.mixer.Sound('sounds/in_field/right-left.ogg').play()
#     #     self.bm_pr_x = bomberman_x
#     #     self.bm_now_x = bomberman_x
#     #     self.should_play = True
#     #
#     # def try_to_play(self, bomberman_x):
#     #     self.bm_now_x = bomberman_x
#     #     if self.bm_pr_x - self.bm_now_x <= 0:
#     #         self.should_play = False
#     #     else:
#     #         self.should_play = True
#     #     if self.should_play:
#     #         pygame.mixer.Sound('sounds/in_field/right-left.ogg').play()
#     #     self.bm_pr_x = self.bm_now_x


class Music:
    themes = ['./sounds/themes/theme_1.ogg',
              './sounds/themes/theme_2.ogg',
              './sounds/themes/theme_3.ogg',
              './sounds/themes/theme_4.ogg',
              './sounds/themes/theme_5.ogg',
              './sounds/themes/theme_6.ogg',
              './sounds/themes/theme_7.ogg',
              './sounds/themes/theme_8.ogg',
              './sounds/themes/theme_9.ogg',
              './sounds/themes/theme_10.ogg']

    def __init__(self):
        index = randint(0, len(self.themes) - 1)
        pygame.mixer.music.load(self.themes[index])
        pygame.mixer.music.set_volume(0.1)

    def play(self):
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()


class Sound:
    sound_file = None

    def __init__(self):
        self.sound = pygame.mixer.Sound(self.sound_file)
        self.sound.set_volume(0.1)
        self.start_time = None
        self.len = 0.25

    def play(self):
        if self.start_time is None:
            self.sound.play()
            self.start_time = time.time()

    def stop(self):
        self.sound.stop()

    def process_logic(self):
        if self.start_time is not None:
            if time.time() - self.start_time > self.len:
                self.stop()
                self.start_time = None


class SoundMove(Sound):
    sound_file = './sounds/in_field/right-left.ogg'

    def __init__(self):
        super().__init__()
        self.len = 0.25


class Game:
    def __init__(self, width=800, height=625):
        pygame.mixer.pre_init(44100, -16, 2, 64)
        pygame.mixer.init()
        self.area = Area()
        self.bomberman = Bomberman()
        self.bomb = Bomb()
        self.camera = Camera(camera_func, self.area.width, self.area.height)
        self.width = width
        self.height = height
        self.size = (width, height)
        self.bomb_x_in_area = 0
        self.bomb_y_in_area = 0
        self.game_over = False
        self.is_bomb = False
        self.is_pressed_up = False
        self.is_pressed_left = False
        self.is_pressed_down = False
        self.is_pressed_right = False
        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        self.music = Music()
        self.bombs = []
        self.fires = []
        self.player = Player_Score()

        self.sounds = [SoundMove()]

    #   self.sound_l = Sound_left(False)

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == 97 or event.key == 276 or event.key == 160:
                    self.is_pressed_left = True
                    # self.sound_l.stop_sound(self.is_pressed_left)
                    self.bomberman.shift_x_left = -self.bomberman.speed
                elif event.key == 100 or event.key == 275 or event.key == 162:
                    self.is_pressed_right = True
                    self.bomberman.shift_x_right = self.bomberman.speed
                elif event.key == 115 or event.key == 274 or event.key == 161:
                    self.is_pressed_down = True
                    self.bomberman.shift_y_down = self.bomberman.speed
                elif event.key == 119 or event.key == 273 or event.key == 172:
                    self.is_pressed_up = True
                    self.bomberman.shift_y_up = -self.bomberman.speed
                # Обработка нажатия клавиши E (для взрыва)
                elif (event.key == 101 or event.key == 173) and not self.bomb.is_bomb:
                    self.bomb.bomb_larger_middle_x = self.bomb_place_x()
                    self.bomb.bomb_larger_middle_y = self.bomb_place_y()
                    if self.bomb.bomb_larger_middle_x:
                        self.bomb.bomb_x_in_area = int((self.bomberman.rect.x - (
                                self.bomberman.rect.x % 50)) // 50)
                    elif not self.bomb.bomb_larger_middle_x:
                        self.bomb.bomb_x_in_area = int((self.bomberman.rect.x - (
                                self.bomberman.rect.x % 50)) // 50) + 1
                    if self.bomb.bomb_larger_middle_y:
                        self.bomb.bomb_y_in_area = int((self.bomberman.rect.y - 75 - (
                                (self.bomberman.rect.y - 75) % 50)) // 50)
                    elif not self.bomb.bomb_larger_middle_y:
                        self.bomb.bomb_y_in_area = int((self.bomberman.rect.y - 75 - (
                                (self.bomberman.rect.y - 75) % 50)) // 50) + 1
                    self.bombs.append(Bomb(self.bomb.bomb_x_in_area * 50, self.bomb.bomb_y_in_area * 50 + 75))
                    if len(self.bombs) == self.bomberman.max_count_bombs:
                        self.bomb.is_bomb = True
                self.bomberman.shift_x = self.bomberman.shift_x_left + self.bomberman.shift_x_right
                self.bomberman.shift_y = self.bomberman.shift_y_up + self.bomberman.shift_y_down
            if event.type == pygame.KEYUP:
                if event.key == 97 or event.key == 276 or event.key == 160:
                    self.is_pressed_left = False
                    self.bomberman.shift_x_left = 0
                elif event.key == 100 or event.key == 275 or event.key == 162:
                    self.is_pressed_right = False
                    self.bomberman.shift_x_right = 0
                elif event.key == 115 or event.key == 274 or event.key == 161:
                    self.is_pressed_down = False
                    self.bomberman.shift_y_down = 0
                elif event.key == 119 or event.key == 273 or event.key == 172:
                    self.is_pressed_up = False
                    self.bomberman.shift_y_up = 0
                self.bomberman.shift_x = self.bomberman.shift_x_left + self.bomberman.shift_x_right
                self.bomberman.shift_y = self.bomberman.shift_y_up + self.bomberman.shift_y_down

    def process_collisions(self):
        self.bomberman.can_move_Right = True
        self.bomberman.can_move_Left = True
        self.bomberman.can_move_Up = True
        self.bomberman.can_move_Down = True
        # Collisions
        all_objects = self.area.objects + self.bombs + self.fires  # Список всех объектов поля, для обработки коллизии
        for objects in all_objects:
            if objects.type == "Bomb" and objects.rect.colliderect(self.bomberman):
                return
            if objects.type == "Fire" and objects.rect.colliderect(self.bomberman):
                print("Game Over")
                self.game_over = True
                return
            if objects.type != 'Grass' and objects.type != 'Fire':
                if objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x + self.bomberman.speed, self.bomberman.rect.y)):
                    self.bomberman.can_move_Right = False
                if objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x - self.bomberman.speed, self.bomberman.rect.y)):
                    self.bomberman.can_move_Left = False
                if objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x, self.bomberman.rect.y + self.bomberman.speed)):
                    self.bomberman.can_move_Down = False
                if objects.rect.colliderect(
                        Bomberman(self.bomberman.rect.x, self.bomberman.rect.y - self.bomberman.speed)):
                    self.bomberman.can_move_Up = False
        for i in range(len(self.area.objects)):
            for fire in self.fires:
                if self.area.objects[i].type == 'Brick' and self.area.objects[i].rect.colliderect(fire):
                    self.area.objects[i] = Grass(fire.rect.x, fire.rect.y)

    def process_move(self):
        self.bomberman.move()

    def process_draw(self):
        self.screen.fill((75, 100, 150))
        self.camera.update(self.bomberman)
        self.area.process_draw(self.screen, self.camera)
        # Score
        self.player.refresh_area(self.screen)
        self.process_draw_bomb()
        self.process_draw_fires()
        self.bomberman.process_draw(self.screen, self.camera)

    def process_draw_fires(self):
        for fire in self.fires:
            fire.process_draw(self.screen, self.camera)

    def process_logic_fires(self):
        if len(self.fires):
            if self.fires[0].try_blow():
                self.fires.clear()

    def process_logic_bombs(self):
        for i in range(len(self.bombs)):
            if self.bombs[i].try_blow():
                self.generate_fires(self.bombs[i].rect.x, self.bombs[i].rect.y)
                self.bombs.pop(i)
                self.bomb.is_bomb = False
                break

    def process_draw_bomb(self):
        for bomb in self.bombs:
            bomb.process_draw(self.screen, self.camera)

    def bomb_place_x(self):
        if self.bomberman.rect.x <= int((self.bomberman.rect.x - (
                self.bomberman.rect.x % 50)) // 50) * 50 + 25:
            return True

        if self.bomberman.rect.x > int((self.bomberman.rect.x - (
                self.bomberman.rect.x % 50)) // 50) * 50 + 25:
            return False

    def bomb_place_y(self):
        if self.bomberman.rect.y < int(((self.bomberman.rect.y - 75 - (
                (self.bomberman.rect.y - 75) % 50)) // 50) * 50 + 75) + 25:
            return True

        if self.bomberman.rect.y >= int(((self.bomberman.rect.y - 75 - (
                (self.bomberman.rect.y - 75) % 50)) // 50) * 50 + 75) + 25:
            return False

    def generate_fires(self, x, y):
        if len(self.fires) == 0:
            self.fires.append(FireMiddle(x, y))
        can_generate = True
        for i in range(self.bomberman.long_fire):
            if can_generate:
                self.fires.append(FireHorizontal(x + 50 * i, y))
                can_generate = self.check_fire_gen()
                if not can_generate:
                    self.fires.pop()
                    self.fires.pop()
                    self.fires.append(FireHorizontal(x, y + 50 * (i - 1)))

        can_generate = True
        for i in range(self.bomberman.long_fire):
            if can_generate:
                self.fires.append(FireVertical(x, y + 50 * i))
                can_generate = self.check_fire_gen()
                if not can_generate:
                    self.fires.pop()
                    self.fires.pop()
                    self.fires.append(FireVertical(x, y + 50 * (i - 1)))

        can_generate = True
        for i in range(self.bomberman.long_fire):
            if can_generate:
                self.fires.append(FireHorizontal(x - 50 * i, y))
                can_generate = self.check_fire_gen()
                if not can_generate:
                    self.fires.pop()
                    self.fires.pop()
                    self.fires.append(FireHorizontal(x - 50 * (i - 1), y))

        can_generate = True
        for i in range(self.bomberman.long_fire):
            if can_generate:
                self.fires.append(FireVertical(x, y - 50 * i))
                can_generate = self.check_fire_gen()
                if not can_generate:
                    self.fires.pop()
                    self.fires.pop()
                    self.fires.append(FireVertical(x, y - 50 * (i - 1)))

    def check_fire_gen(self):
        for i in self.fires:
            for obj in self.area.objects:
                if obj.type == 'Block' and obj.rect.colliderect(i):
                    print("COLLIDE")
                    return False
        return True

    def play_sounds(self):
        if self.is_pressed_left or self.is_pressed_right:
            self.sounds[0].play()

    def process_logic_sounds(self):
        for sound in self.sounds:
            sound.process_logic()

    def main_loop(self):
        self.music.play()
        while not self.game_over:
            self.process_event()
            # self.sound_l.stop_sound(self.is_pressed_left)
            self.process_collisions()
            self.process_move()
            self.process_draw()
            self.process_logic_bombs()
            self.process_logic_fires()

            self.play_sounds()
            self.process_logic_sounds()

            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()


        # file = 'sounds/theme_6.ogg'
        # pygame.mixer.init()
        # pygame.mixer.music.load(file)
        # pygame.mixer.music.set_volume(0.25)
        # pygame.mixer.music.play(-1)