import threading
import time

class Shield(): 
    def __init__(self, image) -> None:
        self.originalImage = image
        self.shieldImage = image
        self.shieldRect = image.get_rect()
        self.energy = 10
        
        self.minTimeWithoutHits = 120
        self.timeWithoutHits = self.minTimeWithoutHits

        self.minChargeDelay = 15
        self.chargeDelay = self.minChargeDelay 
        self.uiShieldObservers = []

        
    def update(self, player):
        self.shieldRect.x = player.position().x - 45
        self.shieldRect.y = player.position().y - 37

        if self.energy < 11:
            self.timeWithoutHits -= 1
            self.chargeDelay -= 1

            if self.timeWithoutHits < 0:
                if self.chargeDelay < 0:
                    self.chargeDelay = self.minChargeDelay
                    self.charge()
                    player.notify()
    
    def draw(self, screen):
        screen.blit(self.shieldImage, self.shieldRect)
        
    def deflect(self, hitImage):
        self.shieldImage = hitImage
        self.iniciar_proceso_de_cambio_de_imagen()
        if not self.energy == 0:
            self.energy -= 1
        self.timeWithoutHits = self.minTimeWithoutHits
        self.notify()
        

    def charge(self):
        self.energy += 1
        self.notify()

    def getShieldHp(self):
        return self.energy

    def cambiar_imagen_despues_de_retraso(self):
        time.sleep(0.2)  # Espera 3 segundos
        self.shieldImage = self.originalImage  # Cambia la imagen después del retraso

    def iniciar_proceso_de_cambio_de_imagen(self):
        thread = threading.Thread(target=self.cambiar_imagen_despues_de_retraso)
        thread.start()

    def addObserver(self, observer):
        self.uiShieldObservers.append(observer)

    def delObserver(self, observer):
        self.uiShieldObservers.remove(observer)
        
    def notify(self):
        for observer in self.uiShieldObservers:
            observer.update(self)