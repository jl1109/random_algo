class Sudoku:
    
    def solveSuduko(self, board):
        self.board = board
        self.solve()
    
    def find_blank(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == '.':
                    return r,c
        
        return False, False
    
    def solve(self):
        row, col = self.find_blank()
        if row == False and col == False:
            return True
        for num in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if self.is_valid(row, col , num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = '.'
        return False
    
    def is_valid(self, row, col, num):
        sr = row - row%3
        sc = col - col%3
        if self.row_check(row,num) and self.col_check(col,num) and self.square_check(sr,sc,num):
            return True
        return False

    def row_check(self,row,num):
        for col in range(9):
            if self.board[row][col] == num:
                return False
        return True
    
    def col_check(self, col, num):
        for row in range(9):
            if self.board[row][col] == num:
                return False
        return True
    
    def square_check(self, sr, sc, num):
        for r in range(row, row + 3):
            for c in range(col , col + 3):
                if self.board[r][c] == num:
                    return False

        return True
