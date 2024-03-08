import pygame

from Game.collisionHandler import CollisionHandler
from .entity import Entity
import math
from Entities.Enemies.EnemyStates.patrol import Patrol
from Entities.Enemies.EnemyStates.chase import Chase
from Entities.Enemies.EnemyStates.attack import Attack
from Entities.Enemies.EnemyStates.die import Die

from Game.spritesheet import Spritesheet
from Constants.constants import *

from Entities.bullet import Bullet
class FlyingEnemy(pygame.sprite.Sprite, Entity):
    def __init__(self,x,y, dificulty, onlyChase) -> None:
        pygame.sprite.Sprite.__init__(self)
        # Otros objetos
        self.collisionHandler = CollisionHandler()
        
        # Atributos de posicion e imagen
        #self.sprites = Spritesheet('Assets/Images/Entities/32bitsspritesheet.png',(120,120)).get_animation(0,0,223,223,30)
        self.image = pygame.image.load('Assets/Images/Entities/Player/lazer_24.png')
        self.index = 0
        self.time = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 100

        # Atributos de movimiento
        self.moved = 0
        self.patrollingSpeed = dificulty.getEnemyPatrollingSpeed()
        self.chasingSpeed = dificulty.getEnemyChasingSpeed()
        self.velY = 0
        
        # Atributos de control de vision
        self.viewDirection = 1
        self.maxViewDistance = dificulty.getFlyingEnemyMaxViewDistance() # Distancia directa hacia el jugador (diagonal)
        self.minAtackDistance = dificulty.getEnemyMinAttackDistance() # Distancia directa hacia el jugador (diagonal)
        self.distanciaAlJugador = 0
        self.angle = 0
        self.lineStart = (self.rect.centerx, self.rect.centery)

        # Atributos de control de disparo
        self.disparoImg = pygame.image.load('Assets/Images/Entities/Player/lazer_24.png')
        self.shootCooldown = dificulty.getEnemyShootCooldown()
        self.disparosList = []
        self.velocidadBala = dificulty.getEnemyBulletSpeed()
        self.bulletDamage = dificulty.getFlyingEnemyDamage()

        # Atributos de control de estados
        self.onlyChase = onlyChase
        self.chaseTime = dificulty.getEnemyChaseTime()
        self.states = {"patrolling": Patrol(self),
                       "chasing": Chase(self),
                       "attacking": Attack(self),
                       "die": Die(self)}

        self.states = {"patrolling": self.patrol,
                       "chasing": self.chase,
                       "attacking": self.attack,
                       "die": self.die}
        
        self.state_name = "patrolling"
        self.current_state = self.states["patrolling"]
        if onlyChase:
            self.state_name = "chasing"
            self.current_state = self.states["chasing"]
            
    def checkBulletCollision2(self, world, player, disparo):
        if disparo.bulletPosition().colliderect(player.position()):
            if player.hit(self.bulletDamage):
                return True
            else:
                #player.deflect(self.angle + 180, self.disparoImg, self.velocidadBala)
                return True
            
        tileHitBoxList = world.getTilesList()
        destructibleHitBoxList = world.getDestructiblesList()

        tileIndex = disparo.bulletPosition().collidelist(tileHitBoxList)

        destructibleIndex = disparo.bulletPosition().collidelist(destructibleHitBoxList)
        
        if tileIndex >= 0 or destructibleIndex >= 0:
            return True

                
    def update(self, dt, world, player, cameraOffset,enemies_group):
        self.time += 1
        if self.time > 6:
            self.time = 0
            self.index += 1
            #if self.index >= len(self.sprites):
                #self.index=0
            self.image = self.current_state.next_sprite()

        for disparo in self.disparosList:
            disparo.update(cameraOffset)
            if self.checkBulletCollision2(world, player, disparo) or disparo.checkDespawnTime():
                self.disparosList.remove(disparo)
                del disparo

        self.states[self.state_name].update(dt, world, player, cameraOffset,enemies_group)
        self.player_in_sight(world, player)
        if self.current_state.done:
            self.change_state()

    def patrol(self, world, player, cameraOffset,enemies_group):
        # Comportamiento cuando está patrullando
        dy = 0

        self.moved += 1
        if self.moved >= 400:
            self.viewDirection = -self.viewDirection
            self.patrollingSpeed = -self.patrollingSpeed
            self.moved = 0
        
        # Se calculan las colisiones en ambos ejes
        tileHitBoxList = world.getTilesList()
        platformHitBoxList = world.getPlatformsList()
        destructibleHitBoxList = world.getDestructiblesList()

        tileCollisions = self.collisionHandler.checkCollisions(self, tileHitBoxList, self.patrollingSpeed, dy)
        platformCollisions = self.collisionHandler.checkCollisions(self, platformHitBoxList, self.patrollingSpeed, dy)
        destructibleCollisions = self.collisionHandler.checkCollisions(self, destructibleHitBoxList, self.patrollingSpeed, dy)

        if tileCollisions[0] >= 0 or destructibleCollisions[0] >= 0:
            self.patrollingSpeed = -self.patrollingSpeed
            self.viewDirection = -self.viewDirection

        if tileCollisions[1] >= 0:
            if self.velY < 0: #Saltando
                dy = tileHitBoxList[tileCollisions[1]].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = tileHitBoxList[tileCollisions[1]].top - self.rect.bottom
                self.velY = 0
        if destructibleCollisions[1] >= 0:
            if self.velY < 0: #Saltando
                dy = destructibleHitBoxList[destructibleCollisions[1]].bottom - self.rect.top
                self.velY = 0
            elif self.velY >= 0: #Cayendo
                dy = destructibleHitBoxList[destructibleCollisions[1]].top - self.rect.bottom
                self.velY = 0

        if platformHitBoxList[platformCollisions[0]].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
            if self.velY >= 0 and (self.rect.bottom - platformHitBoxList[platformCollisions[0]].top) < 10: #Cayendo
                dy = platformHitBoxList[platformCollisions[0]].top - self.rect.bottom
                self.velY = 0
        
        self.rect.x += self.patrollingSpeed - cameraOffset[0]
        self.rect.y += dy - cameraOffset[1]

    
    def chase(self, world, player,cameraOffset,enemies_group):
        self.chaseTime -= 1

        if self.chaseTime <= 0 and not self.onlyChase:
            self.current_state.next_state = "patrolling"
            self.current_state.done = True
            
        self.moved = 0

        if player.position().x > self.rect.x:
            self.viewDirection = 1
            self.moved -= self.chasingSpeed

        if player.position().x < self.rect.x:
            self.viewDirection = -1
            self.moved += self.chasingSpeed

        tileHitBoxList = world.getTilesList()
        destructibleHitBoxList = world.getDestructiblesList()

        auxRect = pygame.Rect(self.rect.x - self.moved, self.rect.y, self.rect.width, self.rect.height)
        
        tileIndex = auxRect.collidelist(tileHitBoxList)

        destructibleIndex = auxRect.collidelist(destructibleHitBoxList)
        
        if tileIndex >= 0 or destructibleIndex >= 0:
            self.moved = 0

        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]
        
        self.rect.x -= self.moved

        if self.distanciaAlJugador < self.minAtackDistance:
            self.current_state.next_state = "attacking"
            self.current_state.done = True
    
    def attack(self, world, player,cameraOffset,enemies_group):
        # Disparar cada x segundos,
        self.shootCooldown -= 1
        if self.shootCooldown <= 0:
            self.shootCooldown = 30
            disparo = Bullet(self.disparoImg, self.angle, self.velocidadBala, self.rect.x, self.rect.y)
            self.disparosList.append(disparo)

        self.rect.x -= cameraOffset[0]
        self.rect.y -= cameraOffset[1]

        if self.distanciaAlJugador > self.minAtackDistance:
            self.current_state.done = True
            self.current_state.next_state = "chasing"
    
    def drawBullets(self, screen):
        for disparo in self.disparosList:
            disparo.draw(screen)
            
    # Método para cambiar de estado
    def change_state(self):
        self.state_name = self.current_state.next_state
        self.current_state.done = False

        self.current_state = self.states[self.state_name]

    # Lógica para determinar si el jugador está dentro del rango de visión
    def player_in_sight(self, world, player):
        dx = player.position().centerx - self.rect.centerx
        dy = player.position().centery - self.rect.centery

        self.distanciaAlJugador = math.sqrt((dx**2) + (dy**2))
        self.angle = -math.degrees(math.atan2(dy, dx))

        self.lineStart = (self.rect.x, self.rect.y)
        
        # Si no hay ningun obstaculo, y player.position() es < self.maxViewDistance, se puede ver. 
        if self.distanciaAlJugador < self.maxViewDistance:
            # Si la en la linea de vision se interpone un obstaculo, no se puede ver al jugador
            tileHitBoxList = world.getTilesList()
            destructibleHitBoxList = world.getDestructiblesList()

            for tile in tileHitBoxList:
                if tile.clipline((self.lineStart, (player.position().centerx, player.position().centery))):
                    return False
                
            for tile in destructibleHitBoxList:
                if tile.clipline((self.lineStart, (player.position().centerx, player.position().centery))):
                    return False
        else:
            return False
        
        # Si no hay un obstaculo de por medio y esta suficientemente cerca, se está viendo al jugador
        # Cambiar al estado de chasing
        if self.state_name == "patrolling":
            self.chaseTime = 120
            self.current_state.next_state = "chasing"
            self.current_state.done = True

    def die(self,world, player,cameraOffset,enemies_group):
        enemies_group.remove(self)
        
    def kill(self):
        self.current_state = "die"  