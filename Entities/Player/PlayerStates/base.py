import pygame

class pState(object):
    def __init__(self):
        self.animation = None
        self.next = None
        self.sprite_index = 0
    
    def next_sprite(self):
        self.sprite_index += 1
        if self.sprite_index == len(self.animation):
            self.sprite_index = 0
        return self.animation[self.sprite_index]

    def change_state(self):
        pass

    def update(self, dt):
        pass