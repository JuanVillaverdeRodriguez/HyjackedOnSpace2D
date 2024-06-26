from Entities.Enemies.Vonreg import Vonreg
from Entities.Enemies.barnacleEnemy import BarnacleEnemy
from Entities.Enemies.rahm import Rahm
from Entities.Enemies.rayEnemy import RayEnemy
from Entities.Enemies.shooterEnemy import ShooterEnemy
from .enemyFactory import EnemyFactory
from .flyingEnemy import FlyingEnemy
from .meleeEnemy import MeleeEnemy


class SelectedEnemyFactory(EnemyFactory):
    def __init__(self, bulletsGroup, grenadesGroup, uiBossHealthBar, uiCroshair, dificulty, gunPickups) -> None:
        self.bulletsGroup = bulletsGroup
        self.grenadesGroup = grenadesGroup
        self.uiBossHealthBar = uiBossHealthBar
        self.uiCroshair = uiCroshair
        self.dificulty = dificulty
        self.gunPickups = gunPickups    

    def createEnemy(self, columna, fila, enemyID, boss, enemies):
        en = None
        if enemyID == 15:
            if boss: # Apaño rapido... Si Vonreg fue derrotado, no vuelvas a spawnearlo
                en = Vonreg(columna, fila, self.grenadesGroup, self.dificulty, self.uiBossHealthBar, self.gunPickups)
                enemies.add(en)
        elif enemyID == 14:
            en = Rahm(columna, fila, self.bulletsGroup, self.dificulty, self.uiBossHealthBar, self.gunPickups, self.uiCroshair)
        elif enemyID == 12:
            en = RayEnemy(columna, fila,self.dificulty)
        elif enemyID == 13:
            en = BarnacleEnemy(columna, fila,self.dificulty)
        elif enemyID == 11:
            en = FlyingEnemy(columna, fila,self.dificulty, False, self.bulletsGroup)
        elif enemyID == 10:
            en = ShooterEnemy(columna, fila,self.dificulty, False, self.bulletsGroup)
        elif enemyID == 5:
            en = MeleeEnemy(columna, fila,self.dificulty, False, False, self.gunPickups)

        if enemyID != 15 or (enemyID == 15 and boss) and en != None:
            enemies.add(en)
            


