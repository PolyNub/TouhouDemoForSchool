import pygame
import pygame.freetype
import math
import random

from pygame.locals import * # so we have some local variables idk

# I just realized how fu#@ed this project is, I can't submit this I spent so much time using sprites that I never even used a list.
# Pygame might just be the worst thing I've ever gotten myself in..

def firePlayerBullet(self, x, y, type):
    self.bulletGroup.add(PlayerBullet(x, y, type))
    return

def changeKunaiColor(type):
    if type == 0:
        return KUNAI_IMG
    elif type == 1:
        return KUNAI2_IMG
    return KUNAI_IMG

def spellcardGraphic(text, img):
    newSpellcard = Spellcard(text, img)
    spellcardGroup.add(newSpellcard)
    return

def attackName(attackNumber):
    text = ''
    
    if attackNumber == 1:
        text = 'Mutant Sign - \'Barrage\''
    elif attackNumber == 2:
        text = 'Burst Spell - \'Shift\''
    elif attackNumber == 3:
        text = 'Perfect Sign - Kunai Imitation'
    elif attackNumber == 4:
        text = 'Dying Hope - Scope Explosion'

    return text

def winText(deathCount):
    
    text = ''
    
    if deathCount < 1:
        text = 'you won, no deaths so good job'
    else:
        text = "you won, you died "+str(deathCount)+" time(s), do a no hit run now haha"
    return text

# ==== PLAYER BULLET SPRITE
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x,y, type, radius=10,):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.dir = 0
        
        # Rect for collisions
        self.radius = radius
        self.rect = pygame.Rect(self.x - radius, self.y - radius, radius * 2, radius * 2)
        
        self.type = type # 0 equals regular, 1 equals homing
        
    def update(self):
        
        if self.type == 0:
            self.y -= 20
            self.rect.center = (self.x, self.y) #DO NOT FORGET TO UPDATE THE RECT OF THE BULLET ONCE YOU MOVE THE Y
            
        elif self.type == 1:
            
            self.dir = math.atan2(newBoss.y - self.y, newBoss.x - self.x) # Point toward direction of boss
            speed = 12
            self.x += math.cos(self.dir) * speed
            self.y += math.sin(self.dir) * speed
            
            self.rect.center = (self.x, self.y)
            
        if self.y < -50:
            self.kill()
    
    def show(self, surface):
        
        showBulletHitbox = False
        if showBulletHitbox == True:
            pygame.draw.circle(surface, (255,0,255), (self.x, self.y), self.radius)

