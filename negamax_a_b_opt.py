from tkinter import *
from math import inf
from datetime import datetime


class Node():
    def __init__(self, state, pos, player):
        self.state = state
        self.state[pos] = player
        self.value = score(self.state, pos)


def score(state, pos):
    lines = ((0, 1, 2),
             (3, 4, 5),
             (6, 7, 8),
             (0, 3, 6),
             (1, 4, 7),
             (2, 5, 8),
             (0, 4, 8),
             (2, 4, 6))
    for line in lines:
        if pos in line:    
            if 1 == state[line[0]] == state[line[1]] == state[line[2]]:
                return state.count(0) + 1
            elif -1 == state[line[0]] == state[line[1]] == state[line[2]]:
                return -1 * state.count(0) - 1
    if 0 not in state:
        return 0
    else:
        return


def evaluate(state):
    node = Node([0] * 9, 0, 0)
    node.state = state
    if state.count(0) % 2:
        pov = 1
    else:
        pov = -1
    plays, search = negamax(node, pov, -inf, inf, 0, 0)
    best = pov * max(pov * i for i in plays)
    ind = plays.index(best)
    play = search[ind]
    return play


def negamax(node, pov, alpha, beta, depth, ends):
    depth += 1
    if node.state.count(0) % 2:
        player = 1
    else:
        player = -1
    children = []
    search = search_order(node.state)
    for pos in search:
        if alpha >= beta:
            break
        child = Node(list(node.state), pos, player)
        if child.value is not None:
            value = child.value
            children.append(value)
            ends += 1
        else:
            value, ends = negamax(child, -pov, alpha, beta, depth, ends)
            children.append(value)
        if pov == 1:
            if value > alpha:
                alpha = value
        else:
            if value < beta:
                beta = value
    best = pov * max(pov * i for i in children)
    if depth == 1:
        print("ends", ends)
        return children, search
    else:
        return (best, ends)


def search_order(state):
    search = [i for i in range(9) if state[i] == 0]
    lines = ((0, 1, 2),
             (3, 4, 5),
             (6, 7, 8),
             (0, 3, 6),
             (1, 4, 7),
             (2, 5, 8),
             (0, 4, 8),
             (2, 4, 6))
    sum_line = lambda state, line: state[line[0]] + state[line[1]] + state[line[2]]
    for line in lines:
        if sum_line(state, line) == 2 or sum_line(state, line) == -2:
            cell = line[[state[i] for i in line].index(0)]
            search.remove(cell)
            search.insert(0, cell)
            return search
    else:
        return search


class Window():
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.geometry("300x300")

        self.frame1 = Frame(self.master)
        self.frame1.pack()

        self.label = Label(self.frame1, text="Would you like to go first or second?")
        self.label.pack()

        self.first = Button(self.frame1, text="First (play as X)", command=lambda: self.symbol(1))
        self.second = Button(self.frame1, text="Second (play as O)", command=lambda: self.symbol(-1))
        self.first.pack()
        self.second.pack()

    def symbol(self, symbol):
        self.player = symbol
        if self.player == 1:
            self.opponent = -1
            self.xo_player = 'X'
            self.xo_opponent = 'O'
        else:
            self.opponent = 1
            self.xo_player = 'O'
            self.xo_opponent = 'X'

        self.frame1.destroy()
        try:
            self.frame2.destroy()
        except AttributeError:
            pass
        try:
            self.frame3.destroy()
        except AttributeError:
            pass

        self.frame2 = Frame(self.master)
        self.frame2.pack()

        self.grid = [0, 0, 0,
                     0, 0, 0,
                     0, 0, 0]

        self.t_list = []
        for i in range(9):
            self.t_list.append(StringVar())

        self.b_list = []
        self.b_list.append(Button(self.frame2, textvariable=self.t_list[0], command=lambda: self.play(0)))
        self.b_list.append(Button(self.frame2, textvariable=self.t_list[1], command=lambda: self.play(1)))
        self.b_list.append(Button(self.frame2, textvariable=self.t_list[2], command=lambda: self.play(2)))
        self.b_list.append(Button(self.frame2, textvariable=self.t_list[3], command=lambda: self.play(3)))
        self.b_list.append(Button(self.frame2, textvariable=self.t_list[4], command=lambda: self.play(4)))
        self.b_list.append(Button(self.frame2, textvariable=self.t_list[5], command=lambda: self.play(5)))
        self.b_list.append(Button(self.frame2, textvariable=self.t_list[6], command=lambda: self.play(6)))
        self.b_list.append(Button(self.frame2, textvariable=self.t_list[7], command=lambda: self.play(7)))
        self.b_list.append(Button(self.frame2, textvariable=self.t_list[8], command=lambda: self.play(8)))

        self.b_list[0].grid(row=0, column=0)
        self.b_list[1].grid(row=0, column=1)
        self.b_list[2].grid(row=0, column=2)
        self.b_list[3].grid(row=1, column=0)
        self.b_list[4].grid(row=1, column=1)
        self.b_list[5].grid(row=1, column=2)
        self.b_list[6].grid(row=2, column=0)
        self.b_list[7].grid(row=2, column=1)
        self.b_list[8].grid(row=2, column=2)

        if self.opponent == 1:
            self.comp_turn()

    def play(self, pos):
        self.b_list[pos].config(state="disabled")
        self.t_list[pos].set(self.xo_player)
        self.grid[pos] = self.player
        if self.check_endgame():
            self.comp_turn()

    def comp_turn(self):
        t = datetime.now()
        move = evaluate(self.grid)
        self.grid[move] = self.opponent
        self.b_list[move].config(state="disabled")
        self.t_list[move].set(self.xo_opponent)
        print(datetime.now() - t)
        self.check_endgame()

    def check_endgame(self):
        lines = ((0, 1, 2),
                 (3, 4, 5),
                 (6, 7, 8),
                 (0, 3, 6),
                 (1, 4, 7),
                 (2, 5, 8),
                 (0, 4, 8),
                 (2, 4, 6))
        for i in lines:
            if self.grid[i[0]] == self.grid[i[1]] == self.grid[i[2]] == self.player:
                self.finish(1)
                break
            elif self.grid[i[0]] == self.grid[i[1]] == self.grid[i[2]] == self.opponent:
                self.finish(-1)
                break
        else:
            if 0 not in self.grid:
                self.finish(0)
            else:
                return True

    def finish(self, state):
        [i.config(state="disabled") for i in self.b_list]
        if state == 1:
            label_text = ("You win! (not sure how you managed that....)\n"
                          "Play again?")
        elif state == -1:
            label_text = ("You lost. Better luck next time.\n"
                          "Play again?")
        else:
            label_text = ("You tied.\n"
                          "Play again?")

        self.frame3 = Frame(self.master)
        self.frame3.pack()
        self.label = Label(self.frame3, text=label_text)
        self.label.pack()

        self.first = Button(self.frame3, text="First (play as X)", command=lambda: self.symbol(1))
        self.second = Button(self.frame3, text="Second (play as O)", command=lambda: self.symbol(-1))
        self.quit = Button(self.frame3, text="Exit", command=lambda: self.exit())
        self.first.pack()
        self.second.pack()
        self.quit.pack()

    def exit(self):
        self.master.destroy()


root = Tk()
Window(root)
root.mainloop()
