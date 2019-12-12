import pygame
import os

from utils import *

def debug():
    import ipdb; ipdb.set_trace()

class Simple_Game(object):
    """Simple_Game"""
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
        play = True
        new_trash = True
        # debug()

        while trashes and play and lifes > 0:
            print("while")

            if new_trash:
                print("new trash")
                trash = trashes.pop()
                print(trash.type)
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
                    collsion = False
                    for (i, bin_) in enumerate(bins):
                        # if bin_.image.colliderect(trash.image):
                        #     print(i)
                        if collide_in(trash, bin_):

                            if bin_.type == trash.type:
                                print('same')

                                self.score += 100
                                collsion = True
                            else:
                                print("wrong")
                                self.score += 10   
                                collsion = True
                            print(self.score)
                            
                    if not collsion:   
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
        self.play()
        print('done')

        return False



# buttonText = pygame.font.SysFont('', 20)
 
class Button(object):
    def __init__ (self, colour, x, y, width, height, label):
        self.__colour = colour
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__label = label
 
    @property
    def colour(self):
        return self.colour
 
    @property
    def x(self):
        return self.x
 
    @property
    def y(self):
        return self.y

    @property
    def width(self):
        return self.width
 
    @property
    def height(self):
        return self.height
 
    @property
    def label(self):
        return self.label


    # def draw(self, surface):
    #     self._render()
    #     surface.blit(self._surface, self._rect.topleft)


class Trash(pygame.sprite.Sprite):
    """docstring for Trash"""

    precent = 0.05

    def __init__(self, pos=(0, 0), *, img_path=None ,type=None, width):

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
