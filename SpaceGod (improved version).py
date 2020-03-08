# By Jestin Varghese Cherian
# Game title: SPACE GOD 
# This is my final computer tech summative

#---------------Credits--------------------#

# Game music/background music by: Megupets
# Megupets homepage: www.megupets.com

# Game sound effects created from: http://www.bfxr.net/

# Explosion animation by: Kenney.nl
# Animation retrieved from: https://www.youtube.com/watch?v=AdG_ITCFHDI

# Other graphics retrieved from google images 
#------------------------------------------#


# import tools needed to create the game 
import pygame,sys
import random
import time

pygame.init()  # initializes Pygame

display_width = 800         # width of the display 
display_height = 600        # height of the display 

# Colors to be used for the game 
black = (0,0,0) 
white = (255,255,255)
red = (200,0,0)
bright_red = (255,0,0)
blue = (0,0,255)
green = (0,200,0)
bright_green = (0,255,0)
purple = (255,0,255)
yellow = (255,255,0)
bright_yellow = (255,255,102)

screenDisplay = pygame.display.set_mode((display_width,display_height)) # Creates the surface where the game is going to be played 

pygame.display.set_caption ("Space Shooter God") # sets the game title

clock = pygame.time.Clock() # The clock for the game

pygame.mixer.init()  # Initializes audio player 

GUNPOWERUP_TIME = 5000 # 5 sec timer for the gun power up 

# ______Global Variable_______#
Pause = False 
#_____________________________# 


#_______________________________________________Game graphics:______________________________________________________________________#
Spaceship = pygame.image.load('player.png')# The player image 
SpaceshipImg = pygame.transform.scale(Spaceship,(50,50)) # resized 

asteroid = pygame.image.load ('asteroid.png')                   # Obstacle image (asteroid)
asteroidImg = pygame.transform.scale(asteroid,(30,30))          # Resize the asteroid to 30 by 30 pixels 

spaceBackground = pygame.image.load('gamebackground.png')       # Game background  
spaceBackgroundImg = pygame.transform.scale(spaceBackground,(display_width,display_height)) # Resize the background to the width and height of the game display 
spaceBackgroundImg_rect = spaceBackgroundImg.get_rect() # creates a rectangle that encloses the image

enemyShip = pygame.image.load('enemy ship.gif') # The enemy image 
enemyShipImg = pygame.transform.scale(enemyShip,(35,35))  # Rezise the enemy image to 50 by 50 pixels 

laser = pygame.image.load('laserGreen.png') # Laser image

powerUp1 = pygame.image.load ('ShieldPowerUp.png')  # Shield power up image 
powerUp1Img = pygame.transform.scale(powerUp1,(50,50)) # Resize the shield power up image to 50 by 50 pixels  

powerUp2 = pygame.image.load('GunPowerUp.png') # Gun power up image
powerUp2Img = pygame.transform.scale(powerUp2,(50,50)) # Resize the gun power up image to 50 by 50 pixels 

# Control Graphics:
movement = pygame.image.load('movement.png') # Arrow keys image 
movementImg = pygame.transform.scale(movement,(100,100)) # Resize arrow keys image to 100 by 100 pixels

shootKey = pygame.image.load('shootKey.jpg') # Image of s key on the keyboard 
shootKeyImg = pygame.transform.scale(shootKey,(60,60)) # Resize s key to 60 by 60 pixels 

additionalKey = pygame.image.load('pKey.png') # Image of p key on the keyboard 
additionalKeyImg = pygame.transform.scale(additionalKey,(50,50)) # Resize p key to 50 by 50 pixels
#__________________________________________________________________________________________________________________________________#
# __________________________PowerUp Dictionary{}____________________________:

# NOTE TO SELF: Dictionary's are similiar to lists and can be indexed in the same way as lists, using square brackets containing keys 
# Each element in a dictionary is represented by a key:value pair 
powerUpList = {"Shield":pygame.transform.scale(powerUp1,(20,20)),       #Shield is the key and after the colon is the value stored
               "Gun":pygame.transform.scale(powerUp2,(20,20)),          # Gun is another key and after the colon is the value stored 
}               # Closes the dictionary 

# ______________________Game animation(Dictionary{})_____________________________#

