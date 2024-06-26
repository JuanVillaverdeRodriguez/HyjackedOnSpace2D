import pygame
from Game.spritesheet import Spritesheet
from Constants.constants import *

class Health(pygame.sprite.Sprite):
    def __init__(self, x, y, dificulty) -> None:
        pygame.sprite.Sprite.__init__(self)
        
        self.spritesheet = Spritesheet(INTERACTIVES_PATH + 'healing_pickup.png', (64,64))
        
        # Cargar sprites
        self.spriteList = self.spritesheet.cargar_sprites(64, 64)
        self.image = self.spriteList[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.healingPower = dificulty.getHealthPickupHealingPower()

        self.iconNumber = 0
    
    def update(self, player, cameraOffset, healingGroup):
        if self.rect.colliderect(player.position()):
            player.heal(self.healingPower)
            healingGroup.remove(self)
        
        self.iconNumber += 1
        if self.iconNumber == len(self.spriteList):
            self.iconNumber = 0

        self.image = self.spriteList[self.iconNumber]

        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

    