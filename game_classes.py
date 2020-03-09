import pygame
import os
import sys

from utils import *

def debug():
    import ipdb; ipdb.set_trace()


class Simple_Game(object):
    """dSimple_Game"""
    def __init__(self, size,):
        pygame.init()
        self.bgcolour = 0x2F, 0x4F, 0x4F  # darkslategrey   
        self.size = size
        # self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(self.size)

        self.screen.fill(self.bgcolour)

        pygame.display.flip()

        self.clock = pygame.time.Clock()

    def main(self):
        play = True

        while play:
            play = self.menu()



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

    def game_score(self):
        '''game finish screen with score, get player name and push to scores DB'''
        print(self.score)
        pass

    def calibrate(self):
        pass

    @property
    def can_stear(self, obj):
        if self.allow_stearing:
            pass


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
    
        b_s = Button(self.screen, 'Start', (x_screen/2,y_screen/2-1.5*y_button), (x_button, y_button), button_colour, text_colour, self.play)
        b_w = Button(self.screen, 'Wyniki', (x_screen/2,y_screen/2), (x_button, y_button), button_colour, text_colour, self.game_score)
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
                
    def scores(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position

            # checks if mouse position is over the button

            if self.rect.collidepoint(mouse_pos):
                # prints current location of mouse
                print('Wyniki')
                
                
    def get_out(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position

            # checks if mouse position is over the button

            if self.rect.collidepoint(mouse_pos):
                # prints current location of mouse
                #print('button was pressed at {0}'.format(mouse_pos))
                pygame.quit(); sys.exit();


class Trash(pygame.sprite.Sprite):
    """docstring for Trash"""

    precent = 0.05

    def __init__(self, pos=(0, 0), *, img_path=None ,type=None, width):

        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = pygame.image.load("static/trash/plastic_metal/blank-shampoo-bottle-1415298.png").convert()
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

