from project.handler import *
from project.models import *

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

menu_scene = Scene('', Formatter.get_image('main_menu', ''))
game_scene = Scene('', Formatter.get_image('map', ''))

start_btn = Object(Formatter.get_image('start_btn', ''))
start_btn.locate(menu_scene, 510, 200)
start_btn.show()

exit_btn = Object(Formatter.get_image('exit_btn', ''))
exit_btn.locate(menu_scene, 510, 100)
exit_btn.show()


def start_game(x, y, action):
    start_btn.hide()
    exit_btn.hide()
    game_scene.enter()
    manager = GameManager(game_scene)
    manager.random_generate()
    startGame(game_scene)
    pass


def exit_game(x, y, action):
    endGame()


start_btn.onMouseAction = start_game
exit_btn.onMouseAction = exit_game
startGame(menu_scene)

