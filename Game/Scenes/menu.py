import pygame
from Constants.constants import *

from Game.Scenes.dificultySelector import DificultySelector
from Game.Scenes.perifericSelectorMenu import PerifericSelector
from .scene import Scene
from .options import Settings

class Menu(Scene):
    def __init__(self,director):
        super(Menu, self).__init__(director)
        self.active_index = 0
        self.options = ["Play", "Options", "Quit"]
        # pygame.mixer.Sound('Assets/Audio/MainMenu.mp3')
    
    # Funcion renderiza el texto del menu, pone azul la opcion que 
    # se esta seleccionando
    def render_text(self, index):
        color = pygame.Color("blue") if index == self.active_index else pygame.Color("white")
        return self.font.render(self.options[index], True, color)
    
    def get_text_position(self, text, index):
        center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 50))
        return text.get_rect(center=center)
    
    def handle_action(self):
        if self.active_index == 0:
            scene = DificultySelector(self.director)
            self.director.stackScene(scene)
        elif self.active_index == 1:
            scene = Settings(self.director)
            self.director.stackScene(scene)
        elif self.active_index == 2:
            self.director.endApplication()
    
    # Maneja la transicion entre las opciones del menu
    def events(self, events, keys, joysticks):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.endApplication()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.active_index -= 1 if self.active_index >= 1 else 0
                elif event.key == pygame.K_DOWN:
                    self.active_index += 1 if self.active_index < 2 else 0
                elif event.key == pygame.K_RETURN:
                    self.handle_action()
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                scene = PerifericSelector(self.director, joy.get_name())
                self.director.changeScene(scene)
            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                
            if event.type == pygame.JOYBUTTONDOWN:
                
                if event.button == 2:
                    self.handle_action()
            for joystick in joysticks.values():
                hats = joystick.get_numhats()
                for i in range(hats):
                    hat = joystick.get_hat(i)
                    if hat[1] == 1:
                        self.active_index -= 1 if self.active_index >= 1 else 0
                    if hat[1] == -1:
                        self.active_index += 1 if self.active_index < 2 else 0


    def update(self, *args):
        pass 
    
    def draw(self, surface):
        spaceBackground = pygame.transform.scale(pygame.image.load(LVLS_PATH + '/space2.jpg'), (SCREEN_WIDTH,SCREEN_HEIGTH)).convert()
        spaceBackgroundRect = spaceBackground.get_rect()
        surface.blit(spaceBackground,spaceBackgroundRect)
        #self.music.play()
        for index, option in enumerate(self.options):
            text_render = self.render_text(index)
            surface.blit(text_render, self.get_text_position(text_render, index))