explosion_animation = {}    # creates an empty dictionary
explosion_animation['asteroidBullet'] = [] # Empty key for explosion animation when asteroids and bullets collide
explosion_animation['asteroidSpaceshipType1'] =[] # Another empty key for a regular explosion animation when asteroid and spaceship collide 
explosion_animation['asteroidSpaceshipType2'] = [] # Another empty key for a special explosion animation when asteroids and spaceship collide 
for i in range (9):
    filename1 = 'regularExplosion0{}.png'.format(i)  # Goes through all the images under the name of 'regularExplosion'
    img1Load = pygame.image.load(filename1).convert() # Loads each image under 'regularExplosion' and converts it so that it can be used in pygame effectively
    img1Load.set_colorkey(black) # Makes the black transparent 
    img_1 = pygame.transform.scale(img1Load,(75,75)) # Resizes the image to 75 by 75 pixels 
    explosion_animation['asteroidBullet'].append(img_1) # Finally adds each image as a value to the 'asteroidBullet' key 

    img_2 = pygame.transform.scale(img1Load,(25,25)) # The 'regularExplosion' resized to 25 by 25 pixels 
    img_2.set_colorkey(black) # Makes black transparent 
    explosion_animation['asteroidSpaceshipType1'].append(img_2) # Finnaly adds each image as a value to the 'asteroidSpaceshipyType1' key 

    filename3 = 'sonicExplosion0{}.png'.format(i) # Goes through all the images under the name of 'sonicExplosion' 
    img3Load = pygame.image.load(filename3).convert() # Loads each image under the name of 'sonicExplosion' and converts it to be used in pygame effectively
    img_3 = pygame.transform.scale(img3Load,(75,75)) # Resizes the image to 75 by 75 pixels 
    explosion_animation['asteroidSpaceshipType2'].append(img_3) # Finally adds each image as a value to the 'asteroidSpaceshipType2' key 
    

#___________________________________________________________________#


# _________________Game Sounds_________________________#

shootSound = pygame.mixer.Sound('ShootingSound.wav') # Shoot sound for the game 
shootSound.set_volume(0.2) # Volume for the shooting sound 

powerupSound = pygame.mixer.Sound('PowerupSound.wav') # Power up sound for the game 
powerupSound.set_volume(0.2) # Volume for the power up sound 

explosionSound = pygame.mixer.Sound('ExplosionSound.wav') # Explosion sound for the game 
explosionSound.set_volume(0.2) # Volume for the explosion sound 

specialExplosionSound = pygame.mixer.Sound('SpecialExplosionSound.wav') # Special explosion sound for the game 
specialExplosionSound.set_volume(0.2) # Volume for the special explosion sound 

backgroundMusic = pygame.mixer.Sound('gameMusic.wav') # Background music for the game 
backgroundMusic.set_volume(0.6) # Volume for the background music sound 

#Background music loop:
backgroundMusic.play(loops = -1) # Loops the background music 



#_____________________________________________________# 



# Functions(methods):

def text_objects(text,font):    # Define function name 'text_objects', passing 'text' and 'font' as the parameter 
    textSurface = font.render(text,True,white) # Draws text on a new surface 
    return textSurface,textSurface.get_rect() # Returns the text surface and the rectangle enclosing the text 

def message_display(text,size): # Define function name 'message_display', passing 'text' and 'size' as the parameter 
    largeText = pygame.font.Font ('freesansbold.ttf',size) # Uses freesansbold.ttf font and user specified size 
    TextSurf,TextRect = text_objects(text,largeText) # Text and large text used for the text_objects function
    TextRect.center = ((display_width/2),(display_height/2)) # Placement in the middle of the screen
    screenDisplay.blit(TextSurf,TextRect) # Copy to the screenDisplay 
    pygame.display.update() # Updates the screen 

def scoringSYS (count): # Define function name 'scoringSYS', passing 'count' as the parameter 
    font = pygame.font.SysFont(None,25) # Create a font object using the system font 
    text = font.render("Score: " + str(count),True, white) # Draws text 
    screenDisplay.blit(text, (0,0)) # Places the image on (0,0) on screenDisplay 
    return count # Returns count  

def LevelUpMessage(x): # Define function name 'LevelUpMessage', passing 'x' as the parameter 
    font = pygame.font.SysFont(None,25) # Create a font object using the system font 
    text = font.render("Wave " + str(x),True,white) # Draws text 
    screenDisplay.blit(text,(700,0)) # Place text on (700,0) on the screenDisplay 

def textDisplay(text,textSize,x,y,color): #Define function name 'textDisplay', passing 'text','textSize','x','y',and 'color' as the parameter 
    font = pygame.font.SysFont(None,textSize) # Create a font object using the system font 
    write = font.render(str(text),True,color) # Draws text 
    screenDisplay.blit(write,(x,y)) # Places text on (x,y) on the screenDisplay 
    
def newAsteroids(): # Define function name 'newAsteroids' with empty parameters 
    astr = asteroids() # Creates an asteroid 
    game_sprites.add(astr) # Adds the asteroid to the game_sprites group 
    obstacle_sprites.add(astr) # Adds the asteroid to obstacle_sprites group

def newEnemy(): # defined function name 'newEnemy' with empty parameters 
    enemy = Enemy() # variable for the Enemy sprite class 
    game_sprites.add(enemy) # adds the enemy to the game sprites group 
    enemy_sprites.add(enemy) # adds the enemy to the enemy sprites group 
    
    

