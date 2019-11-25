import pygame

# class TrashGame():
#     def __init__(self):
#         pygame.init()
#         self.bgcolour = 0x2F, 0x4F, 0x4F  # darkslategrey        
#         size = self.width, self.height = 640, 480
#         self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
#         #self.screen = pygame.display.set_mode(size)

#         self.screen.fill(self.bgcolour)
#         self.creen = pygame.display.set_mode(size, pygame.FULLSCREEN)
#         self.screen.fill(self.bgcolour)
#         pygame.display.flip()
#         pong = pygame.mixer.Sound('Blip_1-Surround-147.wav')
#         pong.set_volume(10)
#         pong.play(0)
#         pygame.time.wait(500)

#     def kalibracja(self):
#        pass

#     def main(self,std_luz, std_nap):
#         # alfa = 0.03 # szybkość zmiany położenia
#         # xspeed_init = 4
#         # yspeed_init = 4
#         # max_lives = 6
#         # score = 0
#         # BUF_LEN = 32
#         # M_nap = np.median(std_nap)
#         # M_luz = np.median(std_luz)
#         # sd = M_nap - M_luz

#         # bat = pygame.image.load("bat.png").convert()
#         # batrect = bat.get_rect()

#         # ball = pygame.image.load("ball.png").convert()
#         # ball.set_colorkey((255, 255, 255))
#         # ballrect = ball.get_rect()

#         # pong = pygame.mixer.Sound('Blip_1-Surround-147.wav')
#         # pong.set_volume(10)
#         # pong.play(0)
#         # wall = Wall()
#         # wall.build_wall(self.width)

#         # # Initialise ready for game loop
#         # batrect = batrect.move((self.width / 2) - (batrect.right / 2), self.height - 20)
#         # ballrect = ballrect.move(self.width / 2, self.height / 2)
#         # xspeed = xspeed_init
#         # yspeed = yspeed_init
#         # lives = max_lives
#         # clock = pygame.time.Clock()
#         # pygame.key.set_repeat(1, 30)
#         # pygame.mouse.set_visible(0)  # turn off mouse pointer
#         # i = 0
#         # mx = 0.5
#         # while 1:

#         #     # 60 frames per second
#         #     clock.tick(64)

#         #     # process key presses
#         #     for event in pygame.event.get():
#         #         if event.type == pygame.QUIT:
#         #             sys.exit()
#         #         if event.type == pygame.KEYDOWN:
#         #             if event.key == pygame.K_ESCAPE:
#         #                 sys.exit()
#         #     t = pygame.time.get_ticks() / 1000  # to powinien być czas w sek.
#         #     ##############
#         #     ### TU odczytywanie bufora danych i jego analiza
#         #     packet = amp.get_samples(BUF_LEN)
#         #     X = samples_to_microvolts(packet.samples)
#         #     # if i == 0:
#         #     #     t0 = packet.ts[0]
#         #     #     # t00 = t0
#         #     #     i += 1
#         #     # dt = packet.ts[0] - t0
#         #     # t0 = packet.ts[0]
#         #     x = X[:, 0] - X[:, 1]
#         #     syg = x - np.mean(x)
#         #     std = np.std(syg)
#         #     ################
#         #     # normalizujemy
#         #     mx_new = (std -np.mean((M_nap, M_luz)) )/sd
#         #     mx = (1-alfa)*mx+ alfa*mx_new
#         #     if mx<0:
#         #         mx=0
#         #     elif mx>1:
#         #         mx=1


#         #     # przesuwamy paletkę
#         #     batrect.centerx = mx*self.width
#         #     #print(t, std)
#         #     if (batrect.left < 0):
#         #         batrect.left = 0
#         #     if (batrect.right > self.width):
#         #         batrect.right = self.width

#         #     # check if bat has hit ball    
#         #     if ballrect.bottom >= batrect.top and \
#         #             ballrect.bottom <= batrect.bottom and \
#         #             ballrect.right >= batrect.left and \
#         #             ballrect.left <= batrect.right:
#         #         yspeed = -yspeed
#         #         pong.play(0)
#         #         offset = ballrect.center[0] - batrect.center[0]
#         #         # offset > 0 means ball has hit RHS of bat                   
#         #         # vary angle of ball depending on where ball hits bat                      
#         #         if offset > 0:
#         #             if offset > 30:
#         #                 xspeed = 7
#         #             elif offset > 23:
#         #                 xspeed = 6
#         #             elif offset > 17:
#         #                 xspeed = 5
#         #         else:
#         #             if offset < -30:
#         #                 xspeed = -7
#         #             elif offset < -23:
#         #                 xspeed = -6
#         #             elif offset < -17:
#         #                 xspeed = -5

#         #                 # move bat/ball
#         #     ballrect = ballrect.move(xspeed, yspeed)
#         #     if ballrect.left < 0 or ballrect.right > self.width:
#         #         xspeed = -xspeed
#         #         pong.play(0)
#         #     if ballrect.top < 0:
#         #         yspeed = -yspeed
#         #         pong.play(0)

