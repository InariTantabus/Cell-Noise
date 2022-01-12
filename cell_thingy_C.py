import pygame, sys, os, random, math

#----------------Setup pygame/window----------------#
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Cell')

WINDOW_SIZE = (400, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((100, 100))
#----------------Setup pygame/window----------------#

click = False
run = False
amount = 10

def get_cells(cells):
    temp_list = []
    for cell in cells:
        temp_list.append(cell)
    random.shuffle(temp_list)
    
    return temp_list

class Cell(object):
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.value = [random.random(), random.random(), random.random()]
        self.color = self.value
    
    def update(self, cells):
        temp_value = [0, 0, 0]
        counter = 0
    
        #------------------ONLY ONE------------------#
        # temp_list = []
        # temp_list.append('{}:{}'.format(self.x+1, self.y))
        # temp_list.append('{}:{}'.format(self.x-1, self.y))
        # temp_list.append('{}:{}'.format(self.x, self.y+1))
        # temp_list.append('{}:{}'.format(self.x, self.y-1))
        # for item in temp_list:
        #     if item in cells:
        #         counter += 1
        #         temp_value[0] += cells[item].value[0]
        #         temp_value[1] += cells[item].value[1]
        #         temp_value[2] += cells[item].value[2]

        for i in range(0, 2): # (0, 2) For slant, (0, 3) default
            for v in range(0, 2): # (0, 2) For slant, (0, 3) default
                if '{}:{}'.format((i-1)+self.x, (v-1)+self.y) in cells:
                    counter += 1
                    temp_value[0] += cells['{}:{}'.format((i-1)+self.x, (v-1)+self.y)].value[0]
                    temp_value[1] += cells['{}:{}'.format((i-1)+self.x, (v-1)+self.y)].value[1]
                    temp_value[2] += cells['{}:{}'.format((i-1)+self.x, (v-1)+self.y)].value[2]
        #------------------ONLY ONE------------------#

        if counter:
            temp_value[0] /= counter
            temp_value[1] /= counter
            temp_value[2] /= counter
            
            #------------------ONLY ONE------------------#
            # for i in range(0, 3):
            #     if temp_value[i] < .4:
            #         self.value[i] -= .05
            #     if temp_value[i] > .6:
            #         self.value[i] += .05
            #     self.value[i] += (random.random()*2-1)/amount
            #     if self.value[i] > 1:
            #         self.value[i] = 1
            #     if self.value[i] < 0:
            #         self.value[i] = 0

            for i in range(0, 3):
                self.value[i] = temp_value[i]+(random.random()*2-1)/amount
                if self.value[i] > 1:
                    self.value[i] = 1
                if self.value[i] < 0:
                    self.value[i] = 0
            #------------------ONLY ONE------------------#

        self.color = self.value

cells = {}
for i in range(0, 99):
    for v in range(0, 99):
        cells['{}:{}'.format(i, v)] = Cell((i, v))

display.fill((0, 0, 0))
for cell in cells:
    pygame.draw.circle(display, (cells[cell].value[0]*255, cells[cell].value[1]*255, cells[cell].value[2]*255), (cells[cell].x, cells[cell].y), 1)
    cells[cell].update(cells)

while True:
    mx, my = pygame.mouse.get_pos()
    mx = round(mx/4)
    my = round(my/4)

    if run:
        display.fill((0, 0, 0))
        
        #------------------ONLY ONE------------------#
        for cell in cells:
            pygame.draw.circle(display, (cells[cell].value[0]*255, cells[cell].value[1]*255, cells[cell].value[2]*255), (cells[cell].x, cells[cell].y), 1)
            cells[cell].update(cells)
        
        # cell_list = get_cells(cells)
        # for cell in cell_list:
            # pygame.draw.circle(display, (cells[cell].value[0]*255, cells[cell].value[1]*255, cells[cell].value[2]*255), (cells[cell].x, cells[cell].y), 1)
            # cells[cell].update(cells)
        #------------------ONLY ONE------------------#
        
    if click:
        for cell in cells:
            manh_dist = abs(mx-cells[cell].x) + abs(cells[cell].y-my)
            if manh_dist < 4:
                for i in range(0, 3):
                    cells[cell].value[i] = 1 - cells[cell].value[i]
        
    click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
            if event.button == 4:
                amount += 4
            if event.button == 5:
                amount -= 4
                if amount < 2:
                    amount = 2
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                run = not run

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    mainClock.tick(60)