def healthBar(surf,x,y,HealthStatus): # Define function name 'healthBar', passing 'surf','x','y', and'healthStatus' as the parameters 
    HealthBarLENGTH = 50 # Length of the health bar is 50 pixels 
    HealthBarWIDTH = 5   # Width of the health bar is 5 pixels 

    if HealthStatus < 0: # Keeps the healthStatus at 0 if healthStatus goes less than 0 
        HealthStatus = 0

    if HealthStatus > 75: # Color of the healthStatus is green if healthStatus is more than 75 
        HealthColor = green

    elif HealthStatus > 50: # Color of the healthStatus is yellow if health is more than 50 
        HealthColor = yellow

    else:
        HealthColor = red # Else color is red if healthStatus below 50 
    
        
    display_healthCalc = (HealthStatus/100) * HealthBarLENGTH # Calculates were the player's health is on the health bar 
    healthBar_outline = pygame.Rect(x,y,HealthBarLENGTH,HealthBarWIDTH) # Creates a rectangle representing the health bar 
    fill_healthBar = pygame.Rect(x,y,display_healthCalc,HealthBarWIDTH) # Creates a rectangle representing the player health status 
    pygame.draw.rect(surf,HealthColor,fill_healthBar) # Draws the player's health status 
    pygame.draw.rect(surf,white,healthBar_outline,2) # Draws the health bar with white outline of a thickness of 2 

def gameIntro(): # Define function by the name 'gameIntro' with empty parameters 
    spaceBackground = pygame.image.load('gamebackground.png') # Load game background image 
    spaceBackgroundImg = pygame.transform.scale(spaceBackground,(display_width,display_height)) # Resizes the image to display height and width 
    spaceBackgroundImg_rect = spaceBackgroundImg.get_rect() # Creates a rectangle enclosing the spaceBackgroundImg 

    background1X = 0 # x location of the first space background image 
    background1Y = 0 # y location of the first space background image 

    background2X = 0 # x location of the second space background image 
    background2Y = -display_height # y location of the second space background image 

    # Loop:
    IntroRun = True 
    while IntroRun:
        for event in pygame.event.get():           # Captures any events 
            if event.type == pygame.QUIT:          # Checks if user wants to quit 
                pygame.quit() # Runs if the user wants to quit 
                quit()


        background1Y += 8 # Increases the y location of the first space background image by 8 
        background2Y += 8 # Increases the y location of the second space background image by 8

        screenDisplay.blit(spaceBackgroundImg,(background1X,background1Y)) # Copy the first background image to the screenDisplay  
        screenDisplay.blit(spaceBackgroundImg,(background2X,background2Y)) # Copy the second background image to the screenDisplay 

        if background1Y > display_height: # Checks if the y location of the first background image has exceeded the display height 
            background1Y = -display_height # Moves the y location of the first background image to -display_height(-600) 

        if background2Y > display_height: # Checks if the y location of the second background image has exceeded the display height 
            background2Y = -display_height # Moves the y location of the second background image to - display_height(-600) 
        

        mousePos = pygame.mouse.get_pos() # Gets the mouse position 
        mouseClick = pygame.mouse.get_pressed() # Gets the mouse press 

        if 150 + 100 > mousePos[0] > 150 and 500 + 50 > mousePos[1] > 500:  # Checks if the mouse position is on the stated boundaries
            pygame.draw.rect(screenDisplay,bright_green,(150,500,100,50)) # Draws a rectangle bright green in color if true  
            if mouseClick[0] == 1:  # Checks to see if the user has clicked in the boundaries 
                gameLoop() # Runs the game loop 
        else:
            pygame.draw.rect(screenDisplay,green,(150,500,100,50)) # If not in the boundaries the draws a rectangle green in color 


        if 350 + 100 > mousePos[0] > 350 and 500 + 50 > mousePos[1] > 500: # Checks if the mouse position is on the stated boundaries
            pygame.draw.rect(screenDisplay,bright_yellow,(350,500,100,50)) # Draws a rectangle bright yellow in color if true 
            if mouseClick[0] == 1: # Checks to see if the user has clicked in the boundaries 
                controls() # Runs the controls function showing the contorls of the game 
        else:
            pygame.draw.rect(screenDisplay,yellow,(350,500,100,50)) # If not in the boundaries then draws a rectangle yellow in color 


        if 550 + 100 > mousePos[0] > 550 and 500 + 50 > mousePos[1] > 500: # Checks if the mouse position is on the stated boundaries
            pygame.draw.rect(screenDisplay,bright_red,(550,500,100,50)) # Draws a rectangle bright red in color if true 
            if mouseClick[0] == 1: # Checks to see if the user has clicked in the boundaries 
                pygame.quit() # Quits 
                quit()
        else:
            pygame.draw.rect(screenDisplay,red,(550,500,100,50)) # If not in the boundaries then draws a rectangle red in color 

        textDisplay("Begin",30,173,519,black) # Draws text on the green box
        textDisplay("Controls",30,357,519,black) # Draws text on the yellow box 
        textDisplay("Quit",30,577,519,black) # Draws text on the red box 

        textDisplay("By Jestin Varghese Cherian",25,570,575,purple) # Draws text in purple showing the name of the creator of the game 

        
        
        message_display("SPACE GOD",115) # Draws text in big font displaying the game title 
        

        pygame.display.update() # Updates the screen 
        clock.tick(50) # Updates 50 frames per second 
        