#         #         # check if ball has gone past bat - lose a life
#         #     if ballrect.top > self.height:
#         #         lives -= 1
#         #         # start a new ball
#         #         xspeed = xspeed_init
#         #         if random.random() > 0.5:
#         #             xspeed = -xspeed
#         #         yspeed = yspeed_init
#         #         ballrect.center = self.width * random.random(), self.height / 3
#         #         if lives == 0:
#         #             msg = pygame.font.Font(None, 70).render("Game Over", True, (0, 255, 255), self.bgcolour)
#         #             msgrect = msg.get_rect()
#         #             msgrect = msgrect.move(self.width / 2 - (msgrect.center[0]), self.height / 3)
#         #             self.screen.blit(msg, msgrect)
#         #             pygame.display.flip()
#         #             # process key presses
#         #             #     - ESC to quit
#         #             #     - any other key to restart game
#         #             while 1:
#         #                 restart = False
#         #                 for event in pygame.event.get():
#         #                     if event.type == pygame.QUIT:
#         #                         sys.exit()
#         #                     if event.type == pygame.KEYDOWN:
#         #                         if event.key == pygame.K_ESCAPE:
#         #                             sys.exit()
#         #                         if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
#         #                             restart = True
#         #                 if restart:
#         #                     self.screen.fill(self.bgcolour)
#         #                     wall.build_wall(self.width)
#         #                     lives = max_lives
#         #                     score = 0
#         #                     break

#         #     if xspeed < 0 and ballrect.left < 0:
#         #         xspeed = -xspeed
#         #         pong.play(0)

#         #     if xspeed > 0 and ballrect.right > self.width:
#         #         xspeed = -xspeed
#         #         pong.play(0)

#         #     # check if ball has hit wall
#         #     # if yes yhen delete brick and change ball direction
#         #     index = ballrect.collidelist(wall.brickrect)
#         #     if index != -1:
#         #         if ballrect.center[0] > wall.brickrect[index].right or \
#         #                 ballrect.center[0] < wall.brickrect[index].left:
#         #             xspeed = -xspeed
#         #         else:
#         #             yspeed = -yspeed
#         #         pong.play(0)
#         #         wall.brickrect[index:index + 1] = []
#         #         score += 10

#         #     self.screen.fill(self.bgcolour)
#         #     scoretext = pygame.font.Font(None, 40).render(str(score), True, (0, 255, 255), self.bgcolour)
#         #     scoretextrect = scoretext.get_rect()
#         #     scoretextrect = scoretextrect.move(self.width - scoretextrect.right, 0)
#         #     self.screen.blit(scoretext, scoretextrect)

#         #     for i in range(0, len(wall.brickrect)):
#         #         self.screen.blit(wall.brick, wall.brickrect[i])

#         #         # if wall completely gone then rebuild it
#         #     if wall.brickrect == []:
#         #         wall.build_wall(self.width)
#         #         xspeed = xspeed_init
#         #         yspeed = yspeed_init+2
#         #         ballrect.center = self.width / 2, self.height / 3

#         #     self.screen.blit(ball, ballrect)
#         #     self.screen.blit(bat, batrect)
#             pygame.display.flip()


# class Wall():

#     def __init__(self):
#         self.brick = pygame.image.load("brick.png").convert()
#         brickrect = self.brick.get_rect()
#         self.bricklength = brickrect.right - brickrect.left
#         self.brickheight = brickrect.bottom - brickrect.top

#     def build_wall(self, width):
#         xpos = 0
#         ypos = 60
#         adj = 0
#         self.brickrect = []
#         for i in range(0, 52):
#             if xpos > width:
#                 if adj == 0:
#                     adj = self.bricklength / 2
#                 else:
#                     adj = 0
#                 xpos = -adj
#                 ypos += self.brickheight

#             self.brickrect.append(self.brick.get_rect())
#             self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
#             xpos = xpos + self.bricklength

# class Thrash():

#     def __init__(self, type=""):
#         self.thrash = pygame.image.load("static/thrash.png").convert()
#         thrash = self.brick.get_rect()
#         self.thrashlength = thrash.right - thrash.left
#         self.thrashheight = thrash.bottom - thrash.top

# class Thrashbin():

#     def __init__(self, type=""):
#         self.thrashbin = pygame.image.load("static/thrashbin.png").convert()
#         thrash = self.brick.get_rect()
#         self.thrashbinlength = thrashbin.right - thrashbin.left
#         self.thrashbinheight = thrashbin.bottom - thrashbin.top

# if __name__ == '__main__':

#     tg = TrashGame()
#     tg.main()
import pygame, sys

def rescale(scale, obj):
    w, h = obj.get_width(), obj.get_height()

    w, h = int(scale*w), int(scale*h)
    return pygame.transform.scale(obj, (w, h))

pygame.init()
clock = pygame.time.Clock()

display_width = 1280//2
display_height = 720//2
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('The Trash Game')

trashImg = pygame.image.load('static/kosz_szkło.png')
trashImg = rescale(0.5, trashImg)
trashImg = pygame.transform.rotozoom(trashImg, 90, 0.6)
def trash(x,y):
    x =  (display_width * .5)
    y = (display_height * .5)
    gameDisplay.blit(trashImg, (x,y))

x = (display_width * 0.45)
y = (display_height * 0.8)

floorImg = pygame.image.load('static/floor.jpg')
def floor():
    x, y = 0, 0
    gameDisplay.blit(floorImg, (x,y))

wallImg = pygame.image.load('static/wall.jpg')
def wall():
    x, y = 0, 0
    gameDisplay.blit(wallImg, (x,y))


black = (0,0,0)
white = (255,255,255)

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
    gameDisplay.fill(white)
    trash(x,y)

        
    pygame.display.update()
    clock.tick(60)

pygame.quit()
print("quiting")
quit()