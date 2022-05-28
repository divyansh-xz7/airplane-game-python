import pygame as pg
import random2 as rn
import time

pg.init()

# display
a = 1000
b = 800
d = pg.display.set_mode((a, b))

# color variables for rgb(red, green, blue)
c1 = 250
c2 = 250
c3 = 250
# for changing value of c1,c2,c3
c1_c = 1
c2_c = 2
c3_c = 3
color = (c1, c2, c3)
black = (0, 0, 0)
white = (255, 255, 255)

clock = pg.time.Clock()

# boolean variables
crashed = False
sett = False
stop = False

# control variables
left = False
right = False
up = False
down = False
fire = False
# image variables
img1 = pg.image.load('plane3.png')
img2 = pg.image.load('space.jpg')
img3 = pg.image.load('alien.png')
img_pause = pg.image.load('pause.png')
img_sett = pg.image.load('settings.png')
img_play = pg.image.load('play.png')

# plane coordinates
x = 450
y = 600

q = 0
w = 0
# size of plane
x1 = 100
y1 = 100

# groups
targets = []  # to store enemies
bullets = []  # to store bullets
bulletspeed = 8
targetspeed = 1

laserfuel = 50
laserfuelcapacity = 90
bullet_time_gap = 0
enemy_time_gap = 0
health = 4
score = 0

# extra variables
mode = "main"
firemode = "bullet"
inputmode = "keyboard"
frame = 60


# functions

def draw_menu():
    if mode == "main":
        d.blit(img_pause, (a - 70, 20))
    else:
        d.blit(img_play, (a - 70, 20))
    d.blit(img_sett, (a - 70, 90))
    message_display(str(score), a - 50, 180, 30)


def text_objects(text, font):
    textsurface = font.render(text, True, (255, 255, 255))
    return textsurface, textsurface.get_rect()


def message_display(text, h, k, size):
    largetext = pg.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text, largetext)
    TextRect.center = (h, k)
    d.blit(TextSurf, TextRect)


def rgb():
    global c1, c2, c3, c1_c, c2_c, c3_c
    c1 += c1_c
    c2 += c2_c
    c3 += c3_c
    if c1 >= 255:
        c1_c = -1
        c1 = 255
    if c2 >= 255:
        c2_c = -2
        c2 = 255
    if c3 >= 255:
        c3_c = -3
        c3 = 255
    if c1 <= 100:
        c1_c = 1
        c1 = 100
    if c2 <= 100:
        c2_c = 2
        c2 = 100
    if c3 <= 100:
        c3_c = 3
        c3 = 100
    to_return = (c1, c2, c3)
    return to_return


def pause():
    global stop, mode
    stop = True
    mode = "pause"
    while stop:
        d.fill((0, 0, 0))
        draw_menu()
        message_display("! Paused !", a / 2, 75, 50)
        event_handler()
        pg.display.update()
        clock.tick(30)


def settings():
    global sett, mode
    sett = True
    mode = "settings"
    while sett:
        d.fill((0, 0, 0))
        draw_menu()
        message_display("! Settings !", a / 2, 75, 50)
        message_display("Frame Speed : ", a / 2 - 40, 150, 25)
        message_display(str(frame), a / 2 + 100, 150, 25)

        event_handler()
        pg.display.update()
        clock.tick(30)


def bullet():  # to draw and create bullets
    global bullets, bullet_time_gap, laserfuel
    i = 0
    while i < len(bullets):
        bullets[i][1] -= bulletspeed
        pg.draw.circle(d, white, (bullets[i][0], bullets[i][1]), 4)
        if bullets[i][1] < 0:
            bullets.remove(bullets[i])
            i -= 1
        i += 1

    if fire and firemode == "bullet":
        bullet_time_gap += 1
        if bullet_time_gap == 5:
            point = [x + 50, y]
            bullets.append(point)
            bullet_time_gap = 0
    if fire and firemode == "laser" and laserfuel > 0:
            pg.draw.polygon(d, color, ((x + 47, 0), (x + 53, 0), (x + 53, y), (x + 47, y)), 0)
            laserfuel -= 0.5


def enemy():  # to create new bullets and enemies
    global targets, enemy_time_gap, score
    i = 0
    while i < len(targets):
        targets[i][1] += targetspeed
        health_decrease = int(60 / health)
        t1 = targets[i][0]  # x coordinate
        t2 = targets[i][1]  # y coordinate
        t3 = targets[i][2]  # to decide if they will move horizontally also
        t4 = targets[i][3]  # to decide direction
        t5 = targets[i][4]  # health

        if t3 == 1:
            if t4 == 0:
                targets[i][0] -= 1
            elif t4 == 1:
                targets[i][0] += 1
            if t1 >= a:
                targets[i][3] = 0
            elif t1 <= 0:
                targets[i][3] = 1

        d.blit(img3, (t1, t2))
        pg.draw.polygon(d, (255, 0, 0), ((t1, t2), (60 + t1, t2), (60 + t1, t2 + 8), (t1, t2 + 8)))
        pg.draw.polygon(d, (0, 255, 0), ((t1, t2), (t5 * health_decrease + t1, t2), (t5 * health_decrease + t1, t2 + 8), (t1, t2 + 8)))

        if t2 > b:
            targets.remove(targets[i])
            i -= 1
            score -= 1

        i += 1

    if len(targets) < int(score / 10) + 5:
        enemy_time_gap += 1
        if enemy_time_gap >= 50 - int(score / 20):
            t1 = rn.randint(0, a - 60)
            t2 = 0
            t3 = rn.randint(0, 1)
            t4 = rn.randint(0, 1)
            t5 = health
            enemy_time_gap = 0
            targets.append([t1, t2, t3, t4, t5])