def gamePause(): # Define function 'gamePause' with no parameters 
    spaceBackground = pygame.image.load('gamebackground.png') # Load game background image 
    spaceBackgroundImg = pygame.transform.scale(spaceBackground,(display_width,display_height)) # Resize the background image to display height and width 
    spaceBackgroundImg_rect = spaceBackgroundImg.get_rect() # Creates a rectangle enclosing the image 

    background1X = 0 # x location of the first space background image
    background1Y = 0 # y location of the first space background image

    background2X = 0 # x location of the second space background image
    background2Y = -display_height # y location of the second space background image

    global Pause # Global variable 

    # Loop:
    while Pause:
        for event in pygame.event.get(): # Checks for events 
            if event.type == pygame.QUIT: # Checks if the event is quit 
                pygame.quit() # Quits 
                quit()
            if event.type == pygame.KEYDOWN: # Checks for key presses 
                if event.key == pygame.K_p: # Checks if the p key is pressed 
                    unpause() # Runs the unpause function which unpauses the game 


        background1Y += 8 # Increases the y location of the first space background image by 8 
        background2Y += 8 # Increases the y location of the second space background image by 8 

        screenDisplay.blit(spaceBackgroundImg,(background1X,background1Y)) # Copy the first background image to the screenDisplay 
        screenDisplay.blit(spaceBackgroundImg,(background2X,background2Y)) # Copy the second background image to the screenDisplay 

        if background1Y > display_height: # Checks if the y location of the first background image has exceeded the display height
            background1Y = -display_height # Moves the y location of the first background image to -display_height(-600)

        if background2Y > display_height: # Checks if the y location of the second background image has exceeded the display height
            background2Y = -display_height # Moves the y location of the second background image to -display_height(-600)

        mousePos = pygame.mouse.get_pos() # Gets the mouse position
        mouseClick = pygame.mouse.get_pressed() # Gets mouse presses

        if 150 + 100 > mousePos[0] > 150 and 500 + 50 > mousePos[1] > 500: # Checks if the mouse position is on the stated boundaries
            pygame.draw.rect(screenDisplay,bright_green,(150,500,100,50)) # Draws a rectangle bright green in color if true
            if mouseClick[0] == 1: # Checks to see if the user has clicked in the boundaries
                unpause()  # Runs the unpause function which unpauses the game 
        else:
            pygame.draw.rect(screenDisplay,green,(150,500,100,50)) # If not in the boundaries the draws a rectangle green in color 


        if 550 + 100 > mousePos[0] > 550 and 500 + 50 > mousePos[1] > 500: # Checks if the mouse position is on the stated boundaries
            pygame.draw.rect(screenDisplay,bright_red,(550,500,100,50)) # Draws a rectangle bright red in color if true 
            if mouseClick[0] == 1: # Checks to see if the user has clicked in the boundaries
                pygame.quit() # Quits
                quit()
        else:
            pygame.draw.rect(screenDisplay,red,(550,500,100,50)) # If not in the boundaries then draws a rectangle red in color

        textDisplay("Resume",30,163,519,black) # Draws text on the green box
        textDisplay("Controls",30,357,519,black) # Draws text on the yellow box
        textDisplay("Quit",30,577,519,black) # Draws text on the red box

        message_display("SPACE GOD",115) # Draws text in big font displaying the game title

        pygame.display.update() # Updates the screen
        clock.tick(50) # Updates 50 frames per second 
        

def unpause():  # Define function 'unpause' with no parameters
    global Pause # Stating the global variable 
    Pause = False # Changes the global variabel(True) to False 

