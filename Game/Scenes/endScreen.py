import pygame
from .scene import Scene
import Game.Scenes.menu as menu
import Game.Scenes.level3 as level3
import Game.Scenes.level4 as level4
import Game.Scenes.level2 as level2
import Game.Scenes.level1 as level1
import Constants.constants as c

class EndScreen(Scene):
    def __init__(self,director, persist):
        super(EndScreen, self).__init__(director, persist)
        self.title = self.font.render("Game Over", True, pygame.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.instructions = self.font.render("Enhorabuena has completado el juego",
                                             True, pygame.Color("white"))
        instructions_center = (self.screen_rect.center[0], self.screen_rect.center[1] + 50)
        self.instructions_rect = self.instructions.get_rect(center=instructions_center)

    def manageJoystick(self, joystick):
        if joystick.get_button(9):  
            scene = menu.Menu(self.director)
            self.director.changeScene(scene)
        if joystick.get_button(2):
            self.director.finishScene()

    def events(self, events, keys, joysticks):
        for event in events:
            if event.type == pygame.QUIT:
                self.director.endApplication()

        for joystick in joysticks.values():
            self.manageJoystick(joystick)

        if keys[pygame.K_RETURN]:  
            self.director.endApplication()
        if keys[pygame.K_SPACE]:
            self.director.endApplication()
        if keys[pygame.K_ESCAPE]:
            self.director.endApplication()
    
    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)
        surface.blit(self.instructions, self.instructions_rect)