# ==== PLAYER SPRITE
class Player(pygame.sprite.Sprite):
    def __init__(self, x,y, bulletGroup, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = image
        
        self.focus = False
        self.speed = 8
        self.bulletGroup = bulletGroup
        self.eTime = 0
        self.cooldown = 50  
        
        self.focusFire = 0 # so i can toggle how much homing bullets is spawned when shooting
        
        self.rect = pygame.Rect(self.x - 5, self.y - 5, 5 * 2, 5 * 2)
        
    def update(self):
        
        keys = pygame.key.get_pressed()

        # focus mode
        
        if keys[K_LSHIFT]:
            self.focus = True
        else:
            self.focus = False
        
        if self.focus == True: 
            self.speed = 3
        else: 
            self.speed = 8

        # movement
        # the "self.x/y > 0 is just for collision so the sprite doesn't go offscreen"
        if keys[K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[K_RIGHT] and self.x < WIN_WIDTH:
            self.x += self.speed
        if keys[K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[K_DOWN] and self.y < WIN_HEIGHT:
            self.y += self.speed

        # shooting
        if keys[K_z]:
            now = pygame.time.get_ticks()
            if now - self.eTime > self.cooldown:
                self.eTime = now
                # regular centered 
                firePlayerBullet(self, self.x-10, self.y, 0)
                firePlayerBullet(self, self.x+10, self.y, 0)
                
                self.focusFire += 1
                
                # homing bullet stuff
                if self.focus == True and self.focusFire > 2:  
                    firePlayerBullet(self, self.x-40, self.y+20, 1)
                    firePlayerBullet(self, self.x+40, self.y+20, 1)
                    self.focusFire = 0
                
        #Update player collision i actually hate pygame so much 
        #why do i gotta add all of this just to make my collisions work atleast it's easy  
        self.rect.center = (self.x, self.y) 
        
    def show(self, surface):
        if godmode == False:
            surface.blit(THERESA_IMG, (self.x-50, self.y-50)) # Make image, this is the Ame
        else:
            surface.blit(THERESA_IMG_HALF, (self.x-50, self.y-50))
        if self.focus == True:
            pygame.draw.circle(surface, (0,0,255), (self.x, self.y), 8)

# ==== ENEMY BULLET SPRITE
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x,y, targetX, targetY, speed, dir, AIM, type, type2): # aim is to toggle if it aims toward player or not, type2 is between dagger or bullet
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.targetX = targetX # for aiming at something, um the same is for targetY and dir
        self.targetY = targetY
        self.speed = speed
        self.dir = dir
        self.type = type # 0 means red, 1 means blue
        self.type2 = type2
        
        self.freeze = False
        
        self.rect = pygame.Rect(self.x - 5, self.y - 5, 5 * 2, 5 * 2)
        
        if AIM == True:
            self.dir = math.atan2(targetY - y, targetX - x)
        elif AIM == False:
            self.dir = math.radians(dir) # because for SOME F$*$A$$ REASON PYTHON USES RADIANS FOR MATH WHO GENUINELY LIKES THIS LANGUAGE IVE SEEN BETTER FROM SCRATCH

    def update(self):
        self.x += math.cos(self.dir) * self.speed # praise chatgpt for making equations like these
        self.y += math.sin(self.dir) * self.speed
            
        if self.x < -50 or self.x > 1330 or self.y < -50 or self.y > 1010:
            self.kill() #remove sprite when its offscreen
            
        self.rect.center = (self.x, self.y)
            
    def show(self, surface):
        if self.type2 == 0:
            pygame.draw.circle(surface, (255,0,0), (self.x, self.y), 5)

        elif self.type2 == 1:
            angle = -math.degrees(self.dir) - 90 # -90 is for the offset
            
            rotated = pygame.transform.rotate(changeKunaiColor(self.type), angle)
            rect = rotated.get_rect(center=(self.x, self.y))

            # draw rotated kunai
            surface.blit(rotated, rect)

            # draw rect around rotated kunai (debug)
            if debug == True:
               pygame.draw.rect(surface, (255,0,0), rect, 1)  


# ==== BOSS SPRITE
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, bulletGroup, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = image
        self.speed = 8
        self.bulletGroup = bulletGroup
        
        self.rect = pygame.Rect(self.x - 30, self.y - 30, 30 * 2, 30 * 2)
        
        self.eTime = 0 # used to find the difference between current time and the cooldown
        self.eTime2 = 0 # used to find the difference between current time and the cooldown, second one incase i want the boss to do smth else alongside it uh
        self.eTime3 = 0 # same reason as eTime2
        
        self.eDir = 0 # direction to shoot a bullet
        self.cooldown = 100  # same as in flower test
        
        self.timeOffset = 0 # for the sin wave timing!!
        
        self.burstCount = 0 # for attack 2
        
        self.mTime = 0 # used for movement and changing the position of the boss
        self.mCooldown = 5000 #cooldown for when the boss moves
        self.targetX = x
        self.targetY = y
        
    def update(self):
        
        if phaseChanging == False:

            # attacks
            
            # ============= ATTACK 1
            if attack == 1:
                # this is the flower test pattern from the while true loop code
                currentTime = pygame.time.get_ticks()
                self.cooldown = 100
                
                self.timeOffset += 0.02  # controls the speed apparently..
                self.eDir = math.sin(self.timeOffset) * 90  # whatever its multiplied by is the max angle it can spin
                
                if currentTime - self.eTime > self.cooldown:
                    for i in range(18):      
                        if i % 2 == 0:
                            newEnemyBullet = EnemyBullet(
                                self.x, # x position of boss
                                self.y, # y position of boss
                                newPlayer.x, # x position of the target to shoot
                                newPlayer.y, # y position of the target to shoot
                                5, # speed of the bullet
                                (i * 20) + self.eDir, #rotation of the bullet
                                False, #toggle whether the bullet is aimed toward player or not; overrides target x and target y
                                0, #bullet apperance
                                0) # bullet type
                        else:
                            newEnemyBullet = EnemyBullet(
                                self.x, # x position of boss
                                self.y, # y position of boss
                                newPlayer.x, # x position of the target to shoot
                                newPlayer.y, # y position of the target to shoot
                                5, # speed of the bullet
                                (i * 20) + self.eDir, #rotation of the bullet
                                False, #toggle whether the bullet is aimed toward player or not; overrides target x and target y
                                2, # bullet appearance
                                0) # bullet type
                        enemyBullets.add(newEnemyBullet)
                    self.eTime = currentTime
                
                # ===============
                # boss moving
                self.x += (self.targetX - self.x) * 0.01
                self.y += (self.targetY - self.y) * 0.01
                bossMoveTime = pygame.time.get_ticks()
                self.mCooldown = 5000 #cooldown for when the boss moves
                
                if bossMoveTime - self.mTime > self.mCooldown:
                    
                    if self.x < WIN_WIDTH/2 - 1:
                        self.targetX = self.x+100
                    else:
                        self.targetX = self.x-100
                    self.targetY = self.y+0
                    self.mTime = bossMoveTime
                    
            # ================= ATTACK 2
            elif attack == 2:
                
                currentTime = pygame.time.get_ticks()
                self.cooldown = 200 # cooldown between bursts
                self.cooldown2 = 1250 # cooldown between the 3 bursts
                self.cooldown3 = 450 # cooldown between the flower code thing

                # flower stuff
                if currentTime - self.eTime3 > self.cooldown3:
                    for i in range(25):      
                        newEnemyBullet = EnemyBullet(
                            self.x, # x position of boss
                            self.y, # y position of boss
                            newPlayer.x, # x position of the target to shoot
                            newPlayer.y, # y position of the target to shoot
                            5, # speed of the bullet
                            (i * 15) + self.eDir, #rotation of the bullet
                            False, #toggle whether the bullet is aimed toward player or not; overrides target x and target y
                            0, # bullet apperance
                            0) # bullet type
                        
                        enemyBullets.add(newEnemyBullet)
                    self.eTime3 = currentTime
                    self.eDir += 5

                # THE BURST CODE for the 5 bullet spawns
                if currentTime - self.eTime2 > self.cooldown2 and self.burstCount == 0:
                    
                    # fire first burst instantly for some reason
                    for e in range(5):
                        for i in range(7):
                            newEnemyBullet = EnemyBullet(
                                self.x, # x position of boss
                                self.y, # y position of boss
                                newPlayer.x - 300 + 150*e, #x position of the target to shoot
                                newPlayer.y, # y position of the target to shoot
                                7+i, # speed of the bullet
                                0, #rotation of the bullet
                                True, #toggle whether the bullet is aimed toward player or not; overrides target x and target y
                                1, # bullet appearance
                                0) # bullet type
                            enemyBullets.add(newEnemyBullet)

                    self.burstCount = 1
                    self.eTime = currentTime # start the first eTime thing

                # then after first burst, fire the second and third
                if 1 <= self.burstCount < 3 and currentTime - self.eTime > self.cooldown:

                    for e in range(5):
                        for i in range(7):
                            newEnemyBullet = EnemyBullet(
                                self.x, # x position of boss
                                self.y, # y position of boss
                                newPlayer.x - 300 + 150*e, #x position of the target to shoot
                                newPlayer.y, # y position of the target to shoot
                                7+i, # speed of the bullet
                                0, #rotation of the bullet
                                True, #toggle whether the bullet is aimed toward player or not; overrides target x and target y
                                1, # bullet appearance
                                0) # bullet type
                            enemyBullets.add(newEnemyBullet)

                    self.burstCount += 1
                    self.eTime = currentTime

                    # only happens once burst count reaches 3, resets the timer for long cooldown and burstcount
                    if self.burstCount == 3:
                        self.eTime2 = currentTime
                        self.burstCount = 0
            elif attack == 3:    
                currentTime = pygame.time.get_ticks()
                self.cooldown = 200 # cooldown between bursts
                self.cooldown2 = 500 # cooldown between the 3 bursts
                self.cooldown3 = 450 # cooldown between the flower code thing
                
                
                # random bullets
                if currentTime - self.eTime > self.cooldown:    
                    for i in range(15):
                        newEnemyBullet = EnemyBullet(
                            self.x, # x position of boss 
                            self.y, # y position of boss
                            newPlayer.x, # x position of the target to shoot
                            newPlayer.y, # y position of the target to shoot
                            random.randint(4, 7), # speed of the bullet
                            random.randint(-180, 180), #rotation of the bullet
                            False, #toggle whether the bullet is aimed toward player or not; overrides target x and target y
                            random.randint(0, 4), # bullet appearance
                            0) # bullet type
                        enemyBullets.add(newEnemyBullet)
                    self.eTime = currentTime
                    
                #kunai
                if currentTime - self.eTime2 > self.cooldown2:    
                    for e in range(2):
                        for i in range(7):
                            newEnemyBullet = EnemyBullet(
                                self.x, # x position of boss
                                self.y, # y position of boss
                                newPlayer.x - 600 + 200*i, #x position of the target to shoot
                                newPlayer.y, # y position of the target to shoot
                                4+e, # speed of the bullet
                                0, #rotation of the bullet
                                True, #toggle whether the bullet is aimed toward player or not; overrides target x and target y
                                e, # bullet appearance
                                1) # bullet type
                            enemyBullets.add(newEnemyBullet)                    
                        self.eTime2 = currentTime
                    
            elif attack == 4:
                currentTime = pygame.time.get_ticks()
                self.cooldown = 750 # cooldown between bursts
                self.cooldown2 = 2000 # cooldown between the 3 bursts
                self.cooldown3 = 2000 # cooldown between the flower code thing
                
                # flower stuff
                if currentTime - self.eTime > self.cooldown:
                    for i in range(45):      
                        newEnemyBullet = EnemyBullet(
                            self.x, # x position of boss
                            self.y, # y position of boss
                            newPlayer.x, # x position of the target to shoot
                            newPlayer.y, # y position of the target to shoot
                            5, # speed of the bullet
                            (i * 8) + self.eDir, #rotation of the bullet
                            False, #toggle whether the bullet is aimed toward player or not; overrides target x and target y
                            1, # bullet apperance
                            1) # bullet type
                        enemyBullets.add(newEnemyBullet)
                    self.eTime = currentTime
                    self.eDir += 5
                    
                # aimed bullets
                if currentTime - self.eTime2 > self.cooldown2:
                    for i in range(7):      
                        newEnemyBullet = EnemyBullet(
                            self.x, # x position of boss
                            self.y, # y position of boss
                            newPlayer.x, # x position of the target to shoot
                            newPlayer.y, # y position of the target to shoot
                            7+i*0.8, # speed of the bullet
                            (i * 15) + self.eDir, #rotation of the bullet
                            True, #toggle whether the bullet is aimed toward player or not; overrides target x and target y
                            1, # bullet apperance
                            0) # bullet type
                        enemyBullets.add(newEnemyBullet)
                    self.eTime2 = currentTime
                
                # explosion
                if currentTime - self.eTime3 > self.cooldown3:
                    for e in range(3):
                        for i in range(24):      
                            newEnemyBullet = EnemyBullet(
                                self.x, # x position of boss
                                self.y, # y position of boss
                                newPlayer.x, # x position of the target to shoot
                                newPlayer.y, # y position of the target to shoot
                                4+e*2, # speed of the bullet
                                (i * 15)+ self.eDir, #rotation of the bullet
                                False, #toggle whether the bullet is aimed toward player or not; overrides target x and target y
                                2+e, # bullet apperance
                                0) # bullet type
                            enemyBullets.add(newEnemyBullet)
                    self.eTime3 = currentTime
                    
            # Oh my god i AM NOT CONTAINING MYSELF ANYMORE I FORGOT TO ADD THIS DUMB LINE OF CODE AND THATS WHY THE HOMING BULLETS DIDNT DISAPPEAR WHEN THEY HIT THE BOSS
            # PYGAME IS THE WORST GAME ENGINE IVE EVER USED I NEVER WANT TO USE THIS DUMB LANGUAGE AGAIN
            # im too scared to even swear in my comments
            # oh god i only have 3 more hours to work on this?? this is not good lol
        self.rect.center = (self.x, self.y)

    def show(self, surface):
        surface.blit(self.image, (self.x-50, self.y-50))

# ==== SPELLCARD GRAPHIC
class Spellcard(pygame.sprite.Sprite):
    def __init__(self, text, img):
        pygame.sprite.Sprite.__init__(self)
        self.x = WIN_WIDTH+950
        self.y = 980
        self.text = text
        self.targetX = WIN_WIDTH+200
        self.targetY = 980
        self.eTime = pygame.time.get_ticks()
        self.img = img
        
    def update(self):
        self.x += (self.targetX - self.x) * 0.05
        self.y += (self.targetY - self.y) * 0.015

        if pygame.time.get_ticks() - self.eTime > 1500:
            self.targetY = -1000

        if self.y < -500:
            self.kill()
    
    def show(self, surface):
        
        if self.img == 1:
            SPELLCARD_IMG = pygame.image.load("Ame.png").convert_alpha()
        elif self.img == 2:
            SPELLCARD_IMG = pygame.image.load("Theresa.png").convert_alpha()
            
        surface.blit(pygame.transform.scale(SPELLCARD_IMG, (900, 900)), (self.x-900, self.y-900))
        
        pygame.draw.rect(surface, (0,0,205), pygame.Rect(self.x-870, self.y-230, 500, 60))
        
        GAME_FONT.size = 30
        text_surface, rect = GAME_FONT.render(self.text, (255, 255, 255)) # rect is there for some reason idk probably to add something for the text to rest on
        SCREEN.blit(text_surface, (self.x-850, self.y-220))

pygame.init() # start the pygame engine

WIN_WIDTH = 1280
WIN_HEIGHT = 960
SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)) #set_mode takes a tuple, its kind of weird