def controls(): # Define function 'controls' with no parameters
    spaceBackground = pygame.image.load('gamebackground.png') # Load game background image
    spaceBackgroundImg = pygame.transform.scale(spaceBackground,(display_width,display_height)) # Resize the background image to display height and width
    spaceBackgroundImg_rect = spaceBackgroundImg.get_rect() # Creates a rectangle enclosing the image

    background1X = 0 # x location of the first space background image
    background1Y = 0 # y location of the first space background image

    background2X = 0 # x location of the second space background image
    background2Y = -display_height # x location of the second space background image

    #Loop:
    Controls = True
    while Controls:
        for event in pygame.event.get(): # Checks for events
            if event.type == pygame.QUIT: # Checks if the event is quit 
                pygame.quit() #Quits 
                quit()


        background1Y += 8 # Increases the y location of the first space background image by 8
        background2Y += 8 # Increases the y location of the second space background image by 8

        screenDisplay.blit(spaceBackgroundImg,(background1X,background1Y)) # Copy the first background image to the screenDisplay
        screenDisplay.blit(spaceBackgroundImg,(background2X,background2Y)) # Copy the second background image to the screenDisplay

        if background1Y > display_height: # Checks if the y location of the first background image has exceeded the display height
            background1Y = -display_height # Moves the y location of the first background image to -display_height(-600)

        if background2Y > display_height: # Checks if the y location of the second background image has exceeded the display height
            background2Y = -display_height # Moves the y location of the second background image to -display_height(-600)

        mousePos = pygame.mouse.get_pos() # Gets the mouse position
        mouseClick = pygame.mouse.get_pressed() # Gets mouse presses

        if 150 + 100 > mousePos[0] > 150 and 500 + 50 > mousePos[1] > 500: # Checks if the mouse position is on the stated boundaries
            pygame.draw.rect(screenDisplay,bright_green,(150,500,100,50)) # Draws a rectangle bright green in color if true
            if mouseClick[0] == 1:  # Checks to see if the user has clicked in the boundaries
                gameLoop()  # Runs the game loop
        else:
            pygame.draw.rect(screenDisplay,green,(150,500,100,50)) # If not in the boundaries the draws a rectangle green in color


        if 550 + 100 > mousePos[0] > 550 and 500 + 50 > mousePos[1] > 500: # Checks if the mouse position is on the stated boundaries
            pygame.draw.rect(screenDisplay,bright_red,(550,500,100,50)) # Draws a rectangle bright red in color if true
            if mouseClick[0] == 1:  # Checks to see if the user has clicked in the boundaries
                pygame.quit() # Quit
                quit()
        else:
            pygame.draw.rect(screenDisplay,red,(550,500,100,50)) # If not in the boundaries the draws a rectangle red in color

        textDisplay("Begin",30,173,519,black) # Draws text on the green box
        textDisplay("Quit",30,577,519,black) # Draws text on the red box

        textDisplay("Controls",110,250,50,white) # Draws text on screenDisplay

        textDisplay("Movement:",50,50,200,white) # Draws text on screenDisplay
        screenDisplay.blit(movementImg,(400,150)) # Copy image on screenDisplay 

        textDisplay("Shoot:",50,50,300,white) # Draws text on screenDisplay
        screenDisplay.blit(shootKeyImg,(420,275)) # Copy image on screenDisplay 

        textDisplay("Additional Key:",50,50,400,white) # Draws text on screenDisplay
        textDisplay("<---- Pause and unpause",35,500,400,white) # Draws text on screenDisplay
        screenDisplay.blit(additionalKeyImg,(425,390))  # Copy image on screenDisplay 

        pygame.display.update() # Updates the screen
        clock.tick(50) # Updates 50 frames per second 

def gameOutro(score): # Define function 'controls', passing 'score' as the parameter 
    spaceBackground = pygame.image.load('gamebackground.png')  # Load game background image
    spaceBackgroundImg = pygame.transform.scale(spaceBackground,(display_width,display_height)) # Resize the background image to display height and width
    spaceBackgroundImg_rect = spaceBackgroundImg.get_rect() # Creates a rectangle enclosing the image

    background1X = 0 # x location of the first space background image
    background1Y = 0 # y location of the first space background image

    background2X = 0 # x location of the second space background image
    background2Y = -display_height # y location of the second space background image

    # Loop:
    IntroRun = True
    while IntroRun:
        for event in pygame.event.get(): # Checks for events
            if event.type == pygame.QUIT: # Checks if the event is quit
                pygame.quit() #Quit
                quit()


        background1Y += 8 # Increases the y location of the first space background image by 8
        background2Y += 8 # Increases the y location of the second space background image by 8

        screenDisplay.blit(spaceBackgroundImg,(background1X,background1Y)) # Copy the first background image to the screenDisplay
        screenDisplay.blit(spaceBackgroundImg,(background2X,background2Y)) # Copy the second background image to the screenDisplay

        if background1Y > display_height: # Checks if the y location of the first background image has exceeded the display height
            background1Y = -display_height # Moves the y location of the first background image to -display_height(-600)

        if background2Y > display_height: # Checks if the y location of the second background image has exceeded the display height
            background2Y = -display_height # Moves the y location of the second background image to -display_height(-600)
        

        mousePos = pygame.mouse.get_pos() # Gets the mouse position
        mouseClick = pygame.mouse.get_pressed() # Gets mouse presses

        if 150 + 100 > mousePos[0] > 150 and 500 + 50 > mousePos[1] > 500: # Checks if the mouse position is on the stated boundaries
            pygame.draw.rect(screenDisplay,bright_green,(150,500,100,50)) # Draws a rectangle bright green in color if true
            if mouseClick[0] == 1: # Checks to see if the user has clicked in the boundaries
                gameLoop() # Runs the game loop
        else:
            pygame.draw.rect(screenDisplay,green,(150,500,100,50))


        if 550 + 100 > mousePos[0] > 550 and 500 + 50 > mousePos[1] > 500: # Checks if the mouse position is on the stated boundaries
            pygame.draw.rect(screenDisplay,bright_red,(550,500,100,50)) # If not in the boundaries the draws a rectangle red in color
            if mouseClick[0] == 1: # Checks to see if the user has clicked in the boundaries
                pygame.quit() # Quit 
                quit()
        else:
            pygame.draw.rect(screenDisplay,red,(550,500,100,50)) # If not in the boundaries the draws a rectangle red in color

        textDisplay("Restart",30,165,519,black) # Draws text on the green box
        textDisplay("Quit",30,577,519,black) # Draws text on the red box
        textDisplay("Your score is: " + str(score),50,283,400,white) # Draws text on the screenDisplay 

        
        
        message_display("SPACE GOD",115) # Draws text in big font displaying the game title
        

        pygame.display.update() # Updates the screen
        clock.tick(50)  # Updates 50 frames per second 
    
    
    
