# Intro to GameDev - main game file
import pgzrun
import pgzero
import mathstropy
import random

WIDTH = 1000
HEIGHT = 600

BACKGROUND_TITLE = "game_logo"
BACKGROUND_LEVEL1 = "background_level1"
BACKGROUND_LEVEL2 = "background_level2"
BACKGROUND_LEVEL3 = "background_level3"
START_IMG = "start_button"
INSTRUCTIONS_IMG = "instructions_button"
BACKGROUND_IMG = "background_level1"
PLAYER_IMG = "shippe"
JUNK_IMG = "space_debris"
SATELITE_IMG = "satellite"
LASER_IMG = "laser_red"
LASER_SPEED = -10
lvl1_LIMIT = 20
lvl2_LIMIT = 100
lvl3_LIMIT = 250
lvl4_LIMIT = 500
junk_collect = 0
music.play("exitthisearth")

SCOREBOX_HEIGHT = 60
junk_speed = 15
sat_speed = 20

player = Actor(PLAYER_IMG)
junk = Actor(JUNK_IMG)
satellite = Actor(SATELITE_IMG)

player.midright = (900, HEIGHT / 2)



# start game with title screen

START_IMG = "start_button"
INSTRUCTIONS_IMG = "instructions_button"

# initialize title screen buttons
start_button = Actor(START_IMG)
start_button.center = (WIDTH/2, 425)

instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2, 500)


def on_mouse_down(pos):
    global level, level_screen


    if start_button.collidepoint(pos):
        level = 1
    level_screen = 1

    if instructions_button.collidepoint(pos):
        level = -1

# initialize junks
junks = []
for i in range(5):
    junk = Actor(JUNK_IMG)
    x_pos = random.randint(-500, -50)
    y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
    junk.topleft = (x_pos, y_pos)
    junks.append(junk)

# Initialize lazers
lasers = []
player.laserActive = 1

#keep track of score
score = 0
level = 0
level_screen = 0


x_sat = random.randint(-500, -50)
y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
satellite.topright = (x_sat, y_sat)


def updateLasers():
    global score
    for laser in lasers:
        laser.x += LASER_SPEED
        # remove laser if moves off screen
        collision_satellite = satellite.colliderect(laser)
        if laser.right < 0:
            lasers.remove(laser)
            # check for collisions
        if satellite.colliderect( laser) == 1:
            lasers.remove(laser)
            x_sat = random.randint(-500, -50)
            y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score += -5
        if junk.colliderect(laser) == 1:
            lasers.remove(laser)
            x_debris = random.randint(-500, -50)
            y_debris = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
            junk.topright = (x_debris, y_debris)
            score += 5
        for j in junks:
            if j.colliderect(laser) == 1:
                lasers.remove(laser)
                x_debris = random.randint(-500, -50)
                y_debris = random.randint(SCOREBOX_HEIGHT, HEIGHT - j.height)
                j.topright = (x_debris, y_debris)
                score += 5



def updateSatellite():
    global score
    satellite.x += sat_speed

    collision = player.colliderect(satellite)
    if satellite.left > WIDTH:
        score += 5
    if satellite.left > WIDTH or collision == 1:
        x_sat = random.randint(-500, -50)
        y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)

    if collision == 1:
        score -= 10


def updateJunk():
    global score, junk_collect

    for junk in junks:

        junk.x += junk_speed

        collision = player.colliderect(junk)
        if (junk.left >= WIDTH):
            score -= 1

        if junk.left > WIDTH or collision == 1:

            x_pos = -50
            y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)

        if (collision == 1):
            score += 2
            junk_collect += 1

def updatePlayer():
    if (keyboard.up == 1):
        player.y = player.y + (-10)

    elif (keyboard.down == 1):
        player.y = player.y + 10
    if (player.top < 60):
        player.top = 60

    if (player.bottom > HEIGHT):
        player.bottom = HEIGHT

    if (player.left < 0):
        player.left = 0

    if (player.right > WIDTH):
        player.right = WIDTH

    if keyboard.space == 1:
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)






# activating lasers (template code)____________________________________________________________________________________________
player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list


def update():
    global level, level_screen, BACKGROUND_IMG, score, junk_collect, junk_speed, sat_speed
    if level == -1:  # instructions screen
        BACKGROUND_IMG = BACKGROUND_LEVEL1
    if score >= lvl2_LIMIT:  # level 2
        level = 2
    if score >= lvl3_LIMIT:  # level 3
        level = 3




    if level >= 1:
        if level_screen == 1:
            BACKGROUND_IMG = BACKGROUND_LEVEL1
            if keyboard.RETURN == 1:
                level_screen = 2
            updatePlayer()

            updateJunk()

        if level_screen == 2:  # level 1 gameplay
            updatePlayer()# calling our player update function
            junk_speed = 8.5
            updateJunk()  # calling junk update function

        if level == 2 and level_screen <= 3:
            BACKGROUND_IMG = BACKGROUND_LEVEL2
            level_screen = 3
            if keyboard.RETURN == 1:
                level_screen = 4
        if level_screen == 4:
            updatePlayer()
            updateLasers()
            junk_speed = 10
            sat_speed = 15
            updateJunk()
            updateSatellite()

        if level == 3 and level_screen <= 5:
            BACKGROUND_IMG = BACKGROUND_LEVEL3
            level_screen = 5
            if keyboard.RETURN == 1:
                level_screen = 6
        if level_screen == 6:
            updatePlayer()
            updateJunk()
            junk_speed = 20
            sat_speed = 25

            updateSatellite()
            updateLasers()

        if score < 0 or level == -2:  # game over or end game
            if keyboard.RETURN == 1:
                score = 0
                junk_collect = 0
                level = 0


def draw():
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0, 0))
    if level == -1:
        start_button.draw()
        show_instructions = "Use UP and DOWN arrow keys to move your player\n\npress SPACEBAR to shoot"
        screen.draw.text(show_instructions, midtop=(WIDTH / 2, 70), fontsize=35, color="white")
    if level == 0:
        start_button.draw()
        instructions_button.draw()
    if level >= 1:
        player.draw()  # draw player sprite on screen
        for junk in junks:
            junk.draw()  # draw junk sprite on screen
    if level >= 2:
        satellite.draw()
    if level == 3:
        for laser in lasers:
            laser.draw()

        # game over screen
    if score < -50:
        game_over = "GAME OVER\npress ENTER to play again"
        screen.draw.text(game_over, center=(WIDTH / 2, HEIGHT / 2), fontsize=60, color="white")

        # draw some text on the screen
    show_score = "Score: " + str(score)  # remember to convert score to a string
    screen.draw.text(show_score, topleft=(650, 15), fontsize=35, color="black")
    show_collect_value = "Junk: " + str(junk_collect)
    screen.draw.text(show_collect_value, topleft=(450, 15), fontsize=35, color="black")

    if level >= 1:
        show_level = "LEVEL " + str(level)
        screen.draw.text(show_level, topright=(375, 15), fontsize=35, color="white")

    if level_screen == 1 or level_screen == 3 or level_screen == 5:
        show_level_title = "LEVEL " + str(level) + "\nPress ENTER to continue..."
        screen.draw.text(show_level_title, center=(WIDTH / 2, HEIGHT / 2), fontsize=70, color="white")



pgzrun.go()
