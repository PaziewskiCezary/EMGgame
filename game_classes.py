import pygame

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
        score = 0 
        speed_rate = 0.0003

        play = True

        w, h = self.size

        thrash = Thrash((100, 100), width=Thrash.precent*w)

        number_of_bins = 5
        bin_widht = w * ThrashBin.precent

        offset = ( 1 - number_of_bins * ThrashBin.precent ) / ( number_of_bins + 1 )
        offset = round( w * offset )

        # bins = [ThrashBin(( offset + ( w - offset ) // number_of_bins * (i), y) ) for i in range(5)] 
        bins = [ThrashBin(width=w*ThrashBin.precent) for i in range(5) ] 
        bin_w, bin_h = bin_size = bins[0].size

        pos_y = h - bin_h

        for i, bin_ in enumerate(bins):
            pos_x = bin_w * i
            pos_x += offset * (i + 1)
            bin_.pos = (pos_x, pos_y)

        while play:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        play = False


            thrash_w, thrash_h = thrash.pos 

            translation_x = w * speed_rate
            thrash.pos = thrash_w, thrash_h +  translation_x

            if thrash.bottom > pos_y:
                print("at bins")

                # TODO collison with bins

                for (i, bin_) in enumerate(bins):
                    breakpoint()
                    if bin_.image.colliderect(thrash.image):
                        print(i)


            # ploting stuff
            self.screen.fill(self.bgcolour)
            for bin_ in bins:
                self.screen.blit(bin_.image, bin_.pos)
            self.screen.blit(thrash.image, thrash.pos)
            pygame.display.update()


            self.clock.tick(60)


    def calibrate(self):
        pass

    def stear(self, obj):
        if self.allow_stearing:
            pass


    def menu(self):
        self.play()


        play_button = Button([0, 255, 0], 450, 100, 100, 50, "Graj")
        exit_button = Button([255, 0, 0], 450, 200, 100, 50, "Wyjdź")
         


        while True:

            pygame.draw.rect(self.screen, [255, 0, 0], play_button)  
            pygame.draw.rect(self.screen, [255, 0, 0], exit_button)  


            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos 


                        if play_button.collidepoint(mouse_pos):
                           self.play()
                        
                        if exit_button.collidepoint(mouse_pos):
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


class Thrash(pygame.sprite.Sprite):
    """docstring for Trash"""

    precent = 0.07

    def __init__(self, pos=(0, 0), *,  width):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("static/thrash/plastic_metal/blank-shampoo-bottle-1415298.png").convert()

        w, h = size = self.image.get_size()

        scale = width / w

        self.image = pygame.transform.scale(self.image, (int(size[0]*scale), int(size[1]*scale)))
        self.size = self.image.get_size()

        self.pos = pos

    @property
    def bottom(self):
        return self.image.get_rect()[3] + self.pos[1]

    @property
    def top(self):
        return self.image.get_rect()[1] + self.pos[1]


    def draw(self):
        pass
 
class ThrashBin(pygame.sprite.Sprite):
    """docstring for Trash"""

    precent = 0.15

    def __init__(self, pos=(0, 0), *,  width):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("static/trash.png").convert()
        w, h = size = self.image.get_size()

        scale = width / w

        self.image = pygame.transform.scale(self.image, (int(size[0]*scale), int(size[1]*scale)))
        self.size = self.image.get_size()

        self.pos = pos


    def draw(self):
        pass
        