def crash():
    global crashed

    for i in range(0, len(targets)):
        if not crashed:
            if (targets[i][0] in range(x - 30, x + 80)) and (targets[i][1] in range(y - 30, y + 80)):
                crashed = True
                pg.draw.circle(d, (255, 255, 0), (targets[i][0] + 45, targets[i][1] + 45), 30)
                message_display("CRASHED", a / 2, b / 2, 150)
                message_display(str(score), a / 2, b / 2 + 150, 150)
                pg.display.update()
                time.sleep(3)


def kill():
    global bullets, targets, score, laserfuel
    if firemode == "laser" and laserfuel > 0 and fire:
        i = 0
        while i < len(targets):
            if (targets[i][0] in range(x - 12, x + 54)) and (targets[i][1] in range(0, y + 5)):
                targets.remove(targets[i])
                score += 1
                i -= 1
                if laserfuel < laserfuelcapacity:
                    laserfuel += 1
            i += 1

    i = 0
    while i < len(targets):
        j = 0
        while j < len(bullets):
            if i < len(targets):
                if (bullets[j][0] in range(targets[i][0], targets[i][0] + 60)) and (bullets[j][1] in range(targets[i][1] + 10, targets[i][1] + 50)):
                    bullets.remove(bullets[j])
                    targets[i][4] -= 1
                    if targets[i][4] == 0:
                        targets.remove(targets[i])
                        score += 1
                        if laserfuel < laserfuelcapacity:
                            laserfuel += 5
                    j -= 1
            j += 1
        i += 1

    i = 0
    while i < len(targets):

        if mode == "laser" and laserfuel > 0:
            if (targets[i][0] in range(x - 12, x + 54)) and (targets[i][1] in range(0, y + 5)) and fire:
                targets.remove(targets[i])
                score += 1
                i -= 1
                if laserfuel < laserfuelcapacity:
                    laserfuel += 3

        i += 1

    if score < 0:
        score = 0


def plane():
    global x, y
    if up:
        y -= 5
    if down:
        y += 5
    if right:
        x += 5
    if left:
        x -= 5
    if x > a - x1:
        x = a - x1
    if y > b - y1:
        y = b - y1
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    d.blit(img1, (x, y))


def event_handler():  # to handle input from keyboard and mouse
    global crashed, mode, sett, stop, left, down, up, right, fire, inputmode, firemode, x, y

    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True
            pg.quit()
            quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            m = pg.mouse.get_pos()
            m1 = m[0]
            m2 = m[1]
            if (m1 in range(a - 70, a - 20)) and (m2 in range(20, 70)):
                if mode == "main":
                    pause()
                else:
                    mode = "main"
                    sett = False
                    stop = False
            elif (m1 in range(a - 70, a - 20)) and (m2 in range(90, 140)):
                settings()

        if inputmode == "keyboard":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    up = True
                if event.key == pg.K_DOWN:
                    down = True
                if event.key == pg.K_LEFT:
                    left = True
                if event.key == pg.K_RIGHT:
                    right = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    up = False
                if event.key == pg.K_DOWN:
                    down = False
                if event.key == pg.K_LEFT:
                    left = False
                if event.key == pg.K_RIGHT:
                    right = False

        if inputmode == "keyboard" or inputmode == "mouse":
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    fire = True
                if event.key == pg.K_LCTRL:
                    if inputmode == "keyboard":
                        inputmode = "mouse"
                    else:
                        inputmode = "keyboard"
                if event.key == pg.K_LSHIFT:
                    if firemode == "bullet":
                        firemode = "laser"
                    else:
                        firemode = "bullet"
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    fire = False

        if inputmode == "mouse":
            x = pg.mouse.get_pos()[0]
            y = pg.mouse.get_pos()[1]


def scoring():
    global score, health, targetspeed
    if score < 0:
        score = 0
    health = 4 + int(score / 20)
    targetspeed = 1 + int(score / 50)
    frame = 60 + int(score / 4)


def engine():
    global crashed
    while not crashed:
        d.blit(img2, (0, 0))
        bullet()
        enemy()
        event_handler()
        plane()
        kill()
        plane()
        crash()
        scoring()
        draw_menu()
        pg.display.update()
        clock.tick(frame)


engine()
