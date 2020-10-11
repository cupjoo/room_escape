from project.handler import *
from project.models import *


start_scene = Scene("", "images/map.png")
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

manager = GameManager(start_scene)
manager.random_generate()

startGame(start_scene)




startGame(start_scene)
