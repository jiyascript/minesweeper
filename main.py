from tkinter import *
from tkinter import messagebox
import random
import time


class Cell:
    all_cells = []
    revealed_cells = 0
    non_mine = 0 
    total_mines = 0
    flags = 0
    t = None
    flag_label = None

    def __init__(self, row, col, is_mine=False):
        self.row = row
        self.col = col
        self.is_mine = is_mine
        self.neighboring_mines = 0
        self.revealed = False
        self.flagged = False
        self.btn = None
        Cell.all_cells.append(self)

    def btn_obj(self, master):
        self.btn = Button(master, width=2, height=1)
        self.btn.bind('<Button-1>', self.left_click)
        self.btn.bind('<Button-3>', self.right_click)
        return self.btn

    def left_click(self, event):
        if self.flagged:
            return
        if self.is_mine:
            self.reveal_mine()
        else:
            self.reveal_cell()
        self.btn.config(relief=SUNKEN)

    @staticmethod
    def game_win():
        if Cell.revealed_cells == Cell.non_mine and Cell.flags == Cell.total_mines:
            for cell in Cell.all_cells:
                cell.btn.unbind('<Button-1>')
                cell.btn.unbind('<Button-3>')
            if Cell.t:
                root.after_cancel(Cell.t)
            messagebox.showinfo("game over", "you won!")

    @staticmethod
    def game_over():
        for cell in Cell.all_cells:
            if cell.is_mine:
                cell.btn.config(relief=SUNKEN, text = "\U0001F4A3")
        for cell in Cell.all_cells:
            cell.btn.unbind('<Button-1>')
            cell.btn.unbind('<Button-3>')
        if Cell.t:
            root.after_cancel(Cell.t)
        messagebox.showinfo("game over", "you clicked on a mine")

    def cell_coords(self, row, col):
        for c in Cell.all_cells:
            if (c.row == row) and (c.col == col):
                return c

    @property
    def adjacent(self):
        neighbors = [
            self.cell_coords(self.row - 1, self.col - 1),
            self.cell_coords(self.row - 1, self.col),
            self.cell_coords(self.row - 1, self.col + 1),
            self.cell_coords(self.row, self.col - 1),
            self.cell_coords(self.row, self.col + 1),
            self.cell_coords(self.row + 1, self.col - 1),
            self.cell_coords(self.row + 1, self.col),
            self.cell_coords(self.row + 1, self.col + 1)
        ]
        neighbors = [neighbor for neighbor in neighbors if neighbor]
        return neighbors

    def reveal_cell(self):
        if self.revealed or self.flagged:
            return
        self.revealed = True
        Cell.revealed_cells += 1
        self.btn.config(relief=SUNKEN)
        for n in self.adjacent:
            if n.is_mine:
                self.neighboring_mines += 1
        if self.neighboring_mines > 0:
            self.btn.config(text=str(self.neighboring_mines))
        else:
            self.btn.config(text=str(self.neighboring_mines))
            for n in self.adjacent:
                n.reveal_cell()
        Cell.game_win()


    def right_click(self, event):
        if not self.revealed:
            if self.flagged:
                self.btn.config(text='')
                self.flagged = False
                Cell.flags -= 1
            else:
                self.btn.config(text='F')
                self.flagged = True
                Cell.flags += 1
            if Cell.flag_label:
                Cell.flag_label.config(text=f'flags: {Cell.flags}/{Cell.total_mines}')
        Cell.game_win()

    @staticmethod
    def assign_mines(mines):
        all_positions = [(cell.row, cell.col) for cell in Cell.all_cells]
        random.shuffle(all_positions)
        mine_positions = all_positions[:mines]
        for row, col in mine_positions:
            for cell in Cell.all_cells:
                if cell.row == row and cell.col == col:
                    cell.is_mine = True
        Cell.total_mines = mines
        Cell.non_mine = len(Cell.all_cells) - mines

    def reveal_mine(self):
        self.btn.config(text = "\U0001F4A3", relief=SUNKEN)
        Cell.game_over()


def create_grid(game_window, rows, columns):
    grid = []
    for i in range(rows):
        row = []
        for j in range(columns):
            cell = Cell(i, j)
            cell.btn_obj(game_window)
            cell.btn.grid(row=i, column=j)
            row.append(cell)
        grid.append(row)
    return grid

def new_window(rows, columns, mines):
    game_window = Toplevel(root)
    game_window.title(f'Minesweeper - {level}')
    grid = create_grid(game_window, rows, columns)
    Cell.assign_mines(mines)
    Cell.flags = 0
    flag_label = Label(game_window, text=f'flags: {Cell.flags}/{Cell.total_mines}')
    flag_label.grid(row=rows, column=0, columnspan=columns)
    timer = Label(game_window, text="time: 00:00")
    timer.grid(row=rows+1, column=0, columnspan=columns)
    start_time = time.time()
    timer_update(timer, start_time)
    Cell.flag_label = flag_label
    return flag_label

def beginner():
    global level
    level = 'Beginner'
    rows = 9
    columns = 9
    mines = 10
    new_window(rows, columns, mines)

def intermediate():
    global level
    level = 'Intermediate'
    rows = 16
    columns = 16
    mines = 40
    new_window(rows, columns, mines)

def expert():
    global level
    level = 'Expert'
    rows = 24
    columns = 24
    mines = 99
    new_window(rows, columns, mines)

def timer_update(label, start_time):
    elapsed = int(time.time() - start_time)
    mins = elapsed // 60
    secs = elapsed % 60
    label.config(text=f'time: {mins:02}:{secs:02}')
    Cell.t = label.after(1000, timer_update, label, start_time)

root = Tk()
root.geometry('400x200')
root.resizable(False, False)
root.title("Play Minesweeper!")

Label(root, text="choose difficulty level", font=("Arial", 15)).pack(pady = 5)
Button(root, text="beginner", command=beginner).pack(padx=10, pady = 10)
Button(root, text="intermediate", command=intermediate).pack(padx=10,pady = 10)
Button(root, text="expert", command=expert).pack(padx=10,pady = 10)

root.mainloop()