#IMAGE LOADING

AME_IMG = pygame.image.load("Ame.png").convert_alpha()
AME_IMG = pygame.transform.scale(AME_IMG, (100, 100))

SPELLCARD_IMG = pygame.image.load("Ame.png").convert_alpha()

THERESA_IMG = pygame.image.load("Theresa.png").convert_alpha()
THERESA_IMG = pygame.transform.scale(THERESA_IMG, (100, 100))

THERESA_IMG_HALF = THERESA_IMG.copy()
THERESA_IMG_HALF.set_alpha(50)   # 0 = invisible, 255 = fully opaque

PLAYERHITBOX_IMG = pygame.image.load("Hitbox.png").convert_alpha()
PLAYERHITBOX_IMG = pygame.transform.scale(PLAYERHITBOX_IMG, (125, 125))

BULLET_IMG = pygame.image.load("TouhouBullet.png").convert_alpha()
BULLET_IMG = pygame.transform.scale(BULLET_IMG, (35, 35))

BULLET2_IMG = pygame.image.load("TouhouBullet2.png").convert_alpha()
BULLET2_IMG = pygame.transform.scale(BULLET2_IMG, (35, 35))

BULLET3_IMG = pygame.image.load("TouhouBullet3.png").convert_alpha()
BULLET3_IMG = pygame.transform.scale(BULLET3_IMG, (35, 35))

