import pygame
from math import sqrt, sin, cos

# screen width and height for pygame
SCREEN_WIDTH = 1012
SCREEN_HEIGHT = 612

# total map size
MAP_WIDTH = 24
MAP_HEIGHT = 24

# initital start coords
POS_X = 12
POS_Y = 12

# initial direction vector
DIR_X = -1
DIR_Y = 0

# the camera plane. I don't fully understand how this affects the casting with respect to motion
PLANE_X = 0.0;
PLANE_Y = 0.66;


# rgb values for colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREY = (224,224,224)

# pastel colors
PASTEL_RED = (222, 165, 164)
PASTEL_GREEN = (3, 192, 60)
PASTEL_YELLOW = (253, 252, 160)
PASTEL_BLUE = (119, 158, 203)
PASTEL_BLACK = (54, 69, 79)
PASTEL_GREY = (128, 128, 128)
PASTEL_WHITE = (234, 224, 200)
PASTEL_ORANGE = (255, 179, 71)
PASTEL_BROWN = (130, 105, 83)


# time of current and previous frame
# prev time isn't just cur time -1 cause the number fo frames isn't constant
time = 0
prevTime = 0

# checks if the game loop is done
loop_done = False


# the map is a 2d matrix. A zero represents a wall and a non zero value represents a 1
# this the differences in values are used to map colors and maybe textures
MAP_STRING = """1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 2 2 2 2 2 0 0 0 0 3 0 3 0 3 0 0 0 1
1 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 2 0 0 0 2 0 0 0 0 3 0 0 0 3 0 0 0 1
1 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 2 2 0 2 2 0 0 0 0 3 0 3 0 3 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 4 0 4 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 4 0 0 0 0 5 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 4 0 4 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 4 0 4 0 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1""";

MAP = [[int(char) for char in line.split(" ")] for line in MAP_STRING.split("\n")]

pygame.init();
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raycaster. Kinda")

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(PASTEL_BLACK)
screen.blit(background,(0,0))
pygame.display.flip()