#______________________________________________________________#

# _________________________________Game classes___________________________________________________________:

# Note to self:
# 1) The init function is called when an object of the class is created, using the class name as a function
# 2) All methods should have self as their first parameters
# self refers to instance calling the method 

class Player(pygame.sprite.Sprite): # Create player class that uses sprites  
    def __init__(self): # The class constructor  
        pygame.sprite.Sprite.__init__(self) # Initialize sprites 
        self.image = SpaceshipImg # Image of the player
        self.rect = self.image.get_rect()# Rectangle encloses the image of the player
        self.radius = 21 # Radius for the player 
        self.rect.centerx = display_width * 0.5 # Initial x location of the player 
        self.rect.bottom = display_height * 0.9 # Initial y location of the player 
        self.changeX = 0 # Initial change in x coordinates 
        self.changeY = 0 # Initial change in y coordinates 
        self.player_health = 100 # Initial player health 
        self.fireLvl = 1 # Initial bullet per click  
        self.fireLvlTimer = pygame.time.get_ticks() # Timer 
        

    def update(self): # function that takes the player sprite through changes 
        if self.fireLvl >= 2 and pygame.time.get_ticks() - self.fireLvlTimer > GUNPOWERUP_TIME: # checks if 5 seconds have elapsed 
            self.fireLvl -= 1 # Decreases the bullet per click by 1 
            fireLvlTimer = pygame.time.get_ticks() # Reset the timer 

        self.changeX = 0 # Initial change in x coordinates 
        self.changeY = 0 # Initial change in y coordinates 

        user_keypress = pygame.key.get_pressed() # Checks if keys have been pressed 

        if user_keypress[pygame.K_LEFT]: # Checks if the user has pressed the left key 
            self.changeX = -5 # Change x coordinate by -5 (move left)

        if user_keypress[pygame.K_RIGHT]: # Checks if the user has pressed the right key
            self.changeX = 5 # change x coordinate by 5 (move right) 

        if user_keypress[pygame.K_UP]: # Checks if the user has pressed the up key 
            self.changeY = -5 # Change the y coordinate by - 5 (move up) 

        if user_keypress[pygame.K_DOWN]: # Checks if the user has pressed the down key 
            self.changeY = 5 # Change y coordinate by 5 (move down) 

        if self.rect.right > display_width: # Check if the right side of the player has exceeded the display_width(800) 
            self.rect.right = display_width # If True then player's right x coordinates will be display_width(800) 

        if self.rect.left < 0: # Check if the left side of the player has exceeded 0 
            self.rect.left = 0 # If True then player's left x coordinates will be 0 

        if self.rect.bottom > display_height: # Check if the bottom of the player has exceeded the display_height(600) 
            self.rect.bottom = display_height # If True then player's bottom y coordinates will be display_height (600) 

        if self.rect.top < 0: # Check if the top of the player has exceeded 0 
            self.rect.top = 0 # If True then player's top y coordinates will be 0

        self.rect.x += self.changeX # Makes changes in the x coordinate of the player 
        self.rect.y += self.changeY # Makes changes in the y coordinates of the player 

    def gunPowerUp(self): # Define function by the name 'gunPowerUp', with 'self' as the parameter 
        self.fireLvl += 1 # Fire level increase by 1 
        self.fireLvlTimer = pygame.time.get_ticks() # Tracking time

    def shoot(self): # Define function by the name 'shoot', with 'self' as the parameter 
        if self.fireLvl == 1: # Check if the fire level is one 
            bullet = Bullet(self.rect.centerx, self.rect.top) # If True make bullet appear at the center and at the top of the player sprite 
            game_sprites.add(bullet)# Add bullet to the game sprites 
            bullet.add(bullet_sprites) # Add bullet to the bullet sprite 
        if self.fireLvl == 2: # Check if the fire level is two 
            bullet1 = Bullet(self.rect.left, self.rect.centery) # spawns a bullet at the left and center y of the player 
            bullet2 = Bullet(self.rect.right, self.rect.centery) # spawns a bullet at the right and center y of the player 
            game_sprites.add(bullet1) # adds the bullet1 to game sprites group 
            game_sprites.add(bullet2) # adds bullet2 to game sprites group 
            bullet1.add(bullet_sprites) # adds bullet1 to bullet sprites group 
            bullet2.add(bullet_sprites) # adds bullet2 to bullet sprites group 
        elif self.fireLvl >= 3: # check if the fire level is two 
            bullet1 = Bullet(self.rect.left, self.rect.centery) # spawns the bullet at the left and center y of the player 
            bullet2 = Bullet(self.rect.right, self.rect.centery) # spawns the bullet at the right and center y of the player 
            bullet3 = Bullet(self.rect.centerx, self.rect.top) # spawns the bullet at the center x and top of the player 
     # adds all three bullets into game sprites group and bullet sprites group 
            game_sprites.add(bullet1) 
            game_sprites.add(bullet2)
            game_sprites.add(bullet3)
            bullet1.add(bullet_sprites)
            bullet2.add(bullet_sprites)
            bullet3.add(bullet_sprites)
            
