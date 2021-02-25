import tkinter as tk
import random as r
import color as c

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        #Create the root
        self.grid()
        self.main_grid = tk.Frame(self, height=600, width=600, bd=5, bg=c.GRID_COLOR)
        self.main_grid.grid(pady=(115,0))
#VS
       #self.main_grid = tk.Frame(self, height=600, width=600, bd=3, bg=c.GRID_COLOR).grid(pady=(100,0))
        self.score=0
        self.master.title('2048')
        self.make_GUI()
        self.start_game()

        self.master.bind('<Left>',self.left)
        self.master.bind('<Right>',self.right)
        self.master.bind('<Up>',self.up)
        self.master.bind('<Down>',self.down)
        self.mainloop()


    def make_GUI(self):
        #Creating the outlook
        self.cell = []
        for i in range (4):
            row = []
            for j in range(4):
                my_cell = tk.Frame(self.main_grid, width=150, height=150, bg=c.EMPTY_CELL_COLOR)
                my_cell.grid(row=i, column=j, padx=5, pady=5)
                my_label = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                my_label.grid(row=i, column=j)
                cell_data = {'frame': my_cell, 'number': my_label}
                row.append(cell_data)
            self.cell.append(row)

        #Making the socre line
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=50, anchor='center')
        score_label = tk.Label(score_frame, text='score', font=c.SCORE_LABEL_FONT)
        score_label.grid(row=0)
        self.score_label = tk.Label(score_frame, font=c.SCORE_FONT)
        self.score_label.grid(row=1)

    def start_game(self):
        self.matrix = [[0]*4 for i in range(4)]
        for _ in range (2):
            x = r.choice(range(4))
            y = r.choice(range(4))
            self.matrix[x][y] = r.choice([2,2,2,2,2,4])
            if self.matrix[x][y] == 2:
                self.cell[x][y]['frame'].configure(bg=c.CELL_COLORS[2])
                self.cell[x][y]['number'].configure(bg=c.CELL_COLORS[2], font=c.CELL_NUMBER_FONTS[2], fg=c.CELL_NUMBER_COLORS[2], text='2')
            else:
                self.cell[x][y]['frame'].configure(bg=c.CELL_COLORS[4])
                self.cell[x][y]['number'].configure(bg=c.CELL_COLORS[4], font=c.CELL_NUMBER_FONTS[4], fg=c.CELL_NUMBER_COLORS[4], text='4')
        self.score_label.configure(text=0)
    
    def move(self):
        matrix = [[0]*4 for i in range(4)]
        for i in range (4):
            fill = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    matrix[i][fill] = self.matrix[i][j]
                    fill += 1
        self.matrix = matrix
        
    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0 
                    self.score += self.matrix[i][j]

    def reverse(self):
        new_matrix = []
        for i in range (4):
            temp = []
            for j in range (4):
                temp.append(self.matrix[i][3-j])
            new_matrix.append(temp)
        self.matrix = new_matrix
    
    def transpose(self):
        new_matrix = [[0]*4 for i in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    def add_new_tile(self):
        x = r.randint(0,3)
        y = r.randint(0,3)
        while(self.matrix[x][y] != 0):
            x = r.randint(0,3)
            y = r.randint(0,3)
        self.matrix[x][y] = 2

    def update(self):
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] == 0:
                    self.cell[i][j]['frame'].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cell[i][j]['number'].configure(bg=c.EMPTY_CELL_COLOR, text='')
                else:
                    self.cell[i][j]['frame'].configure(bg=c.CELL_COLORS[self.matrix[i][j]])
                    self.cell[i][j]['number'].configure(bg=c.CELL_COLORS[self.matrix[i][j]], font=c.CELL_NUMBER_FONTS[self.matrix[i][j]], fg=c.CELL_NUMBER_COLORS[self.matrix[i][j]], text=str(self.matrix[i][j])) 

        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def move_exist(self):
        for i in range(4):
            for j in range(4):
                if j+1 <= 3 and i+1 <= 3 and self.matrix[i][j] == self.matrix[i][j+1] and self.matrix[i][j] == self.matrix[i+1][j]:
                    return False
        return True

    def win_or_lose(self):
        if any(2048 in row for row in self.matrix):
            winner_frame = tk.Frame(self.main_grid, boarderwidth=2)
            winner_frame.place(relx=0.5, rely=0.5, anchor='center')
            tk.Label(winner_frame, text="You Win!", bg=c.WINNER_BG, fg=c.GAME_OVER_FONT_COLOR, font=c.GAME_OVER_FONT).pack()
        
        if not(any(0 in row for row in self.matrix)) and not(self.move_exist()):
            winner_frame = tk.Frame(self.main_grid, boarderwidth=2)
            winner_frame.place(relx=0.5, rely=0.5, anchor='center')
            tk.Label(winner_frame, text="You Lose!", bg=c.WINNER_BG, fg=c.GAME_OVER_FONT_COLOR, font=c.GAME_OVER_FONT).pack()
            


    def left(self,event):
        self.move()
        self.combine()
        self.move()
        self.add_new_tile()
        self.update()
        self.win_or_lose()


    def right(self,event):
        self.reverse()
        self.move()
        self.combine()
        self.move()
        self.reverse()
        self.add_new_tile()
        self.update()
        self.win_or_lose()


    def up(self,event):
        self.transpose()
        self.move()
        self.combine()
        self.move()
        self.transpose()
        self.add_new_tile()
        self.update()
        self.win_or_lose()


    def down(self,event):
        self.transpose()
        self.reverse()
        self.move()
        self.combine()
        self.move()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update()
        self.win_or_lose()
    
def main():
    Game()

if __name__ == '__main__':
    main()