while(not loop_done):

    for i in range(SCREEN_WIDTH):
        cameraX = 2 * i / float(SCREEN_WIDTH) - 1
        rayPosX = POS_X
        rayPosY = POS_Y
        rayDirX = DIR_X + PLANE_X * cameraX
        rayDirY = DIR_Y + PLANE_Y * cameraX

        # which cell of the map we're in
        mapX = int(rayPosX)
        mapY = int(rayPosY)

        perpendicularWallDist = 0.9

        # dist of ray to next x or y
        sideDistX = 0.0
        sideDistY = 0.0

        deltaDistX = sqrt(1 + (rayDirY * rayDirY) / (rayDirX * rayDirX));

        try:
            deltaDistY = sqrt(1 + (rayDirX * rayDirX) / (rayDirY * rayDirY));
        except ZeroDivisionError:
            # consider using float_info.max here instead of infinity
            deltaDistY = float("inf")

        # steps for the DDA algorithm
        stepX = 0;
        stepY = 0;

        # did the ray hit a wall?
        didHit = False

        # which direction did it hit? North - South (x axis) or East - West (y - axis)
        # x side = 0; y side  = 1
        side = 0;

        # if rayDirX and rayDirY are less than zero step is -1
        # if greater than zero step is 1
        # if zero step is ignored
        # rayPosX - mapX gives perpendicular distance. Multiply by delta to get side
        # simple cartesian distance
        # step is calculated here

        if(rayDirX < 0):
            stepX = -1
            sideDistX = (rayPosX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 2.0 - rayPosX) * deltaDistX

        if(rayDirY < 0):
            stepY = -1
            sideDistY = (rayPosY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - rayPosX) * deltaDistY

        # doing DDA. Increment by one square for each step
        # when ray is hit, figure out which side it hits

        while not didHit:
            # keep jumping to next map square
            if(sideDistX < sideDistY):
                mapX += stepX
                sideDistX += deltaDistX
                side = 0
            else:
                mapY += stepY
                sideDistY += deltaDistY
                side = 1

            if(MAP[mapX][mapY] > 0):
                didHit = True

        # calculate the distance from camera
        if side == 0:
            perpendicularWallDist = abs((mapX - rayPosX + (1 - stepX) / 2) / rayDirX)
        else:
            try:
                perpendicularWallDist = abs((mapY - rayPosY + (1 - stepY) / 2) / rayDirY)
            except ZeroDivisionError:
                perpendicularWallDist = float("inf")

        # calculate height of line to draw on screen
        try:
            lineHeight = abs(int(SCREEN_HEIGHT / perpendicularWallDist))
        except ZeroDivisionError:
            lineHeight = SCREEN_HEIGHT

        # calculate lowest and highest pixel to fill in current stripe
        drawStart = (-lineHeight / 2) + (SCREEN_HEIGHT / 2)
        if drawStart < 0:
            drawStart = 0

        drawEnd = (lineHeight / 2) + (SCREEN_HEIGHT / 2)
        if drawEnd >= SCREEN_HEIGHT:
            drawEnd = SCREEN_HEIGHT -1

        # python doesn't have switch case. Boo
        if MAP[mapX][mapY] == 1:
            color = PASTEL_RED
        elif MAP[mapX][mapY] == 2:
            color = PASTEL_GREEN
        elif MAP[mapX][mapY] == 3:
            color = PASTEL_BLUE
        elif MAP[mapX][mapY] == 4:
            color = PASTEL_WHITE
        elif MAP[mapX][mapY] == 5:
            color = PASTEL_YELLOW
        else:
            color = PASTEL_BROWN

        #color other side is a different color
        if(side == 1):
            color = (color[0]/2, color[1]/2, color[2]/2)

        # draw the line vertically.
        if color:
            pygame.draw.line(background, color, (i, drawStart), (i, drawEnd))



    oldTime = time
    time = pygame.time.get_ticks()
    frameRate = (oldTime - time) / 1000.0
    if frameRate == 0.0:
        frameRate = 1.0

    movementSpeed = frameRate * 3.0
    rotationSpeed = frameRate * 2.0

    #  tried using pygame.event.KEYDOWN but it was too discretised for actions
    # no idea what event.pump does too lazy to look up
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if 1 in list(keys):
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            oldDirX = DIR_X
            DIR_X = DIR_X * cos(rotationSpeed) - DIR_Y * sin(rotationSpeed)
            DIR_Y = oldDirX * sin(rotationSpeed) + DIR_Y * cos(rotationSpeed)
            oldPlaneX = PLANE_X
            PLANE_X = PLANE_X * cos(rotationSpeed) - PLANE_Y * sin(rotationSpeed)
            PLANE_Y = oldPlaneX * sin(rotationSpeed) + PLANE_Y * cos(rotationSpeed)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            oldDirX = DIR_X
            DIR_X = DIR_X * cos(-rotationSpeed) - DIR_Y * sin(-rotationSpeed)
            DIR_Y = oldDirX * sin(-rotationSpeed) + DIR_Y * cos(-rotationSpeed)
            oldPlaneX = PLANE_X
            PLANE_X = PLANE_X * cos(-rotationSpeed) - PLANE_Y * sin(-rotationSpeed)
            PLANE_Y = oldPlaneX * sin(-rotationSpeed) + PLANE_Y * cos(-rotationSpeed)

        if keys[pygame.K_ESCAPE]:
            exit(0)

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if MAP[int(POS_X + DIR_X * movementSpeed)][int(POS_Y)] == 0:
                POS_X += DIR_X * movementSpeed
            if MAP[int(POS_X)][int(POS_Y + DIR_Y * movementSpeed)] == 0:
                POS_Y += DIR_Y * movementSpeed

        # move backwards if there's no wall behind you
        if keys[pygame.K_UP] or keys[pygame.K_a]:
            if MAP[int(POS_X - DIR_X * movementSpeed)][int(POS_Y)] == 0:
                POS_X -= DIR_X * movementSpeed
            if MAP[int(POS_X)][int(POS_Y - DIR_Y * movementSpeed)] == 0:
                POS_Y -= DIR_Y * movementSpeed

        #straife right
        if keys[pygame.K_x]:
            if MAP[int(POS_X - PLANE_X * movementSpeed)][int(POS_Y)] == 0:
                POS_X -= PLANE_X * movementSpeed
            if MAP[int(POS_X)][int(POS_Y - PLANE_Y * movementSpeed)] == 0:
                POS_Y -= PLANE_Y * movementSpeed


        if keys[pygame.K_z]:
            if MAP[int(POS_X + PLANE_X * movementSpeed)][int(POS_Y)] == 0:
                POS_X += PLANE_X * movementSpeed
            if MAP[int(POS_X)][int(POS_Y + PLANE_Y * movementSpeed)] == 0:
                POS_Y += PLANE_Y * movementSpeed



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    screen.blit(background,(0,0))
    pygame.display.flip()

    # this where the screen is refreshed. kinda. like filling it with the background color
    # so it can be painted over
    background.fill(PASTEL_BLACK)
