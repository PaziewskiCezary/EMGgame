import pygame
import os
import math
import time
import sys
import pickle
import pygame_textinput

from scipy.signal import butter, lfilter, iirnotch, lfilter_zi, filtfilt
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss

from utils import *

def debug():
    import ipdb; ipdb.set_trace()

class Simple_Game(object):
    """dSimple_Game"""
    def __init__(self, lock, sample_array, size, use_keyboard=False, lifes=3, 
                 default_name='', full_screen=True):

        self.lock = lock
        self.sample_array = sample_array

        self._use_keyboard = use_keyboard
        self.default_name = default_name
        self.full_screen = full_screen
        pygame.init()

        # if not self.use_keyboard:
            # try:
                # self.amp = Amplifier(512, [0, 1])
            # except ValueError as e:
                # print(e)
                # exit(1)

        self.bgcolour = (255,239,148) #żółte
        self.text_colour = (232,98,203) #różowy
        self.button_colour = (232,98,203) #różowy
        self.button_text_colour = (255,239,148) #żółte
        self.size = size
        self.x_screen, self.y_screen = self.size
        self.max_lifes = lifes
        #self.max_missed = 1   #chyba nie potrzebne 
        
        if self.full_screen:
            self.screen = pygame.display.set_mode((0,0),  pygame.FULLSCREEN)  #do przemyślenienia ,pygame.RESIZABLE)
            self.x_screen = self.screen.get_width()
            self.y_screen = self.screen.get_height()
            self.size = (self.x_screen, self.y_screen)

        else:
            self.screen = pygame.display.set_mode(self.size)

        self.screen.fill(self.bgcolour)

        pygame.display.flip()

        self.clock = pygame.time.Clock()

        self.font_style = 'Teko'
        self.font_size = 30

        self.backgrounds = sorted([x for x in get_backgrounds()])
        self.backgrounds = [pygame.image.load(x) for x in 	self.backgrounds]
        self.max_shift = 10

    @property
    def use_keyboard(self):
        return self._use_keyboard

    def move_thrash(self, arg):
        if not self.trash:
            raise ValueError('self.thrash not set')
        if abs(arg) > 1:
            raise ValueError('arg must be between -1 and 1')
        self.trash.x += self.max_shift * arg

    def muscle_move(self, x):

        d = self.calib_max - self.calib_min
        d /= 3
        
        if x <= self.calib_min:
            return -1
        elif x >= self.calib_max:
            return 1
        else:
            s = x - self.calib_min
            if s <= d:
                return - ( 1 - min(s/d,1) )
            elif d < s <= 2 * d:
                return 0
            elif d * 2 < s <= 3 * d:
	            return  min((s - d * 2)/d, 1)

    def update(self):
        pygame.display.update()

    def calibrate(self):
        
        self.screen.fill(self.bgcolour)
        pygame.display.set_caption('Kalibracja') 
        self.update()
  
        self.screen.fill(self.bgcolour)
        self.text('KALIBRACJA', self.x_screen // 2, self.y_screen // 2)
        self.update()
        time.sleep(2)
        

        self.screen.fill(self.bgcolour)
        self.text('ROZLUŹNIJ RĘKĘ', self.x_screen // 2, self.y_screen // 2)
        self.update()
        time.sleep(1)
        
        czas_kalibracji = 5
        samples = []
        t = time.time()
        while time.time() - t <= czas_kalibracji:
            self.lock.acquire()
            signal = self.sample_array[-256:]
            signal -= np.mean(signal)
            signal = np.abs(signal)
            self.lock.release()
            samples.append(signal)
            t0 = time.time()
            while time.time() - t0 <= 0.5:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit();
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.menu()
              

        self.calib_min = np.mean(samples)
        del samples
        
        time.sleep(2)
        
        self.screen.fill(self.bgcolour)
        self.text('ZACIŚNIJ RĘKĘ', self.x_screen // 2, self.y_screen // 2)
        self.update()

        time.sleep(1)
        
        samples = []
        t = time.time()
        while time.time() - t <= czas_kalibracji:
            self.lock.acquire()
            signal = self.sample_array[-256:]
            signal -= np.mean(signal)
            signal = np.abs(signal)
            self.lock.release()
            samples.append(signal) 
            t0 = time.time()
            while time.time() - t0 <= 0.5:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit();
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.menu()
            
        self.calib_max = np.mean(samples)
        print(len(samples))
        del samples
        print(self.calib_min, self.calib_max)

        # self.calib_max = 400
        if self.calib_min >= self.calib_max or  self.calib_max - self.calib_min < 50:
            self.screen.fill(self.bgcolour)
            self.text('POWTORZAM KALIBRACJĘ', self.x_screen // 2, self.y_screen // 2)
            self.update() 
            time.sleep(2)
            self.calibrate()

        self.screen.fill(self.bgcolour)
        self.text('KONIEC KALIBRACJI', self.x_screen // 2, self.y_screen // 2) 
        self.update()

    def get_name(self):
        
        textinput = pygame_textinput.TextInput()

        textinput.text_color = self.text_colour
        
        clock = pygame.time.Clock()


        #font = pygame.font.Font('freesansbold.ttf', 32) 
        font = pygame.font.SysFont(self.font_style, self.font_size)
        text = font.render("PODAJ SWÓJ NICK:", True, self.text_colour) 
        
        is_input = True
        while is_input:
            self.screen.fill(self.bgcolour)
            textRect = text.get_rect()  
            textRect.center = (self.x_screen // 2, self.y_screen // 4) 
            self.screen.blit(text, textRect)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
	        
            textinput.update(events)
            a = textinput.font_object.size(textinput.get_text())
            self.screen.blit(textinput.get_surface(), 
                             ((self.x_screen - a[0]) // 2 , self.y_screen // 2))

            self.update()
            clock.tick(30)
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.name = textinput.get_text()
                        is_input = False
                        break
    

    def text(self, napis, x_pos, y_pos, *, text='Amatic SC', font_size=30, rectangle_color = None):  #'DejaVu Sans Mono'

        font = pygame.font.SysFont(text, font_size)
        text = font.render(napis, True, self.text_colour) 

        textRect = text.get_rect()  
        if rectangle_color:
            pygame.draw.rect(self.screen, rectangle_color, textRect, True)

        textRect.center = (x_pos, y_pos) 
        self.screen.blit(text, textRect)

    def main_loop(self):
        if not self.use_keyboard:
            self.get_name()
        elif self.default_name:
            self.name = self.default_name
        else:
            self.name = input('Podaj imię: ')

        if not self.use_keyboard:
            self.calibrate()

        self.play()
        
    def play(self):
        # if not self.use_keyboard:
            # self.amp.amp.start_sampling()        
            # time.sleep(1)	
        
        self.lifes = self.max_lifes
        self.score = 0 
        self.missed = 0 
        self.backgrounds = sorted([x for x in get_backgrounds()])
        self.backgrounds = [pygame.image.load(x) for x in 	self.backgrounds]
        self.bgn_idx = 0
        speed_rate = 0.0003 if not self.use_keyboard else 0.0003
        trash_number = 0

        bins = [TrashBin(width=self.x_screen*TrashBin.precent, img_path=path, type=type) for (type, path) in get_bins()]

        number_of_bins = len(bins)
        bin_widht = self.x_screen * bins[0].precent

        offset = ( 1 - number_of_bins * TrashBin.precent ) / ( number_of_bins + 1 )
        offset = round( self.x_screen * offset )

        bin_w, bin_h = bin_size = bins[0].size

        pos_y = self.y_screen - bin_h

        for i, bin_ in enumerate(bins):
            pos_x = bin_w * i
            pos_x += offset * (i + 1)
            bin_.x = pos_x
            bin_.y = pos_y

        trashes = []
        for i, (type, path) in enumerate(get_trashes()):
            t = Trash(width=self.x_screen*Trash.precent, img_path=path, type=type)
            trashes.append(t)

        np.random.shuffle(trashes)

        play = True
        new_trash = True
        self.update_background()

        while trashes and play and self.lifes > 0:
            if new_trash:
                self.trash = trashes.pop()
                trash_number += 1
                # recalcualte x to be in center
                self.trash.x = self.x_screen//2 - self.trash.size[1]//2
                self.trash.y = 100
                new_trash = False
                this_trash = True

            if not self.lifes:
                play = False

            while this_trash:
                break_loop = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            play = False
                            break_loop = True

                        if event.key == pygame.K_LEFT:
                            self.move_thrash(-1)

                        if event.key == pygame.K_RIGHT:
                            self.move_thrash(1)
                        if event.key == pygame.K_DOWN:
                            self.trash.y += 10
                if break_loop:
                    break
                #exit_btn = Button(self.screen, 'Koniec', (200 , 200), (100, 200), (0xff, 0xff, 0xff), (0,0,0) , self.menu) #czy to jest używane?????
                
                if not self.use_keyboard:
                    #signal = self.amp.get_signal(self.amp.fs//3)
                    self.lock.acquire()
                    signal = self.sample_array[-256:]
                    signal -= np.mean(signal)
                    signal = np.abs(signal)
                    self.lock.release()
                    move_value = self.muscle_move(np.mean(signal)) / 10
                    self.move_thrash(move_value)
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                play = False
                                break_loop = True

                            if event.key == pygame.K_LEFT:
                                self.move_thrash(-1)

                            if event.key == pygame.K_RIGHT:
                                self.move_thrash(1) 
                if break_loop:
                    break

                trash_x, trash_y = self.trash.pos 

                translation_y = self.x_screen * speed_rate * 1.02 ** trash_number
                self.trash.x, self.trash.y = trash_x, trash_y +  translation_y


                if self.trash.bottom > pos_y:
                    collsion = False
                    for (i, bin_) in enumerate(bins):

                        if collide_in(self.trash, bin_):

                            if bin_.type == self.trash.type:

                                self.score += 100
                                collsion = True
                            else:
                                self.score += -10   
                                collsion = True
                                self.missed += 1
                            
                    if not collsion:   
                        self.lifes -= 1

                    new_trash = True
                    this_trash = False


                # showing bins
                self.screen.fill(self.bgcolour)
                self.update_background()
                for bin_ in bins:
                    self.screen.blit(bin_.image, bin_.pos)
                self.screen.blit(self.trash.image, self.trash.pos)


                # labes with lives and score
                font_size = 25
                font_size_s = 40
                wh, hh = pygame.font.SysFont(self.font_style, font_size_s).size('❤')  #'DejaVu Sans Mono'
                pygame.draw.rect(self.screen, self.bgcolour, (0, 0, self.x_screen, 50), False)
                self.text("Punkty: "+str(self.score), 100, 25, text=self.font_style, font_size = font_size) 
                self.text('Życia: ', 200 + len("Punkty: "+str(self.score))*font_size, 25, text=self.font_style, font_size = font_size) 
                self.text('❤'*self.lifes, 65 + 0.5 * self.lifes * wh + len("Punkty: "+str(self.score))*font_size + len("Życia: ")*font_size, 25, text=self.font_style, font_size = font_size_s)
               
                self.update()

                self.clock.tick(60)
        

        # if not self.use_keyboard:
            # self.amp.amp.stop_sampling()

        self.score = max(0, self.score)
        self.save_score()

        # show score
        try:
            scores = pickle.load( open( "wyniki.pkl", "rb" ) )
            
        except FileNotFoundError:
            scores = []

        # sorting scores with keeping indexes
        index = range(len(scores))
        scores, index = zip(*reversed(sorted(zip(scores, index), key=lambda x : x[0][0])))

        place = np.argmax(index) + 1
        play = False

        self.screen.fill(self.bgcolour)
        self.update()
        x_button, y_button = 60, 30

        return_btn = Button(self.screen, 'Menu', (x_button, y_button), (x_button*2, y_button*2), 
                            button_color=self.button_colour, label_color=self.button_text_colour, func=self.menu, font_size = 25)
        again_btn = Button(self.screen, 'Zagraj jeszcze raz!', (self.x_screen // 2, 7 * self.y_screen // 8), (x_button*7, y_button*3), 
                            button_color=self.button_colour, label_color=self.button_text_colour, func=self.play, font_size = 25)
                  
        self.text('WYNIK',    self.x_screen // 2, self.y_screen // 4, font_size=64)
        self.text('Punkty', 3*self.x_screen // 4, self.y_screen // 2 )
        self.text('Imię',   2*self.x_screen // 4, self.y_screen // 2 )
        self.text('Pozycja',  self.x_screen // 4, self.y_screen // 2 )

        self.update()
        time.sleep(1)  

        self.text(str(self.score), 3*self.x_screen // 4, self.y_screen // 2 + 100 )
        self.update()
        time.sleep(1)
        
        self.text(self.name, 2*self.x_screen // 4, self.y_screen // 2 + 100)
        self.update() 
        time.sleep(1)  
        
        self.text(f' {str(place) if place<10 else str(place)}.', self.x_screen // 4, self.y_screen // 2 + 100 )
        self.update()

        while True:
            for event in pygame.event.get():
                return_btn.onClick(event)
                again_btn.onClick(event)
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit();
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu()


    def update_background(self):
        
        idx = math.log2(self.max_lifes - self.lifes + self.missed + 1)
        idx = int(idx)

        idx = min(idx, len(self.backgrounds)-1)

        img = self.backgrounds[idx]
        self.screen.blit(img,[0,0])
    
    @property
    def can_stear(self, obj):
        if self.allow_stearing:
            pass

    def save_score(self):
        if not os.path.isfile("wyniki.pkl"):
            scores = []
            pickle.dump( scores, open( "wyniki.pkl", "wb" ) )

        scores = pickle.load( open( "wyniki.pkl", "rb" ) )
        scores.append((self.score, self.name))
        pickle.dump( scores, open( "wyniki.pkl", "wb" ) )

    def scores(self):
        try:
            scores = pickle.load( open( "wyniki.pkl", "rb" ) )
            
        except FileNotFoundError:
            scores = []

        # sorting scores with keeping indexes
        index = range(len(scores))
        scores, index = zip(*reversed(sorted(zip(scores, index), key=lambda x : x[0][0])))

        self.screen.fill(self.bgcolour)
        self.update()
        x_button ,y_button = 60, 30
        return_btn = Button(self.screen, 'Wróć', (x_button, y_button), (x_button*2, y_button*2), 
                            button_color=self.button_colour, label_color=self.button_text_colour, func=self.menu, font_size = 25)
        self.text('WYNIKI', self.x_screen // 2, self.y_screen // 10  - 25, font_size = 48)
        y_offset = 55
        for i in range(min(len(scores), 10)):
            self.text(f'{" " + str(i+1) if i<10 else str(i+1)}.', self.x_screen // 4, self.y_screen // 10 + (i+1)*y_offset)
            self.text(str(scores[i][1]), 2*self.x_screen // 4, self.y_screen // 10 + (i+1)*y_offset)
            self.text(str(scores[i][0]), 3*self.x_screen // 4, self.y_screen // 10 + (i+1)*y_offset)
            time.sleep(0.1)        
            self.update()
        while True:
            for event in pygame.event.get():
                return_btn.onClick(event)
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit();
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu()

        del scores 
        del index

    def menu(self):
        
        self.screen.fill(self.bgcolour)
        
        pygame.display.set_caption('Segreguj smieci')

        x_button = self.x_screen/4
        y_button = self.y_screen/5
        font_size = int(x_button//4)
        
        b_s = Button(self.screen, 'Start', (self.x_screen/2,self.y_screen/2-1.5*y_button), (x_button, y_button), self.button_colour, self.button_text_colour, self.main_loop, font_size = font_size)
        b_w = Button(self.screen, 'Wyniki', (self.x_screen/2,self.y_screen/2), (x_button, y_button), self.button_colour, self.button_text_colour, self.scores, font_size = font_size)
        b_e = Button(self.screen, 'Wyjdź', (self.x_screen/2,self.y_screen/2+1.5*y_button), (x_button, y_button), self.button_colour, self.button_text_colour, pygame.quit, font_size = font_size)
 
        self.update()
        while True:
            for event in pygame.event.get():
                b_s.onClick(event)
                b_w.onClick(event)
                b_e.onClick(event)
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit();
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit();

        return False


class Button(object):
    def __init__(self, screen, label, pos, dims, button_color, label_color, func, font_size):
        
        self.screen = screen
        self.label = label
        self.pos = pos
        self.dims = dims
        self.button_color = button_color
        self.label_color = label_color
        self.font = pygame.font.SysFont('Teko', font_size)
        self.func = func
        
        self.addRect()
        self.addText()


    def addRect(self):
        pos_x, pos_y = self.pos
        weight, height = self.dims
        self.rect = pygame.draw.rect(self.screen, self.button_color, (pos_x-weight/2, pos_y-height/2, weight, height), 0)


    def addText(self):
        l = self.label
        pos_x, pos_y = self.pos
        weight, height = self.dims
        text_width, text_height = self.font.size(l)
        self.screen.blit(self.font.render(l, True, self.label_color), (pos_x-text_width/2, pos_y-text_height/2))
        
        
    def onClick(self, event):
        
        func = self.func

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position

            # checks if mouse position is over the button

            if self.rect.collidepoint(mouse_pos):
                func()
                
class Trash(pygame.sprite.Sprite):
    """docstring for Trash"""

    precent = 0.05

    def __init__(self, pos=(0, 0), *, img_path ,type, width):

        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = pygame.image.load(img_path).convert()
        self.image.set_colorkey((255,255,255))
        
        w, h = size = self.image.get_size()

        scale = width / w

        self.image = pygame.transform.scale(self.image, (int(size[0]*scale), int(size[1]*scale)))
        self.size = self.image.get_size()

        self.x, self.y = pos

    @property
    def pos(self):
        return self.x, self.y
    

    @property
    def bottom(self):
        return self.image.get_rect()[3] + self.pos[1]

    @property
    def top(self):
        return self.image.get_rect()[1] + self.pos[1]


    @property
    def corrners(self):
        w, h = self.size
        p1, p2 = (self.x, self.y), (self.x + w, self.y + h)
        return p1, p2

    def draw(self):
        pass
 
class TrashBin(pygame.sprite.Sprite):
    """docstring for Trash"""

    precent = 0.1

    def __init__(self, pos=(0, 0), img_path="static/trash.png", type=None, *, width):
        pygame.sprite.Sprite.__init__(self)
        
    
        self.type = type


        self.image = pygame.image.load(img_path).convert()
        self.image.set_colorkey((255,255,255))

        w, h = size = self.image.get_size()

        scale = width / w

        self.image = pygame.transform.scale(self.image, (int(size[0]*scale), int(size[1]*scale)))
        self.size = self.image.get_size()
        self.image.set_colorkey((173,170,218))

        self.x, self.y = pos

    @property
    def pos(self):
        return self.x, self.y


    @property
    def corrners(self):
        w, h = self.size
        p1, p2 = (self.x, self.y), (self.x + w, self.y + h)
        return p1, p2

    def draw(self):
        pass
        
    @property
    def bottom(self):
        return self.image.get_rect()[3] + self.pos[1]

    @property
    def top(self):
        return self.image.get_rect()[1] + self.pos[1]

class Amplifier(object):
    def __init__(self, Fs, channels):
        from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier
        if len(channels) != 2:
            raise ValueError("tylko2  kanały chcemy!!!!!!!!1111")
        amps = TmsiCppAmplifier.get_available_amplifiers('usb')
        if not amps:
            raise ValueError("Nie ma wzmacniacza")
			
        self.amp = TmsiCppAmplifier(amps[0])
        self.amp.sampling_rate = Fs
        self.gains = np.array(self.amp.current_description.channel_gains)
        self.offsets = np.array(self.amp.current_description.channel_offsets)
        self.channels = channels
        self.b1,self.self.a1 = butter(1,1/(Fs/2),'highpass')
        
    @property
    def fs(self):
        return self.amp.sampling_rate

    def samples(self,d,p = 100):
        '''Return array of signals in microvolts'''
        t = time.time()
        s = self.amp.get_samples(5*Fs).samples * self.gains + self.offsets
        s = s[:,self.channels[0]] - s[:,self.channels[1]]
        b,a = butter(2,1/(self.amp.sampling_rate/2),'highpass')
        s = filtfilt(b,a,s)
        s = s[-d:]
        if np.mean(s) > p:
            x = 1
        else:
            x = 0
            return s, x
	
    def calib(self, t=5, dt=512//3):
        
        czas_kalibracji = t
   
        
        l = czas_kalibracji
        self.amp.start_sampling()
        sample = []
        t = time.time()

        while time.time() - t <= czas_kalibracji:
            if np.round(time.time() - t,3) == (czas_kalibracji - l) and np.round(time.time() - t,3) < czas_kalibracji + 1:

                l -= 1
            sample.append(self.get_signal(dt))        
    	
        self.amp.stop_sampling()

        scim = np.mean(sample)
        return scim

    def get_signal(self, n):
        Fs = self.amp.sampling_rate
        
        s = self.amp.get_samples(int(n)).samples * self.gains + self.offsets
        
        s = s[:,self.channels[0]] - s[:,self.channels[1]]
        s-=np.mean(s)
        scim = np.mean(np.abs(s))
        return scim