BULLET4_IMG = pygame.image.load("TouhouBullet4.png").convert_alpha()
BULLET4_IMG = pygame.transform.scale(BULLET4_IMG, (35, 35))

BULLET5_IMG = pygame.image.load("TouhouBullet5.png").convert_alpha()
BULLET5_IMG = pygame.transform.scale(BULLET5_IMG, (35, 35))

KUNAI_IMG = pygame.image.load("Kunai.png").convert_alpha()
KUNAI_IMG = pygame.transform.scale(KUNAI_IMG, (35, 35))

KUNAI2_IMG = pygame.image.load("Kunai2.png").convert_alpha()
KUNAI2_IMG = pygame.transform.scale(KUNAI2_IMG, (35, 35))

BULLETPLAYER_IMG = pygame.image.load("TouhouBulletPlayer.png").convert_alpha()
BULLETPLAYER_IMG = pygame.transform.scale(BULLETPLAYER_IMG, (16, 32))

BULLETPLAYERHOME_IMG = pygame.image.load("TouhouBulletPlayerHoming.png").convert_alpha()
BULLETPLAYERHOME_IMG = pygame.transform.scale(BULLETPLAYERHOME_IMG, (28, 30))

pygame.display.set_caption("PolyTouhou") # this sets the name of the window
CLOCK = pygame.time.Clock()

