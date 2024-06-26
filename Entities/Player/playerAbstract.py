import pygame
from Constants.constants import *
from MovementAndCollisions.movement import *

class PlayerAbstract():
    def __init__(self,x,y, dificulty):
        # Posicion
        self.dificulty = dificulty
        self.rect = pygame.Rect(0,0,50,94)
        self.rect.x = x
        self.rect.y = y
        self.width = self.rect.width
        self.height = self.rect.height
        
        # Movimiento
        self.velY = 0            
        self.inAir = True
        self.moving_left = False
        self.moving_right = False
        self.left_mov = 0
        self.right_mov = 0
        self.jumping = False
        self.hold_jump = False
        self.pressed_jump = 0
        self.grabbed = False
        self.dragSpeed = 0
        
        #Vida
        self.maxHealthPoints = 3
        self.healthPoints = self.maxHealthPoints
        self.hitCooldown = dificulty.getPlayerHittedCooldown()
        
        #Armas
        self.arma = None
        self.uiElementsList = []
        self.interactuableText = ""
        self.bulletDamage = dificulty.getPlayerBulletDamage()
        self.bulletSpeed = dificulty.getPlayerBulletSpeed()
        self.shootCooldownConst = dificulty.getPlayerShootCooldown()
        self.shootGrenadeCooldownConst = dificulty.getPlayerShootGrenadeCooldown()
        self.grenadeDamage = dificulty.getPlayerGrenadeDamage()
        
        # Sprites
        self.direction = 0
        self.state = None
        self.states = None

        # SoundEffects
        self.jumpEffect = pygame.mixer.Sound('Assets/Audio/SoundEffects/JumpEffect.mp3')
        self.volume = 0.7
        self.jumpEffect.set_volume(self.volume)

        #Dash
        self.dashing = False
        self.dashCooldown = 0
        self.holdDash = False
        self.dashDuration = 0
        self.lookingUp = False
        self.lookingDown = False

    def update(self, world, dt, enemies_group, interactuableGroup, triggerGroup, cameraOffset) -> tuple:
        pass
    
    def draw(self, screen):
        pass
        
    # Metodo para cambiar los estados cuando se coge un arma diferente
    def changeStates(self):
        self.player.states = self.states

    def change_state(self):
        pass

    def idle(self):
        pass

    def stopShooting(self):
        pass

    def move_left(self):
        pass
    
    def move_right(self):
        pass
    
    def jump(self):
        pass
    
    def getHp(self):
        pass
    
    def shoot(self, direction, gv):
        pass
    
    def addObserver(self, observer):
        self.uiElementsList.append(observer)

    def delObserver(self, observer):
        self.uiElementsList.remove(observer)
        
    def notify(self):
        for observer in self.uiElementsList:
            observer.update(self)
    
    def position():
        pass
    
    def getShieldHp(self):
        pass
    
    def heal(self):
        pass
    
    def getDificulty(self):
        return self.dificulty
    
    def setVolume(self, volume):
        self.jumpEffect.set_volume(volume)
        self.volume = volume

    def dash(self):
        pass

    def unDash(self):
        pass
        
    def lookUp(self):
        pass

    def lookDown(self):
        pass

    def setHealth(self, n):
        self.healthPoints = n

    def hit(self, damage):
        pass
