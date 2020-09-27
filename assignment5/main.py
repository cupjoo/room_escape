from bangtal import *
import random

limit_time = 3600
board = []
min_record = limit_time

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
scene = Scene('그림퍼즐', 'images/background.png')

main_menu = Object('images/main.png')
main_menu.enabled = False
main_menu.locate(scene, 220, 0)
main_menu.show()

start_button = Object('images/start_button.png')
start_button.locate(scene, 510, 100)
start_button.show()

exit_button = Object('images/exit_button.png')
exit_button.locate(scene, 510, 20)
exit_button.show()

max_score_button = Object('images/max_score_button.png')
max_score_button.locate(scene, 860, 660)
max_score_button.show()

give_up_button = Object('images/give_up_button.png')
give_up_button.locate(scene, 240, 660)

timer = Timer(limit_time)


class Puzzle(Object):
    def __init__(self, r, c, img, idx):
        super().__init__('images/' + img + str(idx) + '.png')
        self.r = r
        self.c = c
        self.idx = idx
        self.sz = 196
        self.setScale(0.7)
        self.locate(scene, self.r, self.c)

    def locate(self, scene, r, c):
        self.r = r
        self.c = c
        board[self.r][self.c] = self
        super().locate(scene, 350 + c*self.sz, 80 + (2-r)*self.sz)

    def move(self):
        dc = [-1, 1, 0, 0]
        dr = [0, 0, 1, -1]
        for i in range(4):
            nc = self.c + dc[i]
            nr = self.r + dr[i]
            if nc < 0 or nc > 2 or nr < 0 or nr > 2:
                continue
            if board[nr][nc] is not None:
                continue
            board[self.r][self.c] = None
            self.locate(scene, nr, nc)
            break

    def onMouseAction(self, x, y, action):
        self.move()
        check_board()

    def is_right_pos(self, idx):
        return self.idx == idx


def check_board():
    for r in range(3):
        for c in range(3):
            if board[r][c] is None:
                continue
            if not board[r][c].is_right_pos(r*3+c):
                return
    end_puzzle(True)


def shuffle():
    r = 2
    c = 2
    dc = [-1, 1, 0, 0]
    dr = [0, 0, 1, -1]
    for i in range(100):
        d = random.randrange(0, 4)
        while True:
            nr = r + dr[d]
            nc = c + dc[d]
            if 0 <= nc < 3 and 0 <= nr < 3:
                r = nr
                c = nc
                board[r][c].move()
                break
            d = (d+1) % 4


def start_puzzle(name):
    main_menu.enabled = False
    main_menu.hide()
    give_up_button.show()
    max_score_button.show()
    timer.set(limit_time)

    global board
    board = [[None, None, None], [None, None, None], [None, None, None]]
    for r in range(3):
        for c in range(3):
            if r*3+c == 8:
                continue
            puzzle = Puzzle(r, c, name, r*3+c)
            puzzle.show()
    shuffle()
    timer.start()


def end_puzzle(cleared):
    global board, min_record
    for p in board:
        for c in p:
            if c is None:
                continue
            c.hide()
    board = []
    timer.stop()
    if cleared:
        record = limit_time-int(timer.get())
        message = '걸린 시간: '+str(int(record/60))+'분 '+str(record % 60)+'초'
        if record < min_record:
            min_record = record
            message += ' (최고기록 갱신!)'
        showMessage(message)
    else:
        showMessage('Game Over')
    timer.set(limit_time)
    main_menu.show()
    start_button.show()
    exit_button.show()
    give_up_button.hide()
    max_score_button.show()
    main_menu.enabled = False


def select_puzzle():
    start_button.hide()
    exit_button.hide()
    max_score_button.hide()
    main_menu.enabled = True
    showMessage('원하는 그림을 선택해주세요!')


def give_up(x, y, action):
    end_puzzle(False)


def game_over():
    end_puzzle(False)


def exit_game(x, y, action):
    endGame()


def menu_on_mouse_action(x, y, action):
    if main_menu.enabled is False:
        return
    name = ['lion', 'giraffe', 'elephant']
    for i in range(len(name)):
        if x < (i+1)*280:
            start_puzzle(name[i])
            return


def start_button_on_mouse_action(x, y, action):
    select_puzzle()


def max_score_button_on_mouse_action(x, y, action):
    minutes = str(int(min_record/60))
    seconds = str(min_record % 60)
    showMessage('최고 기록 : '+minutes+':'+seconds)


main_menu.onMouseAction = menu_on_mouse_action
start_button.onMouseAction = start_button_on_mouse_action
exit_button.onMouseAction = exit_game
give_up_button.onMouseAction = give_up
max_score_button.onMouseAction = max_score_button_on_mouse_action
timer.onTimeout = game_over
startGame(scene)