# TEXT FONT STUFF
GAME_FONT = pygame.freetype.Font("COMIC.TTF", 24)

# starting position for the player I guess
x = WIN_WIDTH/2
y = 800

attack = 0 #BOSS ATTACK
bossHealth = 50000

# for the end screen!
deaths = 0

focus = False
playerSpeed = 8
godmode = False
debug = False

# Groups for the sprites
playerBullets = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
enemyBullets = pygame.sprite.Group()
bossGroup = pygame.sprite.Group()
spellcardGroup = pygame.sprite.Group()

# Lines of text for the title screen
titleLines = [
    'Welcome to Touhou Demo!!',
    'Controls:',
    'Arrow Keys to move',
    'Shift Key to focus; slows movement, attacks stronger',
    '',
    'DEBUG FUNCTIONS:',
    'G Key to enable godmode (or maybe just get good..)',
    'B Key during gameplay to cut to win',
    '',
    'Press P to start!',
]

# Do title screen!!
while True:
    
    SCREEN.fill((255,255,255)) #redraw the background white
    
    #1 Handle events (user input of keys or mouse etc)
    for event in pygame.event.get():
        if event.type == QUIT:
            print("User tried to quit")
            pygame.quit() # shut down pygame
    
    keys = pygame.key.get_pressed() # pygame.key.get_pressed() returns a list of keys
    if keys[K_p]:
        break
    
    #TEXT STUFF
    GAME_FONT.size = 40
    
    y_offset = 0
    for line in titleLines:
        text_surface, rect = GAME_FONT.render(line, (0, 0, 0))
        SCREEN.blit(text_surface, (150, WIN_HEIGHT/2 - 180 + y_offset))
        y_offset += 40 # spacing between lines
    
    pygame.display.flip() #reveals the next frame and delay before the next loop iteration
    CLOCK.tick(60) #slow the frame rate to 60 fps

