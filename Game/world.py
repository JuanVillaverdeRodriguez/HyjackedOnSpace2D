import pygame
import json
from Entities.Enemies.enemy import *
from Entities.Player.playerWithPistol import *
from Entities.shieldPickup import ShieldPickup
from Interactives.computer import Computer
from Constants.constants import *
from Entities.health import Health
from Entities.grenadeLauncher import GrenadeLauncher
from Entities.pistol import Pistol

class World():
        def __init__(self, enemies, enemyFactory, interactives, cameraOffset, healthPickUps, destructibles_group, gunPickups):
            self.tile_list = []
            self.gun_list = []
            self.terrainHitBoxList = []
            self.interactuableList = []
            self.enemies = enemies
            self.healthPickUps = healthPickUps
            self.destructibles_group = destructibles_group
            self.gunPickups = gunPickups
            self.interactiveGroup = interactives

            self.enemyFactory = enemyFactory
            self.pistola = pygame.transform.scale(pygame.image.load(PLAYER_PATH + '/pistol.png'), (45,45))
            pistola2 = pygame.image.load(PLAYER_PATH + '/pistol2.png')
            pistola3 = pygame.image.load(PLAYER_PATH + '/pistol3.png')
            ordenador = pygame.image.load(INTERACTIVES_PATH + '/ibm5150.png')

            self.shieldImage = pygame.transform.scale(pygame.image.load(PLAYER_PATH + '/plasma_shield.png'), (45,45))
            
        
            '''row_count = 0
            for row in globalVars.world_data:
                col_count = 0
                previousTileId = -1
                
                for tile in row: 
                    
                    # Podria hacerse cuatro listas (O las que se quisieran)
                    # 1º Contedria todos los tiles de la mitad superior izquierda del nivel
                    # 2º Contendria todos los tiles de la mitad superior derecha del nivel
                    # 3º Contendria todos los tiles de la mitad inferior izquierda del nivel
                    # 4º Contendria todos los tiles de la mitad inferior derecha del nivel
                    # Los sprites no se meterian en estas listas, tendrian una sola lista (NO va  a haber 1000 sprites, pero si tiles)
                    # Se comprobaria en que región (en cual de las cuatro listas) esta el personaje y se comrpobarian las colisiones con los tiles presentes en esa region
                    # Es decir se recorrerian las 4 regiones buscando si el personaje está en cada una de ellas (com collidelist se podria conrpobar si el jugador esta dentro de esta region)
                    # O el personaje podria informar (patron observer) en que region esta
                    # Pero esperar a que oscar lo haga con JSON primero

                    # Tambien se podria simultaneamente los tiles que estan juntos juntarlos mediante union() para hacer solo un rectangulo
                    if tile == 0:
                        previousTileId = 0
                    if tile >= 0 and tile < 20:
                        img_rect = img.get_rect()
                        img_rect.x = (col_count * TILE_SIZE)
                        img_rect.y = row_count * TILE_SIZE
                        
                        hit_box = img.get_rect()
                        hit_box.x = (col_count * TILE_SIZE)
                        hit_box.y = row_count * TILE_SIZE

                        tile = (img, img_rect)

                        if previousTileId == 1:
                            self.terrainHitBoxList.pop()
                            joinedHitBox = previousTile.union(hit_box)
                            previousTile = joinedHitBox
                            self.terrainHitBoxList.append(joinedHitBox)
                        else:
                            self.terrainHitBoxList.append(hit_box)
                            previousTile = hit_box

                        self.tile_list.append(tile)
                        
                        previousTileId = 1

                    if tile == 50:
                        en = self.enemyFactory.createEnemy(col_count * TILE_SIZE, row_count * TILE_SIZE - 52, self.globalVars)
                        enemies.add(en)
                        previousTileId = 2

                    if tile == 3:
                        img = pygame.transform.scale(pistola, (TILE_SIZE, TILE_SIZE))
                        img_rect = img.get_rect()
                        img_rect.x = (col_count * TILE_SIZE)
                        img_rect.y = row_count * TILE_SIZE
                        tile = (img, img_rect)
                        self.gun_list.append(tile)
                        previousTileId = 3
                    if tile == 4:
                        ordenador = Computer(col_count * TILE_SIZE, row_count * TILE_SIZE, self.globalVars)
                        interactuable.add(ordenador)
                        previousTileId = 4
                    col_count += 1
                row_count += 1'''
            self.cargarNivel("Lvl1")

            '''print("Numero de tiles en el terreno antes: ")
            print(len(self.tile_list))
            print("Numero de tiles en el terreno ahora: ")
            print(len(self.terrainHitBoxList))


            print("Numero de tiles en el terreno antes: ")
            print(len(self.tile_list))
            print("Numero de tiles en el terreno ahora: ")
            print(len(self.terrainHitBoxList))'''

        def draw(self, screen, cameraOffset):
            # Se dibuja las tiles teniendo en cuenta el scroll

            (cameraOffsetX,cameraOffsetY) = cameraOffset

            for tile in self.tile_list:
                tile[1].x -= cameraOffsetX
                tile[1].y -= cameraOffsetY

                if tile[1].x > cameraOffsetX - 320 and tile[1].x < cameraOffsetX + SCREEN_WIDTH + 320 and tile[1].y > cameraOffsetY - 320 and tile[1].y < cameraOffsetY + SCREEN_HEIGTH + 320:
                    screen.blit(tile[0], tile[1])

            for gun in self.gun_list:
                gun[0][1].x -= cameraOffsetX
                gun[0][1].y -= cameraOffsetY
                screen.blit(gun[0][0], gun[0][1])

            for hitbox in self.terrainHitBoxList:
                hitbox.x -= cameraOffsetX
                hitbox.y -= cameraOffsetY


        def seleccionarTextura(self, fila, columna, maxColumna, altura, anchura, imagen):
            if columna >= maxColumna:
                return self.seleccionarTextura(fila+1, columna-10, maxColumna, altura, anchura, imagen)
            else:
                return imagen.subsurface((columna*anchura, fila*altura, anchura, altura))
            
        def cargarNivel(self, nivel):

            # Cargar el json con los datos del nivel

            with open(LVLS_PATH + nivel + '/datosNivel.json', 'r') as file:
                nivelData = file.read()
            nivelData = json.loads(nivelData)
            mapaNivel1 = nivelData['layers'][0]
            mapaFondo = nivelData['layers'][2]['data']
            nivel1Grid = mapaNivel1['data']
            anchuraMapa = mapaNivel1['width']
            compresion = nivelData['compressionlevel']

            

            # Cargar el json con los datos de las texturas

            pathTextura = nivelData['tilesets'][0]['source']
            with open(LVLS_PATH + nivel + "/" + pathTextura, 'r') as file:
                texturasNivel = file.read()
            texturasNivel = json.loads(texturasNivel)
            columnas = texturasNivel['columns']
            tileHeight = texturasNivel['tileheight']
            tileWidth = texturasNivel['tilewidth']

            # Cargar la imagen con las texturas de los tiles
            imagen = pygame.image.load(LVLS_PATH + nivel + '/texturas.png') 


            mapaX = 0
            mapaY = 0

            '''# Se recorre el nivel tile por tile
            for tile in mapaFondo:
                # Si un tile
                if tile > 0:
                    # Se recupera la textura que representa el tile y se añade una hitbox
                    texture = self.seleccionarTextura(0, tile+compresion, columnas, tileHeight, tileWidth, imagen)
                    textureRect = texture.get_rect()
                    textureRect.x = mapaX * tileWidth
                    textureRect.y = mapaY * tileHeight
                    tileTuple = (texture, textureRect)
                    self.tile_list.append(tileTuple) 
                    
                # Se actualiza la posicion del mapa
                mapaX += 1
                if mapaX >= anchuraMapa:
                    mapaX = 0
                    mapaY += 1'''


            # Iniciar la posicion del mapa
            mapaX = 0
            mapaY = 0
            previousTileId = 0

            

            # Se recorre el nivel tile por tile
            for tile in nivel1Grid:
                # Si un tile
                if tile > 0:
                    # Se recupera la textura que representa el tile y se añade una hitbox
                    texture = self.seleccionarTextura(0, tile+compresion, columnas, tileHeight, tileWidth, imagen)
                    textureRect = texture.get_rect()
                    textureRect.x = mapaX * tileWidth
                    textureRect.y = mapaY * tileHeight
                    tileTuple = (texture, textureRect)
                    self.tile_list.append(tileTuple) 

                    if previousTileId == 1:
                        self.terrainHitBoxList.pop()
                        joinedHitBox = previousTile.union(textureRect)
                        previousTile = joinedHitBox
                        self.terrainHitBoxList.append(joinedHitBox)
                    else:
                        self.terrainHitBoxList.append(textureRect)
                        previousTile = textureRect

                    previousTileId = 1
                
                else: 
                    previousTileId = 0

                # TODO: Hacer pistola y shield un objeto propio, 
                # facilitara el saber si se recogio una cosa u otra 
                # y se le quitaria trabajo a la clase update() del player (actualmente comprueba colision con todos los pickups)
                if mapaX == 14 and mapaY == 31:
                    pistol = Pistol(mapaX * tileWidth, mapaY * tileHeight)
                    self.gunPickups.add(pistol)
                
                if mapaX == 20 and mapaY == 31:
                    shieldPickup = ShieldPickup(mapaX * tileWidth, mapaY * tileHeight)
                    self.gunPickups.add(shieldPickup)

                if mapaX == 26 and mapaY == 31:
                    grenadeLauncher = GrenadeLauncher(mapaX * tileWidth, mapaY * tileHeight)
                    self.gunPickups.add(grenadeLauncher)

                if mapaX == 50 and mapaY == 31:
                    health = Health(mapaX * tileWidth, mapaY * tileHeight)
                    self.healthPickUps.add(health)

                if mapaX == 30 and mapaY == 31:
                    en = self.enemyFactory.createEnemy(mapaX * tileWidth, mapaY * tileHeight)
                    self.enemies.add(en)
                    print("A")

                if mapaX == 30 and mapaY == 31:
                    computer = Computer(mapaX * tileWidth, mapaY * tileHeight)
                    self.interactiveGroup.add(computer)
                    print("A")

                if mapaX == 30 and mapaY == 31:
                    textureRect = pygame.Rect(mapaX * tileWidth, mapaY * tileHeight, tileWidth,tileHeight)
                    self.terrainHitBoxList.append(textureRect)

                    en = self.enemyFactory.createEnemy2(mapaX * tileWidth, mapaY * tileHeight, textureRect)
                    self.destructibles_group.add(en)

                # Se actualiza la posicion del mapa
                mapaX += 1
                if mapaX >= anchuraMapa:
                    mapaX = 0
                    mapaY += 1

            
