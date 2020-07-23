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
    def __init__(self, size, use_keyboard=False, lifes=3, 
                 default_name='', full_screen=True):

        self._use_keyboard = use_keyboard
        self.default_name = default_name
        self.full_screen = full_screen
        pygame.init()

        if not self.use_keyboard:
            try:
                from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier
                self.amp = Amplifier(512, [0, 1])
            except ValueError as e:
                print(e)
                exit(1)

        self.bgcolour = (232,98,203) 
        self.size = size
        self.max_lifes = lifes
        self.max_missed = 1
        if self.full_screen:
            self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.size)

        self.screen.fill(self.bgcolour)

        pygame.display.flip()

        self.clock = pygame.time.Clock()

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
        self.bgcolour = (255,239,148)
        x_screen, y_screen = self.size
        text_colour = (232,98,203)
        
        self.screen.fill(self.bgcolour)
        pygame.display.set_caption('Kalibracja') 
        self.update()
  
        self.screen.fill(self.bgcolour)
        self.text('KALIBRACJA', x_screen // 2, y_screen // 2)
        self.update()
        time.sleep(2)
        

        self.screen.fill(self.bgcolour)
        self.text('ROZLUŹNIJ RĘKĘ', x_screen // 2, y_screen // 2)
        self.update()
        time.sleep(1)
        self.calib_min = self.amp.calib()
        time.sleep(2)
        
        self.screen.fill(self.bgcolour)
        self.text('ZACIŚNIJ RĘKĘ', x_screen // 2, y_screen // 2)
        self.update()

        time.sleep(1)
        self.calib_max = self.amp.calib()
        # self.calib_max = 400
        if self.calib_min >= self.calib_max or  self.calib_max - self.calib_min < 50:
            self.screen.fill(self.bgcolour)
            self.text('POWTORZAM KALIBRACJĘ', x_screen // 2, y_screen // 2)
            self.update() 
            time.sleep(2)
            self.calibrate()

        self.screen.fill(self.bgcolour)
        self.text('KONIEC KALIBRACJI', x_screen // 2, y_screen // 2) 
        self.update()

    def get_name(self):
        
        self.bgcolour = (255,239,148)
        text_colour = (232,98,203)
	    
        textinput = pygame_textinput.TextInput()

        textinput.text_color = (232,98,203)
        
        self.screen = pygame.display.set_mode(self.size)
        clock = pygame.time.Clock()
        
        x_screen, y_screen = self.size


        font = pygame.font.Font('freesansbold.ttf', 32) 
        text = font.render("PODAJ SWÓJ NICK:", True, text_colour) 
        
        is_input = True
        while is_input:
            self.screen.fill(self.bgcolour)
            textRect = text.get_rect()  
            textRect.center = (x_screen // 2, y_screen // 4) 
            self.screen.blit(text, textRect)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
	        
            textinput.update(events)
            a = textinput.font_object.size(textinput.get_text())
            self.screen.blit(textinput.get_surface(), 
                             ((x_screen - a[0]) // 2 , y_screen // 2))

            self.update()
            clock.tick(30)
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.name = textinput.get_text()
                        is_input = False
                        break
    

    def text(self, napis, x_pos, y_pos, *, text='DejaVu Sans Mono', font_size=32, rectangle_color = None):
        x_screen, y_screen = self.size
        text_colour = (232,98,203)

        font = pygame.font.SysFont(text, font_size)
        text = font.render(napis, True, text_colour) 

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
        if not self.use_keyboard:
            self.amp.amp.start_sampling()        
            time.sleep(1)	
        
        self.lifes = self.max_lifes
        self.score = 0 
        self.missed = 0 
        #self.background = None
        self.backgrounds = sorted([x for x in get_backgrounds()])
        self.backgrounds = [pygame.image.load(x) for x in 	self.backgrounds]
        self.bgn_idx = 0
        speed_rate = 0.003 if not self.use_keyboard else 0.0003
        trash_number = 0
        w, h = self.size

        bins = [TrashBin(width=w*TrashBin.precent, img_path=path, type=type) for (type, path) in get_bins()]

        number_of_bins = len(bins)
        bin_widht = w * bins[0].precent

        offset = ( 1 - number_of_bins * TrashBin.precent ) / ( number_of_bins + 1 )
        offset = round( w * offset )

        bin_w, bin_h = bin_size = bins[0].size

        pos_y = h - bin_h

        for i, bin_ in enumerate(bins):
            pos_x = bin_w * i
            pos_x += offset * (i + 1)
            bin_.x = pos_x
            bin_.y = pos_y

        trashes = []
        for i, (type, path) in enumerate(get_trashes()):
            t = Trash(width=w*Trash.precent, img_path=path, type=type)
            trashes.append(t)

        np.random.shuffle(trashes)

        play = True
        new_trash = True
        self.update_background()

        while trashes and play and self.lifes > 0 and self.score >= 0:
            if new_trash:
                self.trash = trashes.pop()
                trash_number += 1
                # recalcualte x to be in center
                self.trash.x = w//2 - self.trash.size[1]//2
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
                exit_btn = Button(self.screen, 'Koniec', (200 , 200), (100, 200), (0xff, 0xff, 0xff), (0,0,0) , self.menu)
                
                if not self.use_keyboard:
                    signal = self.amp.get_signal(self.amp.fs//3)
                    move_value = self.muscle_move(signal)
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

                translation_y = w * speed_rate * 1.02 ** trash_number
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
                rectangle_color = (255,239,148)
                
                pygame.draw.rect(self.screen, rectangle_color, (0, 0, w, 50), False)
                self.text("Punkty: "+str(self.score), 100, 25, text='DejaVu Sans Mono', font_size = font_size) #, rectangle_color = (255,239,148))
                self.text('Życia: ', 200 + len("Punkty: "+str(self.score))*font_size, 25, text='DejaVu Sans Mono', font_size = font_size) #, rectangle_color = (255,239,148))
                self.text('❤'*self.lifes, 150 + len("Punkty: "+str(self.score))*font_size + len("Życia")*font_size, 25, text='DejaVu Sans Mono', font_size = 40) #, rectangle_color = (255,239,148))
               
                self.update()

                self.clock.tick(60)
        

        if not self.use_keyboard:
            self.amp.amp.stop_sampling()

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

        self.bgcolour = (255,239,148)
        text_colour = (232,98,203)

        x_screen, y_screen = self.size
        self.screen.fill(self.bgcolour)
        self.update()
        x_button ,y_button = 60, 30

        return_btn = Button(self.screen, 'Menu', (x_button, y_button), (x_button*2, y_button*2), 
                            button_color=text_colour, label_color=self.bgcolour, func=self.menu)
        again_btn = Button(self.screen, 'Zagraj jeszcze raz!', (x_screen // 2, 7 * y_screen // 8), (x_button*7, y_button*3), 
                            button_color=text_colour, label_color=self.bgcolour, func=self.play)
                  
        self.text('WYNIK',    x_screen // 2, y_screen // 4, font_size=64)
        self.text('Punkty', 3*x_screen // 4, y_screen // 2 )
        self.text('Imię',   2*x_screen // 4, y_screen // 2 )
        self.text('Pozycja',  x_screen // 4, y_screen // 2 )

        self.update()
        time.sleep(1)  

        self.text(str(self.score), 3*x_screen // 4, y_screen // 2 + 100 )
        self.update()
        time.sleep(1)
        
        self.text(self.name, 2*x_screen // 4, y_screen // 2 + 100)
        self.update() 
        time.sleep(1)  
        
        self.text(f' {str(place) if place<10 else str(place)}.', x_screen // 4, y_screen // 2 + 100 )
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

        self.bgcolour = (255,239,148)
        text_colour = (232,98,203)
	    
        x_screen, y_screen = self.size
        self.screen.fill(self.bgcolour)
        self.update()
        x_button ,y_button = 60, 30
        return_btn = Button(self.screen, 'Wróć', (x_button, y_button), (x_button*2, y_button*2), 
                            button_color=text_colour, label_color=self.bgcolour, func=self.menu)
        self.text('WYNIKI', x_screen // 2, y_screen // 10  - 25, font_size = 48)
        y_offset = 55
        for i in range(min(len(scores), 10)):
            self.text(f'{" " + str(i+1) if i<10 else str(i+1)}.', x_screen // 4, y_screen // 10 + (i+1)*y_offset)
            self.text(str(scores[i][1]), 2*x_screen // 4, y_screen // 10 + (i+1)*y_offset)
            self.text(str(scores[i][0]), 3*x_screen // 4, y_screen // 10 + (i+1)*y_offset)
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
        
        self.bgcolour = (232,98,203) # needed?
        
        self.screen.fill(self.bgcolour)
        
        pygame.display.set_caption('Segreguj smieci')

        x_screen, y_screen = self.size
        x_button = 300
        y_button = 150
        button_colour = (255,239,148) #(237, 168, 19) #(173, 170, 218)
        text_colour = (232,98,203) #(122, 73, 122) #(218, 170, 214)
        
        b_s = Button(self.screen, 'Start', (x_screen/2,y_screen/2-1.5*y_button), (x_button, y_button), button_colour, text_colour, self.main_loop)
        b_w = Button(self.screen, 'Wyniki', (x_screen/2,y_screen/2), (x_button, y_button), button_colour, text_colour, self.scores)
        b_e = Button(self.screen, 'Wyjdź', (x_screen/2,y_screen/2+1.5*y_button), (x_button, y_button), button_colour, text_colour, pygame.quit)
 
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
    def __init__(self, screen, label, pos, dims, button_color, label_color, func):
        
        self.screen = screen
        self.label = label
        self.pos = pos
        self.dims = dims
        self.button_color = button_color
        self.label_color = label_color
        self.font = pygame.font.SysFont('Arial', 25)
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
        self.b1,self.a1 = butter(1,1/(Fs/2),'highpass')
        
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
