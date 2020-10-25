from bangtal import *
from enum import Enum


setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

dx = [-1, 0, 1, 1, 1, 0, -1, -1]
dy = [-1, -1, -1, 0, 1, 1, 1, 0]


class State(Enum):
    BLANK = 0
    POSSIBLE = 1
    BLACK = 2
    WHITE = 3


class Turn(Enum):
    BLACK = 1
    WHITE = 2


class Computer(Timer):
    def __init__(self, delay):
        self.delay = delay
        super().__init__(self.delay)

    def play(self):
        global queue, turn
        pot = None
        max_cnt = 0
        for q in queue:
            cnt = 0
            for i in range(8):
                cnt += count_score(q.x, q.y, i)
            if max_cnt < cnt:
                max_cnt = cnt
                pot = q
        if max_cnt > 0:
            pot.change_state(State.WHITE)
            pot.reverse()
        turn = Turn.BLACK
        if not reset_pots():
            turn = Turn.WHITE if turn == Turn.BLACK else Turn.BLACK
            if not reset_pots():
                end_game()
        queue = []

    def onTimeout(self):
        self.play()
        self.set(self.delay)


start_scene = Scene('', 'images/background.png')
turn = Turn.BLACK
board = []
queue = []
computer = Computer(0.3)


class Stone(Object):
    def __init__(self, scene, x, y):
        super().__init__('')
        self.x = x
        self.y = y
        self.locate(scene, 40 + self.x*80, 120 + self.y*80)
        self.state = None
        self.change_state(State.BLANK)
        self.show()

    def change_state(self, state):
        global turn, queue
        self.state = state
        mapper = {State.BLANK: 'blank', State.BLACK: 'black', State.WHITE: 'white', State.POSSIBLE: 'possible'}
        img = mapper[state]
        if state == State.POSSIBLE:
            img = ('black_' if turn == Turn.BLACK else 'white_') + img
        self.setImage('images/'+img+'.png')
        if state == State.POSSIBLE and turn == Turn.WHITE:
            queue.append(self)

    def is_state(self, state):
        return self.state == state

    def reverse(self):
        me = State.BLACK if turn == Turn.BLACK else State.WHITE
        op = State.BLACK if turn == Turn.WHITE else State.WHITE
        for i in range(8):
            reverse_xy_dir(self.x, self.y, i, me, op)

    def onMouseAction(self, x, y, action):
        global turn
        if self.is_state(State.POSSIBLE):
            if turn == Turn.WHITE:
                return
            self.change_state(State.BLACK)
            self.reverse()
            turn = Turn.WHITE
            if not reset_pots():
                turn = Turn.WHITE if turn == Turn.BLACK else Turn.BLACK
                if not reset_pots():
                    end_game()
            computer.start()


def is_possible_dir(x, y, d):
    me = State.BLACK if turn == Turn.BLACK else State.WHITE
    op = State.BLACK if turn == Turn.WHITE else State.WHITE

    possible = False
    while True:
        x += dx[d]
        y += dy[d]
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        if board[y][x].is_state(op):
            possible = True
            continue
        elif board[y][x].is_state(me):
            return possible
        return False


def is_possible_pot(x, y):
    if board[y][x].is_state(State.BLACK) or board[y][x].is_state(State.WHITE):
        return False
    board[y][x].change_state(State.BLANK)
    for i in range(8):
        if is_possible_dir(x, y, i):
            return True
    return False


def reset_pots():
    possible = False
    for y in range(8):
        for x in range(8):
            if is_possible_pot(x, y):
                board[y][x].change_state(State.POSSIBLE)
                possible = True
    return possible


def reverse_xy_dir(x, y, d, me, op):
    possible = False
    while True:
        x += dx[d]
        y += dy[d]
        if x < 0 or x > 7 or y < 0 or y > 7:
            return

        pot = board[y][x]
        if pot.is_state(op):
            possible = True
        elif pot.is_state(me):
            if possible:
                while True:
                    x -= dx[d]
                    y -= dy[d]
                    pot = board[y][x]
                    if pot.is_state(op):
                        board[y][x].change_state(me)
                    else:
                        return
        else:
            return


def computer_play():
    global queue, turn
    pot = None
    max_cnt = 0
    for q in queue:
        cnt = 0
        for i in range(8):
            cnt += count_score(q.x, q.y, i)
        if max_cnt < cnt:
            max_cnt = cnt
            pot = q
    pot.change_state(State.WHITE)
    pot.reverse()
    turn = Turn.BLACK
    if not reset_pots():
        turn = Turn.WHITE if turn == Turn.BLACK else Turn.BLACK
        if not reset_pots():
            end_game()
    queue = []


def count_score(x, y, d):
    possible = False
    score = 0
    while True:
        x += dx[d]
        y += dy[d]
        if x < 0 or x > 7 or y < 0 or y > 7:
            return 0

        pot = board[y][x]
        if pot.is_state(State.BLACK):
            possible = True
            score += 1
        elif pot.is_state(State.WHITE):
            if possible:
                return score
        else:
            return score


def show_score(num, x):
    y = 215
    if num[0] > 0:
        ten = Object('images/L'+str(num[0])+'.png')
        ten.locate(start_scene, x, y)
        ten.show()
        x += 70
    one = Object('images/L' + str(num[1]) + '.png')
    one.locate(start_scene, x, y)
    one.show()


def end_game():
    black_cnt = 0
    white_cnt = 0
    for r in range(8):
        for c in range(8):
            black_cnt += 1 if board[r][c].is_state(State.BLACK) else 0
            white_cnt += 1 if board[r][c].is_state(State.WHITE) else 0
    left = [int(black_cnt / 10), black_cnt % 10]
    right = [int(white_cnt / 10), white_cnt % 10]
    show_score(left, 755)
    show_score(right, 1075)
    showMessage('게임이 종료됐습니다.')


for y in range(8):
    board.append([])
    for x in range(8):
        board[y].append(Stone(start_scene, x, y))

board[3][3].change_state(State.BLACK)
board[4][4].change_state(State.BLACK)
board[3][4].change_state(State.WHITE)
board[4][3].change_state(State.WHITE)

reset_pots()

startGame(start_scene)