# Had to move these over here because of the title screen, conflicts with some of the timers
spellcardDelayTime = pygame.time.get_ticks() # for spellcard ui, will be changed to the amount of time when the boss does a spellcard
phaseChanging = False

playerDeathTime = pygame.time.get_ticks() # same system as spellcard delay time
playerDying = False

playerGodmodeTime = pygame.time.get_ticks() # same system as spellcard delay time as well
playerGodmodeTimeStart = False

# Spawn Player
newPlayer = Player(x, y, playerBullets, AME_IMG)
playerGroup.add(newPlayer)

# Spawn Boss
newBoss = Boss(WIN_WIDTH/2, 100, enemyBullets, AME_IMG)
bossGroup.add(newBoss)

phaseChanging = True
attack += 1
spellcardGraphic(attackName(attack), 1)
bossHealth = 50000
spellcardDelayTime = pygame.time.get_ticks()
pygame.sprite.Group.empty(enemyBullets)

# This is the main game loop!!
while True:
    
    #1 Handle events (user input of keys or mouse etc)
    # I dont use this alot just because its just a single keypress but it is good for debug functions
    for event in pygame.event.get():
        if event.type == QUIT:
            print("User tried to quit")
            pygame.quit() # shut down pygame
        elif event.type == KEYDOWN:
            if event.key == K_g:
                if godmode == False:
                    godmode = True
                    spellcardGraphic('journalist mode activated..?', 2)
                else:
                    godmode = False
                    spellcardGraphic('journalist mode deactivated!!', 2)
         
    # I would have done this in the pygame.event.get(), but its in a for loop so I gotta do it this way..
    # Besides, they are near eachother so it shouldn't hurt me anyway.. right?
               
    keys = pygame.key.get_pressed() # pygame.key.get_pressed() returns a list of keys
    if keys[K_b]:
        break
    
    # Bullet Debug: To test bullet aiming
    # if keys[K_SPACE]:
    #     newEnemyBullet = EnemyBullet(
    #         boss.x, # x position of boss
    #         boss.y, # y position of boss
    #         newPlayer.x, # x position of the target to shoot
    #         newPlayer.y, # y position of the target to shoot
    #         random.randint(4, 7), # speed of the bullet
    #         random.randint(-180, 180), #rotation of the bullet
    #         False, #toggle whether the bullet is aimed toward player or not; overrides target x and target y
    #         random.randint(0, 4)) # bullet appearance
    #     enemyBullets.add(newEnemyBullet)
        
    #2 Update the state of the game (move characters increase score etc.)
    # where the game logic goes!!
    
    # Boss Health stuff

    bossHealthPercentage = (bossHealth/50000) * 100

    if bossHealth <= 0 and phaseChanging == False:
        phaseChanging = True
        attack += 1
        spellcardGraphic(attackName(attack), 1)
        bossHealth = 50000
        spellcardDelayTime = pygame.time.get_ticks()
        pygame.sprite.Group.empty(enemyBullets)
        if attack > 4:
            break

    if phaseChanging == True:
        if pygame.time.get_ticks() - spellcardDelayTime > 1500:
            print('phase changed')
            bossHealth = 50000
            phaseChanging = False

    #3 Draw all components on the screen
    #bg, enemies, player, whatever else
        
    SCREEN.fill((0,0,0)) #redraw the background white
        
    # Draw all the sprites
    
    playerGroup.update()
    for p in playerGroup:
        p.show(SCREEN)
        
    enemyBullets.update()
    for bullet in enemyBullets:
        bullet.show(SCREEN)
        
    bossGroup.update()
    for boss in bossGroup:
        boss.show(SCREEN)
        
    playerBullets.update()
    for bullet in playerBullets:
        bullet.show(SCREEN)

    # deletes the player bullet when it hits the boss
    playerBulletCollision = pygame.sprite.groupcollide(playerBullets, bossGroup, True, False, pygame.sprite.collide_circle)

    # when player bullet collision happens, start the godmode timer
    playerCollision = pygame.sprite.groupcollide(playerGroup, enemyBullets, False, False, pygame.sprite.collide_circle) 
    if playerBulletCollision:
        bossHealth -= 100
    
    # Player death code
    if playerCollision and godmode == False:
        # break
        deaths += 1
        playerDying = True
        playerDeathTime = pygame.time.get_ticks()
        playerGodmodeTimeStart = True
        playerGodmodeTime = pygame.time.get_ticks()
        pygame.sprite.Group.empty(playerGroup)
        godmode = True
        print('ded', deaths)
    
    # Only starts going off if the playerdying variable is true, then after it does its thing it sets the variable to false so it doesnt happen again
    if playerDying == True:
        if pygame.time.get_ticks() - playerDeathTime > 1000:
            print('player respawn')
            newPlayer = Player(x, y, playerBullets, AME_IMG)
            playerGroup.add(newPlayer)
            playerDying = False

    # Once this activates it just turns off your godmode
    if playerGodmodeTimeStart == True:
        if pygame.time.get_ticks() - playerGodmodeTime > 2500:
            print('godmode off')
            godmode = False
            playerGodmodeTimeStart = False


    #For loops to iterate through the groups, um it just displays an image over them incase i wanna do some fun stuff, also i hate updating images in sprites
    for player in playerGroup:
        if player.focus == True:
            SCREEN.blit(PLAYERHITBOX_IMG, (player.x-125/2, player.y-125/2)) # Make image, this is hitbox 
    
    for bullet in enemyBullets:
        if bullet.type2 == 0:
            if bullet.type == 0:
                SCREEN.blit(BULLET_IMG, (bullet.x-35/2, bullet.y-35/2)) # Make image, red bullet
            elif bullet.type == 1:
                SCREEN.blit(BULLET2_IMG, (bullet.x-35/2, bullet.y-35/2)) # Make image, blue bullet
            elif bullet.type == 2:
                SCREEN.blit(BULLET3_IMG, (bullet.x-35/2, bullet.y-35/2)) # Make image, bullet variation 1
            elif bullet.type == 3:
                SCREEN.blit(BULLET4_IMG, (bullet.x-35/2, bullet.y-35/2)) # Make image, bullet variation 2
            elif bullet.type == 4:
                SCREEN.blit(BULLET5_IMG, (bullet.x-35/2, bullet.y-35/2)) # Make image, bullet variation 3
    
    for bullet in playerBullets:
        if bullet.type == 0:
            SCREEN.blit(BULLETPLAYER_IMG, (bullet.x-16/2, bullet.y-32/2)) # Make image, this is the regular bullet
        elif bullet.type == 1:
            SCREEN.blit(BULLETPLAYERHOME_IMG, (bullet.x-28/2, bullet.y-30/2)) # Make image, this is the homing bullet (talisman i think?)
    
    for boss in bossGroup:
        SCREEN.blit(AME_IMG, (boss.x-50, boss.y-50)) # Make image, this is the boss

    # Boss healthbar thing
    pygame.draw.rect(SCREEN, (255,255,255), pygame.Rect(0, WIN_HEIGHT-10, WIN_WIDTH*bossHealthPercentage/100, WIN_HEIGHT-10))

    # Spellcard Ui sprite, here because it goes ontop of everything
    spellcardGroup.update()
    for ui in spellcardGroup:
        ui.show(SCREEN)

    # Font stuff
    GAME_FONT.size = 24

    # Text to show boss health
    text_surface, rect = GAME_FONT.render(str(round(bossHealthPercentage, 1)), (255, 255, 255)) # rect is there for some reason idk probably to add something for the text to rest on
    SCREEN.blit(text_surface, (10, WIN_HEIGHT-40))
    
    pygame.display.flip() #reveals the next frame and delay before the next loop iteration
    CLOCK.tick(60) #slow the frame rate to 60 fps
        
while True:
    
    SCREEN.fill((255,255,255)) #redraw the background white
    
    #1 Handle events (user input of keys or mouse etc)
    for event in pygame.event.get():
        if event.type == QUIT:
            print("User tried to quit")
            pygame.quit() # shut down pygame
    
    text_surface, rect = GAME_FONT.render(str(winText(deaths))) # rect is there for some reason idk probably to add something for the text to rest on
    SCREEN.blit(text_surface, (WIN_WIDTH/2 -100, WIN_HEIGHT/2))
    
    pygame.display.flip() #reveals the next frame and delay before the next loop iteration
    CLOCK.tick(60) #slow the frame rate to 60 fps