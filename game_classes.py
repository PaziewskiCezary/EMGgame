import pygame
import os
import math
import time
import sys
import pickle
import pygame_textinput

from scipy.signal import butter, lfilter,iirnotch,lfilter_zi, filtfilt
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier

from utils import *

def debug():
    import ipdb; ipdb.set_trace()


class Simple_Game(object):
    """dSimple_Game"""
    def __init__(self, size,):
        pygame.init()
        try:
            self.amp = Amplifier(512, [0, 1])
        except ValueError as e:
            print('123', e)
            exit(1)

        self.bgcolour = (232,98,203) # 0x2F, 0x4F, 0x4F  # darkslategrey   
        self.size = size
        self.max_lifes = 1
        self.max_missed = 1
        # self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(self.size)

        self.screen.fill(self.bgcolour)

        pygame.display.flip()

        self.clock = pygame.time.Clock()

        self.backgrounds = sorted([x for x in get_backgrounds()])
        self.backgrounds = [pygame.image.load(x) for x in 	self.backgrounds]
        self.max_shift = 10

    def move_thrash(self, arg):
        if not self.trash:
            raise ValueError('self.thrash not set')
        if abs(arg) > 1:
            raise ValueError('arg must be between -1 and 1')
        self.trash.x += self.max_shift * arg

    def main(self):
        play = True

        #while play:
        play = self.menu()

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


    def calibrate(self):
        self.bgcolour = (255,239,148)
        x_screen, y_screen = self.size
        text_colour = (232,98,203)
        
        self.screen.fill(self.bgcolour)
        print("kalibracja")
        pygame.display.set_caption('Kalibracja') 
        pygame.display.update()
  
        self.screen.fill(self.bgcolour)
        self.text('KALIBRACJA', x_screen // 2, y_screen // 2)
        pygame.display.update()
        time.sleep(2)
        
        print("rozluznij reke")

        self.screen.fill(self.bgcolour)
        self.text('ROZLUŹNIJ RĘKĘ', x_screen // 2, y_screen // 2)
        pygame.display.update()
        time.sleep(1)
        self.calib_min = self.amp.calib()
        # self.calib_min = 10
        time.sleep(2)
        print("zacisnij reke")
        
        self.screen.fill(self.bgcolour)
        self.text('ZACIŚNIJ RĘKĘ', x_screen // 2, y_screen // 2)
        pygame.display.update()

        time.sleep(1)
        self.calib_max = self.amp.calib()
        # self.calib_max = 400
        if self.calib_min >= self.calib_max or  self.calib_max - self.calib_min < 50:
            print("powtarzam kalibrację")
            self.screen.fill(self.bgcolour)
            self.text('POWTORZAM KALIBRACJĘ', x_screen // 2, y_screen // 2)
            pygame.display.update() 
            time.sleep(2)
            self.calibrate()

        print('koniec kalibracji')
        self.screen.fill(self.bgcolour)
        self.text('KONIEC KALIBRACJI', x_screen // 2, y_screen // 2) 
        pygame.display.update()

    def get_name(self):
        
        self.bgcolour = (255,239,148)
        text_colour = (232,98,203)
	    
        textinput = pygame_textinput.TextInput()

        #textinput.cursor_color = (232,98,203)
        textinput.text_color = (232,98,203)
        
        self.screen = pygame.display.set_mode(self.size)
        clock = pygame.time.Clock()
        
        x_screen, y_screen = self.size


        font = pygame.font.Font('freesansbold.ttf', 32) 
        text = font.render("PODAJ SWÓJ NICK:", True, text_colour) 
        #display_surface = pygame.display.set_mode((x_screen, y_screen ))

        #textRect = text.get_rect()  
        #textRect.center = (x_screen // 2, y_screen // 4) 
        #self.screen.blit(text, textRect)
        #pygame.display.update()  	
        
        d = True
        while d:
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
            #print(a)
            self.screen.blit(textinput.get_surface(), ((x_screen - a[0]) // 2 , y_screen // 2))

            pygame.display.update()
            clock.tick(30)
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    print(event.key, pygame.K_RETURN)
                    if event.key == pygame.K_RETURN:
                        self.name = textinput.get_text()
                        print(self.name)
                        d = False
                        break
    

    def text(self, napis, x_pos, y_pos, *, text='DejaVu Sans Mono', font_size=32):
        x_screen, y_screen = self.size
        text_colour = (232,98,203)
        self.bgcolour = (255,239,148)
        # self.screen = pygame.display.set_mode((x_screen, y_screen ))
        # self.screen.fill(self.bgcolour)

        font = pygame.font.SysFont(text, font_size)
        text = font.render(napis, True, text_colour) 

        textRect = text.get_rect()  
        textRect.center = (x_pos, y_pos) 
        self.screen.blit(text, textRect)
        # pygame.display.update()  			


    def main_loop(self):
        self.get_name()
        self.calibrate()
        self.play()
        
    def play(self):
        self.amp.amp.start_sampling()        
        time.sleep(1)	
        
        self.lifes = self.max_lifes
        self.score = 0 
        self.missed = 0 
        #self.background = None
        self.backgrounds = sorted([x for x in get_backgrounds()])
        self.backgrounds = [pygame.image.load(x) for x in 	self.backgrounds]
        self.bgn_idx = 0
        speed_rate = 0.003

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
            # print(type, path)
            t = Trash(width=w*Trash.precent, img_path=path, type=type)
            trashes.append(t)

        np.random.shuffle(trashes)

        play = True
        new_trash = True
        # debug()
        self.update_background()

        while trashes and play and self.lifes > 0:
            if new_trash:
                print("new")
                print(len(trashes))

                self.trash = trashes.pop()
                print(id(self.trash.image))
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
                if break_loop:
                    break
                exit_btn = Button(self.screen, 'Koniec', (200 , 200), (100, 200), (0xff, 0xff, 0xff), (0,0,0) , self.menu)
                predupa = self.amp.get_signal(self.amp.fs//3)
                # print(self.calib_min, predupa, self.calib_max)
                dupa = self.muscle_move(predupa)
                # print(dupa)
                self.move_thrash(dupa)

                trash_x, trash_y = self.trash.pos 

                translation_y = w * speed_rate
                self.trash.x, self.trash.y = trash_x, trash_y +  translation_y

                # if trash.bottom > pos_y:

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
                            print(self.score)
                            
                    if not collsion:   
                        self.lifes -= 1
                        print(self.lifes, 'lifes left')
                        

                    new_trash = True
                    this_trash = False


                # if trash.top > self.size[1]:
                #     pygame.quit()

                # ploting stuff
                self.screen.fill(self.bgcolour)
                self.update_background()
                for bin_ in bins:
                    self.screen.blit(bin_.image, bin_.pos)
                self.screen.blit(self.trash.image, self.trash.pos)
                pygame.display.update()

                self.clock.tick(60)
        


        
        self.amp.amp.stop_sampling()
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

        x_screen, y_screen = self.size
        self.screen.fill(self.bgcolour)
        pygame.display.update()
        x_button ,y_button = 60, 30

        self.bgcolour = (255,239,148)
        text_colour = (232,98,203)

        return_btn = Button(self.screen, 'Menu', (x_button, y_button), (x_button*2, y_button*2), 
                            button_color=text_colour, label_color=self.bgcolour, func=self.menu)
        again_btn = Button(self.screen, 'Zagraj jeszcze raz!', (x_screen // 2, 7 * y_screen // 8), (x_button*7, y_button*3), 
                            button_color=text_colour, label_color=self.bgcolour, func=self.play)
                  
        self.text('WYNIK', x_screen // 2, y_screen // 4, font_size = 64)
        self.text('Punkty', 3*x_screen // 4, y_screen // 2 )
        self.text('Imię', 2*x_screen // 4, y_screen // 2 )
        self.text('Pozycja', x_screen // 4, y_screen // 2 )

        pygame.display.update()
        time.sleep(1)  


        self.text(str(self.score), 3*x_screen // 4, y_screen // 2 + 100 )
        pygame.display.update()
        time.sleep(1)
        
        self.text(self.name, 2*x_screen // 4, y_screen // 2 + 100)
        pygame.display.update() 
        time.sleep(1)  
        
        self.text(f'{" " + str(place) if place <10 else str(place)}.', x_screen // 4, y_screen // 2 + 100 )
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                return_btn.onClick(event)
                again_btn.onClick(event)
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit();
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu()


    def game_score(self):
        '''game finish screen with score, get player name and push to scores DB'''
        print(self.score)
        pass

    def update_background(self):
        
        idx = math.log2(self.max_lifes - self.lifes + self.missed + 1)
        # print(self.lifes, self.missed, idx)
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

        print('wyniki', scores)

        self.bgcolour = (255,239,148)
        text_colour = (232,98,203)
	    
        # self.screen = pygame.display.set_mode(self.size)
        
        x_screen, y_screen = self.size
        self.screen.fill(self.bgcolour)
        pygame.display.update()
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
            pygame.display.update()
        while True:
            for event in pygame.event.get():
                return_btn.onClick(event)
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit();
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu()
        # pygame.display.update() 


        del scores 
        del index
        

    def menu(self):
        # remove when menu is finished
        #self.play()
        #print('done')
        
        self.bgcolour = (232,98,203)
        
        self.screen.fill(self.bgcolour)
        
        pygame.display.set_caption('Segreguj smieci')
        #screen = pygame.display.set_mode((600,400), 0, 32)
        #screen.fill((154, 7, 118))
        
        x_screen, y_screen = self.size
        x_button = 300
        y_button = 150
        button_colour = (255,239,148) #(237, 168, 19) #(173, 170, 218)
        text_colour = (232,98,203) #(122, 73, 122) #(218, 170, 214)
        
        #(self, screen, label, pos, dims, button_color, label_color=(255,255,255))
    
        b_s = Button(self.screen, 'Start', (x_screen/2,y_screen/2-1.5*y_button), (x_button, y_button), button_colour, text_colour, self.main_loop)
        b_w = Button(self.screen, 'Wyniki', (x_screen/2,y_screen/2), (x_button, y_button), button_colour, text_colour, self.scores)
        b_e = Button(self.screen, 'Wyjdź', (x_screen/2,y_screen/2+1.5*y_button), (x_button, y_button), button_colour, text_colour, pygame.quit)
 
        pygame.display.update()
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
        pygame.display.update()

        return False


##### wersja bez mięśni######################################## 			
'''
    def play(self):

        lifes = 10
        self.score = 0 
        speed_rate = 0.0003


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

        trashes = [Trash(width=w*Trash.precent, img_path=path, type=type) for (type, path) in get_trashes()] 
        # debug()
        play = True
        new_trash = True
        print(bool(trashes))
        while trashes and play and lifes > 0:
            print("while")

            if new_trash:
                print("new trash")
                trash = trashes.pop()
                # recalcualte x to be in center
                trash.x = w//2 - trash.size[1]//2
                trash.y = 100
                new_trash = False
                this_trash = True

            if not lifes:
                play = False

            while this_trash:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        play = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            play = False

                        if event.key == pygame.K_LEFT:
                            trash.x += -10

                        if event.key == pygame.K_RIGHT:
                            trash.x += 10

                trash_x, trash_y = trash.pos 

                translation_y = w * speed_rate
                trash.x, trash.y = trash_x, trash_y +  translation_y

                if trash.bottom > pos_y:

                    for (i, bin_) in enumerate(bins):
                        # if bin_.image.colliderect(trash.image):
                        #     print(i)
                        if collide_in(trash, bin_):

                            if bin_.type == trash.type:
                                print('same')

                                self.score += 100
                            else:
                                print("wrong")
                                self.score += 10   
                            print(self.score)

                        else:
                            print("miss")

                            lifes -= 1
                            print(lifes, 'lifes left')
                    new_trash = True
                    this_trash = False



                # if trash.top > self.size[1]:
                #     pygame.quit()

                # ploting stuff
                self.screen.fill(self.bgcolour)
                for bin_ in bins:
                    self.screen.blit(bin_.image, bin_.pos)
                self.screen.blit(trash.image, trash.pos)
                pygame.display.update()


                self.clock.tick(60)
'''

#################################################################



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
                # prints current location of mouse
                #print('button was pressed at {0}'.format(mouse_pos))
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
            print(time.time()-t)
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
        #fcalibs = filtfilt(self.b1,self.a1,s)
        scim = np.mean(np.abs(s))
        return scim
