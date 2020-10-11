from project.handler import *
from project.models import *


start_scene = Scene("", "images/map.png")
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

handler = EventHandler()

monster_x = 1080
monster_y = 0
yd = 140

cannon_x = 100
cannon_y = 280

handler.add_creature(Warrior(monster_x, monster_y, start_scene))
monster_y += yd
handler.add_creature(Zombie(monster_x, monster_y, start_scene))
monster_y += yd
handler.add_creature(Boss(monster_x, monster_y, start_scene))
monster_y += yd
handler.add_creature(Zombie(monster_x, monster_y, start_scene))
monster_y += yd
handler.add_creature(Warrior(monster_x, monster_y, start_scene))
monster_y += yd

handler.add_tower(Tank(cannon_x, cannon_y, start_scene))

startGame(start_scene)
