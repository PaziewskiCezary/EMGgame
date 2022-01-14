import pygame
import os
import math
import time
import pickle
import pygame_textinput
import numpy as np

import utils as utils
from button import Button
from projectile import Projectile
from target import Target

from games import AbstractGame

MOVE_LEFT = -1
MOVE_RIGHT = 1
MOVE_DOWN = 0
NUMBER_OF_MUSCLE_TENSION_SAMPLES = 256


class SimpleGame(AbstractGame):
    """Simple_Game"""

    def __init__(self, queue, lock, sample_array, size, use_keyboard=False, lives=3, name='', full_screen=True):

        self.__queue = queue
        self.__lock = lock
        self.__sample_array = sample_array

        self.__use_keyboard = use_keyboard
        self.__default_name = name
        self.__full_screen = full_screen
        pygame.init()

        self.__yellow_rgb = (255, 239, 148)
        self.__pink_rgb = (232, 98, 203)
        self.__background_colour = self.__yellow_rgb
        self.__text_colour = self.__pink_rgb
        self.__button_colour = self.__pink_rgb
        self.__button_text_colour = self.__yellow_rgb
        self.__screen_size = size
        self.__x_screen, self.__y_screen = self.__screen_size
        self.__max_lives = lives

        if self.__full_screen:
            display_info = pygame.display.Info()
            auto_screen_resolution = (display_info.current_w, display_info.current_h)
            self.__screen = pygame.display.set_mode(auto_screen_resolution, pygame.FULLSCREEN)
            self.__x_screen = self.__screen.get_width()
            self.__y_screen = self.__screen.get_height()
            self.__screen_size = (self.__x_screen, self.__y_screen)

        else:
            self.__screen = pygame.display.set_mode(self.__screen_size)

        self.__screen.fill(self.__background_colour)

        pygame.display.flip()

        self.__clock = pygame.time.Clock()

        self.__font_style = 'DejaVu Sans Mono'
        self.__font_size = 30

        self.__max_shift = 10

        self.__backgrounds = sorted([x for x in utils.get_backgrounds()])
        self.__backgrounds = [pygame.image.load(x) for x in self.__backgrounds]

        self.__bins = [Target(desired_width=self.__x_screen * Target.percentage, img_path=bin_path,
                              bin_type=bin_type) for (bin_type, bin_path) in utils.get_targets()]

        self.__trashes = []
        for i, (trash_type, trash_path) in enumerate(utils.get_projectiles()):
            trash = Projectile(desired_width=self.__x_screen * Projectile.percentage, img_path=trash_path, projectile_type=trash_type)

            self.__trashes.append(trash)

    def __kill(self):
        self.__queue.put(1)
        pygame.quit()
        exit()

    @property
    def use_keyboard(self):
        return self.__use_keyboard

    def __move_projectile(self, shift):
        if not self.__trash:
            raise ValueError('self.__thrash not set')
        if abs(shift) > 1:
            raise ValueError('arg must be between -1 and 1')

        self.__trash.x_position += self.__max_shift * shift

    def __muscle_move(self, muscle_tension):

        calibration_difference = self.__calibrate_value_max - self.__calibrate_value_min
        number_of_movement_interval = 3
        movement_interval = calibration_difference / number_of_movement_interval
        second_movement_interval = 2 * movement_interval
        third_movement_interval = 3 * movement_interval

        if muscle_tension <= self.__calibrate_value_min:
            return MOVE_LEFT
        elif muscle_tension >= self.__calibrate_value_max:
            return MOVE_RIGHT
        else:
            actual_muscle_tension = muscle_tension - self.__calibrate_value_min
            if actual_muscle_tension <= movement_interval:
                return (actual_muscle_tension - movement_interval) / movement_interval
            elif movement_interval < actual_muscle_tension <= second_movement_interval:
                return MOVE_DOWN
            elif second_movement_interval < actual_muscle_tension <= third_movement_interval:
                return (actual_muscle_tension - second_movement_interval) / movement_interval

    @staticmethod
    def __update():
        pygame.display.update()

    def __get_calib_samples(self):

        calibration_time = 5
        quit_time = 0.5
        samples = []
        start_time_calibration_min = time.time()

        while time.time() - start_time_calibration_min <= calibration_time:
            self.__lock.acquire()
            signal = self.__sample_array[-NUMBER_OF_MUSCLE_TENSION_SAMPLES:]
            signal -= np.mean(signal)
            signal = np.abs(signal)
            self.__lock.release()
            samples.append(signal)
            start_quit_time = time.time()
            while time.time() - start_quit_time <= quit_time:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__kill()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self._menu()

        samples_mean = np.mean(samples)
        del samples
        return samples_mean

    def __check_calib(self, text_x_position, text_y_position, font_size):

        minimum_difference_between_calibration_values = 50

        if self.__calibrate_value_min >= self.__calibrate_value_max or \
                self.__calibrate_value_max - self.__calibrate_value_min < minimum_difference_between_calibration_values:
            self.__screen.fill(self.__background_colour)
            self.__text('POWTARZAM KALIBRACJĘ', text_x_position, text_y_position, font_size=font_size)
            self.__update()
            time.sleep(2)
            self.__calibrate()

    def __calibrate(self):

        text_x_position = self.__x_screen // 2
        text_y_position = self.__y_screen // 2
        font_size = self.__y_screen // 10

        self.__screen.fill(self.__background_colour)
        pygame.display.set_caption('Kalibracja')
        self.__update()

        self.__screen.fill(self.__background_colour)
        self.__text('KALIBRACJA', text_x_position, text_y_position, font_size=font_size)
        self.__update()
        time.sleep(2)

        self.__screen.fill(self.__background_colour)
        self.__text('ROZLUŹNIJ RĘKĘ', text_x_position, text_y_position, font_size=font_size)
        self.__update()
        time.sleep(1)

        self.__calibrate_value_min = self.__get_calib_samples()

        time.sleep(2)

        self.__screen.fill(self.__background_colour)
        self.__text('ZACIŚNIJ RĘKĘ', text_x_position, text_y_position, font_size=font_size)
        self.__update()

        time.sleep(1)

        self.__calibrate_value_max = self.__get_calib_samples()
        self.__check_calib(text_x_position, text_y_position, font_size)
        self.__screen.fill(self.__background_colour)
        self.__text('KONIEC KALIBRACJI', text_x_position, text_y_position, font_size=font_size)
        self.__update()

    def __get_name(self):

        input_name = pygame_textinput.TextInput(font_family=self.__font_style, font_size=self.__y_screen // 13,
                                                text_color=self.__text_colour, max_string_length=15)

        clock = pygame.time.Clock()

        is_input = True
        while is_input:
            self.__screen.fill(self.__background_colour)
            self.__text("PODAJ SWÓJ NICK:", self.__x_screen // 2, self.__y_screen // 4, font_size=self.__y_screen // 13)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.__kill()

            input_name.update(events)
            text_length = input_name.font_object.size(input_name.get_text())[0]
            self.__screen.blit(input_name.get_surface(),
                               ((self.__x_screen - text_length) // 2, self.__y_screen // 2))

            self.__update()
            clock.tick(30)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.__name = input_name.get_text()
                        is_input = False
                        break

    def __text(self, caption, x_position, y_position, *, font_style='DejaVu Sans Mono', font_size=30,
               rectangle_color=None):

        font = pygame.font.SysFont(font_style, font_size)
        text = font.render(caption, True, self.__text_colour)

        text_rect = text.get_rect()
        if rectangle_color:
            pygame.draw.rect(self.__screen, rectangle_color, text_rect, True)

        text_rect.center = (x_position, y_position)
        self.__screen.blit(text, text_rect)

    def __start(self):
        if self.__default_name:
            self.__name = self.__default_name
        else:
            self.__get_name()

        if not self.__use_keyboard:
            self.__calibrate()

        self.__play()

    def __show_score(self):

        try:
            scores = pickle.load(open("../wyniki.pkl", "rb"))
        except FileNotFoundError:
            scores = []

        # sorting scores with keeping indexes
        index = range(len(scores))
        scores, index = zip(*reversed(sorted(zip(scores, index), key=lambda x: x[0][0])))
        
        place = np.argmax(index) + 1
        # play = False

        self.__screen.fill(self.__background_colour)
        self.__update()
        x_button, y_button = self.__x_screen // 20, self.__y_screen // 20
        button_font_size = self.__y_screen // 18
        title_font_size = self.__y_screen // 12
        subtitle_font_size = self.__y_screen // 14
        points_font_size = self.__y_screen // 16

        return_btn = Button(self.__screen, 'Menu', (x_button, y_button), (x_button * 2, y_button * 2),
                            button_color=self.__button_colour, label_color=self.__button_text_colour, func=self._menu,
                            font_size=button_font_size)
        again_btn = Button(self.__screen, 'Zagraj jeszcze raz!', (self.__x_screen // 2, 7 * self.__y_screen // 8),
                           (x_button * 7, y_button * 3),
                           button_color=self.__button_colour, label_color=self.__button_text_colour, func=self.__play,
                           font_size=button_font_size)

        self.__text('WYNIK', self.__x_screen // 2, self.__y_screen // 4, font_size=title_font_size)
        self.__text('Punkty', 3 * self.__x_screen // 4, self.__y_screen // 2, font_size=subtitle_font_size)
        self.__text('Imię', 2 * self.__x_screen // 4, self.__y_screen // 2, font_size=subtitle_font_size)
        self.__text('Pozycja', self.__x_screen // 4, self.__y_screen // 2, font_size=subtitle_font_size)

        self.__update()
        time.sleep(1)

        self.__text(str(self.__score), 3 * self.__x_screen // 4, self.__y_screen // 2 + 100, font_size=points_font_size)
        self.__update()
        time.sleep(1)

        self.__text(self.__name, 2 * self.__x_screen // 4, self.__y_screen // 2 + 100, font_size=points_font_size)
        self.__update()
        time.sleep(1)

        self.__text(f' {str(place) if place < 10 else str(place)}.', self.__x_screen // 4, self.__y_screen // 2 + 100,
                    font_size=points_font_size)
        self.__update()

        return return_btn, again_btn

    def __make_health_text(self):

        font_size = self.__y_screen // 24
        font_size_heart = self.__y_screen // 20
        score_text = "Punkty: " + str(self.__score)
        lives_text = "Życia: "
        heart_text = u"♥"
        width_heart, height_heart = pygame.font.SysFont(self.__font_style, font_size_heart).size(heart_text)
        width_score, _ = pygame.font.SysFont(self.__font_style, font_size).size(score_text)
        width_lives, _ = pygame.font.SysFont(self.__font_style, font_size).size(lives_text)
        # 'DejaVu Sans Mono'
        pygame.draw.rect(self.__screen, self.__background_colour,
                         (0, 0, self.__x_screen, self.__y_screen // 14), False)
        self.__text(score_text, width_score / 2, 25, font_style=self.__font_style, font_size=font_size)
        self.__text(lives_text, self.__x_screen//2, 25, font_style=self.__font_style, font_size=font_size)
        self.__text(heart_text * self.__lives, self.__x_screen//2 + width_lives//2 + 0.5 * self.__lives * width_heart,
                    25, font_style=self.__font_style, font_size=font_size_heart)

        self.__update()

    def __what_next(self):

        return_btn, again_btn = self.__show_score()
        while True:
            for event in pygame.event.get():
                return_btn.on_click(event)
                again_btn.on_click(event)
                if event.type == pygame.QUIT:
                    self.__kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._menu()

    def __set_targets(self):

        number_of_bins = len(self.__bins)

        offset = (1 - number_of_bins * Target.percentage) / (number_of_bins + 1)
        offset = round(self.__x_screen * offset)

        first_bin = 0

        bin_width, bin_height = self.__bins[first_bin].size

        bin_y_position = self.__y_screen - bin_height

        for number_of_bin, bin_ in enumerate(self.__bins):
            bin_x_position = bin_width * number_of_bin
            bin_x_position += offset * (number_of_bin + 1)
            bin_.x_position = bin_x_position   
            bin_.y_position = bin_y_position

        return bin_y_position

    def __play(self):

        self.__lives = self.__max_lives
        self.__score = 0
        self.__missed = 0

        self.__bgn_idx = 0
        speed_rate = 0.0003
        trash_number = 0

        bin_y_position = self.__set_targets()
        np.random.shuffle(self.__trashes)

        play = True
        new_trash = True
        actual_trash = None
        self.__update_background()

        while self.__trashes and play and self.__lives > 0:
            if new_trash:
                self.__trash = self.__trashes.pop()
                trash_number += 1

                # recalculate x to be in center
                self.__trash.x_position = self.__x_screen // 2 - self.__trash.size[1] // 2    
                self.__trash.y_position = 100                                                 
                new_trash = False
                actual_trash = True

            if not self.__lives:
                play = False

            while actual_trash:
                break_loop = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__kill()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            play = False
                            break_loop = True

                        if event.key == pygame.K_LEFT:
                            self.__move_projectile(MOVE_LEFT)

                        if event.key == pygame.K_RIGHT:
                            self.__move_projectile(MOVE_RIGHT)

                        if event.key == pygame.K_DOWN:
                            self.__trash.y_position += 10
                if break_loop:
                    break

                if not self.__use_keyboard:
                    self.__lock.acquire()
                    signal = self.__sample_array[-NUMBER_OF_MUSCLE_TENSION_SAMPLES:]
                    signal -= np.mean(signal)
                    signal = np.abs(signal)
                    self.__lock.release()
                    move_value = self.__muscle_move(np.mean(signal)) / 10   # comm why 10?
                    self.__move_projectile(move_value)
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                play = False
                                break_loop = True

                            if event.key == pygame.K_LEFT:
                                self.__move_projectile(MOVE_LEFT)

                            if event.key == pygame.K_RIGHT:
                                self.__move_projectile(MOVE_RIGHT)

                if break_loop:
                    break

                trash_x_position, trash_y_position = self.__trash.get_position   

                acceleration = 1.02 ** trash_number

                y_step = self.__y_screen * speed_rate * acceleration  
                self.__trash.x_position, self.__trash.y_position = trash_x_position, trash_y_position + y_step
                if self.__trash.bottom > bin_y_position:
                    collision = False
                    for (i, bin_) in enumerate(self.__bins):

                        if utils.collide_in(self.__trash, bin_):
                            collision = True
                            if bin_.type == self.__trash.type:
                                self.__score += 100

                            else:
                                self.__score += -10
                                self.__missed += 1
                                     
                    if not collision:
                        self.__lives -= 1

                    new_trash = True
                    actual_trash = False

                # showing bins
                self.__screen.fill(self.__background_colour)
                self.__update_background()

                for bin_ in self.__bins:
                    self.__screen.blit(bin_.image, bin_.get_position)
                self.__screen.blit(self.__trash.image, self.__trash.get_position)

                # labels with lives and score
                self.__make_health_text()

                self.__clock.tick(60)

        self.__score = self.__score
        self.__save_score()

        self.__what_next()
        
    def __update_background(self):

        idx = math.log2(self.__max_lives - self.__lives + self.__missed + 1)
        idx = int(idx)

        idx = min(idx, len(self.__backgrounds) - 1)

        img = self.__backgrounds[idx]
        self.__screen.blit(img, [0, 0])

    def __save_score(self):
        if not os.path.isfile("../wyniki.pkl"):
            scores = []
            pickle.dump(scores, open("../wyniki.pkl", "wb"))

        scores = pickle.load(open("../wyniki.pkl", "rb"))
        scores.append((self.__score, self.__name))
        pickle.dump(scores, open("../wyniki.pkl", "wb"))

    def __scores(self):
        try:
            scores = pickle.load(open("../wyniki.pkl", "rb"))

        except FileNotFoundError:
            scores = []

        # sorting scores with keeping indexes
        index = range(len(scores))
        try:
            scores, index = zip(*reversed(sorted(zip(scores, index), key=lambda x: x[0][0])))
        except ValueError:
            scores, index = ['brak wyników'], [0]

        self.__screen.fill(self.__background_colour)
        self.__update()
        x_button, y_button = self.__x_screen // 20, self.__y_screen // 20
        button_font_size = self.__y_screen // 18
        return_btn = Button(self.__screen, 'Wróć', (x_button, y_button), (x_button * 2, y_button * 2),
                            button_color=self.__button_colour, label_color=self.__button_text_colour, func=self._menu,
                            font_size=button_font_size)
        self.__text('WYNIKI', self.__x_screen // 2, self.__y_screen // 10 - 25, font_size=48)
        y_offset = 55
        for i in range(min(len(scores), 10)):
            self.__text(f'{" " + str(i + 1) if i < 10 else str(i + 1)}.', self.__x_screen // 4,
                        self.__y_screen // 10 + (i + 1) * y_offset)
            self.__text(str(scores[i][1]), 2 * self.__x_screen // 4, self.__y_screen // 10 + (i + 1) * y_offset)
            self.__text(str(scores[i][0]), 3 * self.__x_screen // 4, self.__y_screen // 10 + (i + 1) * y_offset)
            time.sleep(0.1)
            self.__update()
        self.__update()
        while True:
            for event in pygame.event.get():
                return_btn.on_click(event)
                if event.type == pygame.QUIT:
                    self.__kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._menu()

    def _menu(self):

        self.__screen.fill(self.__background_colour)

        pygame.display.set_caption('Segreguj smieci')

        x_button = self.__x_screen / 4
        y_button = self.__y_screen / 5
        font_size = int(x_button // 5)

        b_s = Button(self.__screen, 'Start', (self.__x_screen / 2, self.__y_screen / 2 - 1.5 * y_button),
                     (x_button, y_button), self.__button_colour, self.__button_text_colour, self.__start,
                     font_size=font_size)
        b_w = Button(self.__screen, 'Wyniki', (self.__x_screen / 2, self.__y_screen / 2), (x_button, y_button),
                     self.__button_colour, self.__button_text_colour, self.__scores, font_size=font_size)
        b_e = Button(self.__screen, 'Wyjdź', (self.__x_screen / 2, self.__y_screen / 2 + 1.5 * y_button),
                     (x_button, y_button), self.__button_colour, self.__button_text_colour, self.__kill,
                     font_size=font_size)

        self.__update()
        while True:
            for event in pygame.event.get():
                b_s.on_click(event)
                b_w.on_click(event)
                b_e.on_click(event)
                if event.type == pygame.QUIT:
                    self.__kill()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__kill()
