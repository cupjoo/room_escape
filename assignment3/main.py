from bangtal import *

start_scene = Scene("시작의 방", "images/배경-1.png")
end_scene = Scene("마지막 관문", "images/배경-2.png")
choice_scene = Scene("갈림길", "images/배경-2.png")
wrong_scene1 = Scene("막다른 방", "images/배경-2.png")
wrong_scene2 = Scene("Game Over", "images/배경-2.png")

door1 = Object('images/문-오른쪽-닫힘.png')
door1.locate(start_scene, 700, 290)
door1.closed = True
door1.show()

door2 = Object('images/문-오른쪽-닫힘.png')
door2.locate(start_scene, 900, 255)
door2.closed = True
door2.show()

door3 = Object('images/문-오른쪽-열림.png')
door3.locate(choice_scene, 320, 260)
door3.show()

door4 = Object('images/문-오른쪽-열림.png')
door4.locate(wrong_scene1, 320, 260)
door4.show()

door5 = Object('images/문-오른쪽-닫힘.png')
door5.locate(choice_scene, 850, 280)
door5.closed = True
door5.show()

door6 = Object('images/문-오른쪽-닫힘.png')
door6.locate(choice_scene, 1050, 245)
door6.closed = True
door6.show()

door7 = Object('images/문-오른쪽-열림.png')
door7.locate(end_scene, 320, 260)
door7.show()

door8 = Object('images/문-오른쪽-닫힘.png')
door8.locate(end_scene, 885, 270)
door8.locked = True
door8.show()

key1 = Object('images/열쇠.png')
key1.locate(choice_scene, 640, 150)
key1.setScale(0.2)
key1.show()

flowerpot1 = Object('images/화분.png')
flowerpot1.locate(choice_scene, 450, 150)
flowerpot1.moved = False
flowerpot1.show()

flowerpot2 = Object('images/화분.png')
flowerpot2.locate(choice_scene, 590, 150)
flowerpot2.moved = False
flowerpot2.show()

flowerpot3 = Object('images/화분.png')
flowerpot3.locate(choice_scene, 730, 150)
flowerpot3.moved = False
flowerpot3.show()

keypad = Object('images/키패드.png')
keypad.locate(end_scene, 865, 420)
keypad.show()

switch = Object('images/스위치.png')
switch.locate(end_scene, 860, 440)
switch.lighted = True
switch.show()

password = Object('images/암호.png')
password.locate(end_scene, 400, 100)


def door1_on_mouse_action(x, y, action):
    if door1.closed:
        door1.setImage('images/문-오른쪽-열림.png')
        door1.closed = False
    else:
        choice_scene.enter()


def door2_on_mouse_action(x, y, action):
    if door2.closed:
        door2.setImage('images/문-오른쪽-열림.png')
        door2.closed = False
    else:
        wrong_scene1.enter()
        showMessage('막다른 방인 것 같다.')


def door5_on_mouse_action(x, y, action):
    if key1.inHand() is False:
        showMessage('열쇠가 필요한 듯 하다.')
    else:
        if door5.closed:
            showMessage('문이 열렸다!')
            door5.setImage('images/문-오른쪽-열림.png')
            door5.closed = False
        else:
            wrong_scene2.enter()
            showMessage('Game Over')


def door6_on_mouse_action(x, y, action):
    if key1.inHand() is False:
        showMessage('열쇠가 필요한 듯 하다.')
    else:
        if door6.closed:
            showMessage('문이 열렸다!')
            door6.setImage('images/문-오른쪽-열림.png')
            door6.closed = False
        else:
            end_scene.enter()


def door8_on_mouse_action(x, y, action):
    if door8.locked:
        showMessage('비밀번호를 입력해야 할 것 같다.')
    else:
        endGame()


def return_start_scene_door_on_mouse_action(x, y, action):
    start_scene.enter()


def return_choice_scene_door_on_mouse_action(x, y, action):
    choice_scene.enter()


def flowerpot1_on_mouse_action(x, y, action):
    flowerpot1.locate(choice_scene, 450, 200)


def flowerpot2_on_mouse_action(x, y, action):
    flowerpot2.locate(choice_scene, 590, 200)


def flowerpot3_on_mouse_action(x, y, action):
    flowerpot3.locate(choice_scene, 730, 200)


def key1_on_mouse_action(x, y, action):
    key1.pick()


def keypad_on_mouse_action(x, y, action):
    showKeypad('bangtal', door8)


def switch_on_mouse_action(x, y, action):
    switch.lighted = not switch.lighted
    if switch.lighted:
        end_scene.setLight(1)
        password.hide()
    else:
        end_scene.setLight(0.2)
        password.show()


def door8_on_keypad():
    showMessage('문이 열렸다!')
    door8.locked = False
    door8.setImage('images/문-오른쪽-열림.png')


door1.onMouseAction = door1_on_mouse_action
door2.onMouseAction = door2_on_mouse_action
door3.onMouseAction = return_start_scene_door_on_mouse_action
door4.onMouseAction = return_start_scene_door_on_mouse_action
door5.onMouseAction = door5_on_mouse_action
door6.onMouseAction = door6_on_mouse_action
door7.onMouseAction = return_choice_scene_door_on_mouse_action
door8.onMouseAction = door8_on_mouse_action
door8.onKeypad = door8_on_keypad
flowerpot1.onMouseAction = flowerpot1_on_mouse_action
flowerpot2.onMouseAction = flowerpot2_on_mouse_action
flowerpot3.onMouseAction = flowerpot3_on_mouse_action
key1.onMouseAction = key1_on_mouse_action
keypad.onMouseAction = keypad_on_mouse_action
switch.onMouseAction = switch_on_mouse_action

showMessage('올바른 문을 찾아 방을 탈출하라!')
startGame(start_scene)