# Enemy class sprite:             
class Enemy(pygame.sprite.Sprite): 
    def __init__(self):
        # init function declares all the variables that will be used for the sprite to function 
        pygame.sprite.Sprite.__init__(self)
        self.image = enemyShipImg
        self.rect = self.image.get_rect()
        self.radius = 22
        self.rect.x = random.randint(0,display_width - self.rect.width)
        self.rect.y = random.randint(-100,-50)
        self.speedY = random.randint(1,3)
        self.speedX = 2
        self.fireLvl = 1
        

    def update(self):
    # create how the sprite is going to function 
        self.rect.y += self.speedY
        self.rect.x += self.speedX
        if self.rect.top > display_height + 10:
            self.rect.x = random.randint(0,display_width - self.rect.width)
            self.rect.y = random.randint(-100,-50)
            self.speedY = random.randint(1,3)

        if self.rect.right > display_width: # Check if the right side of the player has exceeded the display_width(800)
            self.speedX = -2

        if self.rect.left < 0: # Check if the left side of the player has exceeded 0
            self.speedX = 2
# EnemyShoot function makes the enemy sprite shoot only one bullet at a time 
    def EnemyShoot(self):
        if self.fireLvl == 1:
            bullet_1 = Bullet(self.rect.centerx,self.rect.top)
            game_sprites.add(bullet)# Add bullet to the game sprites 
            bullet.add(bullet_sprites) # Add bullet to the bullet sprite 
        
        

# asteroid class sprite: 
class asteroids(pygame.sprite.Sprite):
    # init function declares all the variables that will be used for the sprite to function 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroidImg
        self.rect = self.image.get_rect()
        self.radius = 14
        self.rect.x = random.randint(0,display_width - self.rect.width)
        self.rect.y = random.randint(-100,-50)
        self.speedY = random.randint(1,8)

    def update(self):
        # How the sprite is going to function 
        self.rect.y += self.speedY # adds the speed to the y of the image everytime through the loop 
        if self.rect.top > display_height + 10: # if top of the image exceeds the display height 
            self.rect.x = random.randint(0,display_width - self.rect.width) # randomly generate x 
            self.rect.y = random.randint(-100,-50) # randomly generate y 
            self.speedY = random.randint(1,8) # randomly generate speed of asteroids 

class Bullet(pygame.sprite.Sprite):
     # init function declares all the variables that will be used for the sprite to function 
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedY = -10

    def update(self):
        self.rect.y += self.speedY # the speed added to the y of the image 
        if self.rect.bottom < 0: # if the bottom of the bullet exceeds 0 
            self.kill() # remove the sprite

