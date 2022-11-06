import time
import pygame   
from OpenGL.GL import *


running = True
vivo = {}
muerto = {}
grid = {(22, 8), (12, 7), (36, 7), (17, 9), (11, 8), (1, 9), (25, 4), (2, 8), (16, 7),
        (25, 10), (21, 6), (23, 9), (14, 6), (36, 6), (22, 7), (14, 12), (17, 8), (11, 10),
        (25, 9), (35, 7), (1, 8), (18, 9), (22, 6), (21, 8), (23, 5), (12, 11), (17, 10),
        (11, 9), (35, 6), (25, 5), (2, 9), (13, 6), (13, 12), (15, 9), (16, 11), (21, 7)}


def pixel(x, y, width, height,color):
    glEnable(GL_SCISSOR_TEST)
    glScissor(int(x),int(y),int(width),int(height))
    glClearColor(color[0],color[1],color[2],1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)
                                  

def vecinos(grid, x, y):
    vecino = {(x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1)}

    vivo = {(i[0], i[1]) for i in vecino if i in grid}
    muerto = vecino - vivo

    return vivo, muerto
    
    
def upgrade(grid):
    nuevo = set()
    for x in grid:
        nuevo.add(x)
    undead = {}

    for (x, y) in grid:
        n_vivo, n_muerto = vecinos(grid, x, y)
        
        if len(n_vivo) < 2 or len(n_vivo) > 3:
            nuevo.remove((x, y))

        for i in n_muerto:
            undead[i] = undead.get(i, 0) + 1
            
    for key,value in undead.items():
        if value == 3:
            nuevo.add((key[0], key[1]))

    return nuevo

def draw(screen: pygame.Surface, grid: grid) :
    width = screen.get_width() / 50
    height = screen.get_height() / 50
    border = 2

    for (x, y) in grid:
        if x*width+border > 500:
            x = x-50
        if y * height+border>500:
            y = y-50
        if x*width+border < 0:
            x = x+50
        if y * height+border<0:
            y = y+50
        pixel(x* width + border,y * height + border,width - border,height - border,(255,255,255))


pygame.init()
screen = pygame.display.set_mode((500, 500), pygame.OPENGL | pygame.DOUBLEBUF)

while running:

    screen.fill((0, 0, 0))
    draw(screen, grid)
    glClearColor(0,0,0,0)
    pygame.display.flip()
    time.sleep(0.1)
    glClear(GL_COLOR_BUFFER_BIT)
    grid = upgrade(grid)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