class Explosion(pygame.sprite.Sprite):
     # init function declares all the variables that will be used for the sprite to function 
    def __init__(self,center,typeExplo):
        pygame.sprite.Sprite.__init__(self)
        self.typeExplo = typeExplo
        self.image = explosion_animation[self.typeExplo][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        current = pygame.time.get_ticks()
        if current - self.last_update > self.frame_rate:   # runs through all the frames of the animation 
            self.last_update = current
            self.frame += 1
            if self.frame == len(explosion_animation[self.typeExplo]): # if it is the last frame then remove the animation 
                self.kill()
            else:
                center = self.rect.center # spawn at the center 
                self.image = explosion_animation[self.typeExplo][self.frame] # type of explosion 
                self.rect = self.image.get_rect()
                self.rect.center = center


class PowerUps(pygame.sprite.Sprite):
    # init function declares all the variables that will be used for the sprite to function 
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['Shield','Gun'])
        self.image = powerUpList[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
        

    def update(self):
        self.rect.y += self.speedy # makes it go down 
        if self.rect.top > display_height: # if if power up exceed the display height 
            self.kill() # remove the power up 


                
                
                
        
        
          
# ______________________________________________________________________________#    
        
        
# ---------------Sprites Group---------------# 
game_sprites = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
powerups_sprites = pygame.sprite.Group()

player = Player()
game_sprites.add(player)
#---------------------------------------------# 

# ------enemy spawn-------# 
for i in range (10):
    newEnemy()

  
# Game loop: 
def gameLoop():
     user_exit = False
     running = True 
     Score = 0
     AstNum = 8
     countLvl = 0
     global Pause

     for i in range (8): # spawns the asteroids 
         newAsteroids()

     while not user_exit:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 quit()  

             elif event.type == pygame.KEYDOWN: # checks for key presses 
                 if event.key == pygame.K_s: # if s is pressed 
                     shootSound.play() # play the shoot sound 
                     player.shoot() # player shoots a bullet 
                 if event.key == pygame.K_p: # if p is pressed 
                     Pause = True # pause is True 
                     gamePause() # runs the gamePause function 

     
             
                     

      
         game_sprites.update() # Updates the sprites
         # Collision detection: 
         collisionWithPlayer = pygame.sprite.spritecollide(player,obstacle_sprites,True,pygame.sprite.collide_circle) # checks if player and obstacle sprites have collided and deletes the obstacle sprite 
         collisionWithBullet = pygame.sprite.groupcollide(obstacle_sprites,bullet_sprites,True,True) # checks if the groups have collided and deletes both sprites if it has 
         collisionWithPowerUps = pygame.sprite.spritecollide(player,powerups_sprites,True) # checks if player and power up has collided and deletes the powerup 
         collisionWithEnemy = pygame.sprite.spritecollide(player,enemy_sprites,True,pygame.sprite.collide_circle) # checks if player and enemy sprites have collided and deletes the enemy - uses circle collision 
         collisionWithBulletANDEnemy = pygame.sprite.groupcollide(bullet_sprites,enemy_sprites,True,True) # checks if bullet and enemies have collided and delets both if they have 
         
          

         for collisions in collisionWithBullet:
             explosion = Explosion(collisions.rect.center,'asteroidBullet') # create and explosion animation 
             explosionSound.play() # play explosion sound 
             game_sprites.add(explosion) # add the explosion to the game sprites group
             Score+=1 # increase the score 
             number = random.randint(1,11) # randomly generate a number between 1 and 10 
             if number == 1: # if number is 1 
                 powerUp = PowerUps(collisions.rect.center) # spawn a power up at the center of the asteroid 
                 game_sprites.add(powerUp) # add the power up to game sprites group 
                 powerups_sprites.add(powerUp) # add the power up to power up group 

             if Score == 0: # if score is 0 
                 LevelUpMessage(countLvl) # displays 0 
                 
             elif Score % 100 == 0: # if score remainder is 0 
                 countLvl +=1 # levelup by 1 
                 LevelUpMessage(countLvl) # shows the message 
                 AstNum += 1 # increase the number of asteroids by 1 
                 for i in range (AstNum): # creates the asteroids 
                     newAsteroids()
             else:
                 newAsteroids() # if nothing is true then continue creating asteroids 

         for collision in collisionWithPowerUps:
             if collision.type == 'Shield': # if shield power up collides with the player 
                powerupSound.play() # play powerup sound 
                player.player_health += random.randint(10,30) # randomly generate player's health between 10 and 30 
             if player.player_health >= 100: # checks if player's health exceeds 100 
                 player.player_health = 100 # keeps the health at 100 
             if collision.type == 'Gun': # if gun power up collides with the player 
                 powerupSound.play() # play the power up sound 
                 player.gunPowerUp() # gun powerup 

         for collisions in collisionWithEnemy:
             explosion2 = Explosion(collisions.rect.center,'asteroidSpaceshipType1') # spawns an explosion at the center of the player
             explosionSound.play() # plays the explosion sound 
             game_sprites.add(explosion2) # adds the explosion to the game sprites group 
             player.player_health -= 10 # reduces player health by 10
             newEnemy() # spawns new enemies 
             if player.player_health == 0 : # checks if player health is 0 
                 specialExplosion = Explosion(player.rect.center,'asteroidSpaceshipType1') # plays the special explosion animation at the center of the player
                 specialExplosionSound.play() # plays the explosion sound 
                 game_sprites.add(specialExplosion) # adds the specialexplosion to the game sprites group 
                 player.kill() # removes the player 
            
            
                 
                 
         for hits in collisionWithPlayer: 
             explosion2 = Explosion(hits.rect.center,'asteroidSpaceshipType1') # creates an explosion at the center of the player 
             explosionSound.play() # plays the explosion sound 
             game_sprites.add(explosion2) # adds the explosion to the game sprites group 
             player.player_health -= 10 # reduces player health by 10 
             newAsteroids() # creates new asteroids 
             if player.player_health == 0 : # if player health is 0 
                 specialExplosion = Explosion(player.rect.center,'asteroidSpaceshipType2') # play the special explosion animation 
                 specialExplosionSound.play() # play the explosion sound 
                 game_sprites.add(specialExplosion) # add the special explosion to the game sprites group 
                 player.kill() # remove the player 

         for collisions in collisionWithBulletANDEnemy:  
             explosion2 = Explosion(collisions.rect.center,'asteroidSpaceshipType2') # creates an explosion animation at the center of the enemy
             Score += 1
             explosionSound.play() # plays explosion sound 
             game_sprites.add(explosion2) # adds the explosion to the game sprites group 
             newEnemy() # function that creates new enemies 
             
                 
         if player not in game_sprites and specialExplosion not in game_sprites: 
             gameOutro(Score) # plays the gameOutro 



             
             
              

         screenDisplay.fill(black) # fill with black
         screenDisplay.blit(spaceBackgroundImg,spaceBackgroundImg_rect)# background of the game 
         game_sprites.draw(screenDisplay) # draws everything in the gamesprites group on screen display 
         scoringSYS(Score) # keeps track of the score 
         healthBar(screenDisplay,player.rect.x + 50,player.rect.y,player.player_health) # keeps track of the health bar 
         LevelUpMessage(countLvl) # keeps track when to show level up
         pygame.display.update() # updates the screen 
         clock.tick(60) # 60 frames per second 

gameIntro()
gameLoop()     
        
        
        
        








