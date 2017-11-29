class Space(object):
    def __init__(self, row_in, col_in, poss_in):
        self.row = row_in
        self.col = col_in
        self.outties = poss_in
        self.affected = []
        self.value = "0"

class Solution(object):
    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """

    def __init__(self, board_in):
        self.row_dict = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
        self.col_dict = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
        self.block_groups = [[ [], [], [] ],
                           [ [], [], [] ],
                           [ [], [], [] ] ]
        self.outties = []
        self.innies = []
        self.perm_innies = set()
        self.board = board_in
        self.open = [] # list of spaces!
        self.parse_board()
        self.counter = 0
    
    def calc_possible_num(self,row,col):
        all_nums = {'1','2','3','4','5','6','7','8','9'}
        set1 = set()
        set2 = set()
        set3 = set()

        for i in range(0,9):
            if(self.board[row][i] != '.'):
                set1.add(self.board[row][i])
            if(self.board[i][col] != '.'):
                set2.add(self.board[i][col])
        block_range = [int(row/3), int(col/3)]
        for i in range(block_range[0]*3, block_range[0]*3+3):
            for j in range(block_range[1]*3, block_range[1]*3+3):
                if(self.board[i][j] != '.'):
                    set3.add(self.board[i][j])
        possibilities = list(all_nums.difference(set1, set2, set3))
        result = Space(row, col, possibilities)
        rand_int = -1
        if(len(possibilities) == 1):
            self.board[row][col] = "".join(possibilities)
            self.remove_possibilities(result, next(iter(possibilities)), rand_int)
        
        return result

    def parse_board(self):
        counter = -1
        for i in range(0,9):
            for j in range(0,9):
                if (self.board[i][j] == "."):
                    space = self.calc_possible_num(i,j)
                    if(len(space.outties) != 1):
                        counter += 1
                        self.row_dict[i].append(counter)
                        self.col_dict[j].append(counter)
                        self.block_groups[int(i/3)][int(j/3)].append(counter)
                        self.open.append(space)
                        self.outties.append(counter)
    
    def remove_possibilities(self, space, val, cur_idx):
        need_removals = []
        for idx in self.row_dict[space.row]:
            try:
                if((idx == cur_idx) or (idx in self.perm_innies)):
                    continue
                self.open[idx].outties.remove(val)
                space.affected.append(idx)
                if len(self.open[idx].outties) == 0:
                    return False
                if (len(self.open[idx].outties) == 1):
                    new_val = "".join(self.open[idx].outties)
                    self.innies.append(idx)
                    self.outties.remove(idx)
                    self.board[self.open[idx].row][self.open[idx].col] = new_val
                    self.open[idx].value = new_val
                    need_removals.append(idx)
            except ValueError:
                continue
        for idx in self.col_dict[space.col]:
            try:
                if((idx == cur_idx) or (idx in self.perm_innies)):
                    continue
                self.open[idx].outties.remove(val)
                space.affected.append(idx)
                if len(self.open[idx].outties) == 0:
                    return False
                if (len(self.open[idx].outties) == 1):
                    new_val = "".join(self.open[idx].outties)
                    self.innies.append(idx)
                    self.outties.remove(idx)
                    self.board[self.open[idx].row][self.open[idx].col] = new_val
                    self.open[idx].value = new_val
                    # print(self.board)
                    need_removals.append(idx)
            except ValueError:
                continue
        for idx in self.block_groups[int(space.row/3)][int(space.col/3)]:
            try:
                if((idx == cur_idx) or (idx in self.perm_innies)):
                    continue
                self.open[idx].outties.remove(val)
                space.affected.append(idx)
                if len(self.open[idx].outties) == 0:
                    return False
                if (len(self.open[idx].outties) == 1):
                    new_val = "".join(self.open[idx].outties)
                    self.innies.append(idx)
                    self.outties.remove(idx)
                    self.board[self.open[idx].row][self.open[idx].col] = new_val
                    self.open[idx].value = new_val
                    # print(self.board)
                    need_removals.append(idx)
            except ValueError:
                continue
        
        for i in range(0, len(need_removals)):
            idx = need_removals[i]
            go = self.remove_possibilities(self.open[idx], self.open[idx].value, idx)
            if not go:
                for k in need_removals:
                    if k in self.innies:
                        self.innies.remove(k)
                        self.outties.append(k)
                for j in range(0,i+1):
                    self.add_possibilities(self.open[need_removals[j]])
                return False

        return True

    def add_possibilities(self, space):
        for i in space.affected:
            self.open[i].outties.append(space.value)
            if(i in self.innies):
                self.outties.append(i)
                self.innies.remove(i)
                self.add_possibilities(self.open[i])
        space.affected.clear()
        return
    
    def perm(self):
        try:
            idx = self.outties[0]
        except:
            return True
        sol_found = False
        self.perm_innies.add(idx)
        self.outties.remove(idx)
        for i in range(0, len(self.open[idx].outties)):
            self.counter += 1
            self.open[idx].value = self.open[idx].outties[i]
            go = self.remove_possibilities(self.open[idx], self.open[idx].value, idx)
            if go:
                sol_found = self.perm_helper(self.outties[0])
                if sol_found:
                    return sol_found
            self.add_possibilities(self.open[idx])
        
        return False

    def perm_helper(self, idx):
        sol_found = False
        self.perm_innies.add(idx)
        self.outties.remove(idx)
        if(len(self.open[idx].outties) == 0):
            return False
        for i in range(0, len(self.open[idx].outties)):
            # self.counter += 1
            # print(self.counter)
            self.open[idx].value = self.open[idx].outties[i]
            go = self.remove_possibilities(self.open[idx], self.open[idx].value, idx)
            if(len(self.outties) == 0):
                print("Solution Found!")
                # for i in self.innies:
                #     self.board[self.open[i].row][self.open[i].col] = self.open[i].value
                # for i in self.board:
                #     print(i)
                return True
            if go:
                sol_found = self.perm_helper(self.outties[0])
                if sol_found:
                    return sol_found
            self.add_possibilities(self.open[idx])
        self.outties.append(idx)
        self.perm_innies.remove(idx)
        return sol_found


            
        
if __name__ == '__main__':
    
    y = [["7","4","8",  "6","3",".",  "1",".","."],
         [".","3",".",  ".",".","5",  ".",".","."],
         [".",".",".",  ".","8",".",  ".","9","."],

         ["8","7","4",  ".",".",".",  ".",".","9"],
         [".",".",".",  ".",".",".",  ".",".","."],
         ["1",".",".",  ".",".",".",  "6","2","7"],

         [".","2",".",  ".","9",".",  ".",".","."],
         [".",".",".",  "5",".",".",  ".","7","."],
         [".",".","6",  ".","7","8",  "2","3","1"]]
    
    z = [[".","8",".",  "3",".",".",  ".",".","9"],
         ["6",".",".",  ".",".",".",  "8",".","."],
         [".",".",".",  ".","6","8",  "1",".","7"],

         [".",".","8",  ".","7",".",  "3","1","."],
         ["4",".",".",  "9",".","6",  ".",".","8"],
         [".","6","7",  ".","3",".",  "5",".","."],

         ["8",".","3",  "4","2",".",  ".",".","."],
         [".",".","2",  ".",".",".",  ".",".","3"],
         ["5",".",".",  ".",".","3",  ".","7","."]]
    x = Solution(z)
    print(x.board)
    w = x.perm()
    x.innies.sort()
    print(x.innies)
    if w:
        for i in x.innies:
            x.board[x.open[i].row][x.open[i].col] = x.open[i].value
        for i in x.perm_innies:
            x.board[x.open[i].row][x.open[i].col] = x.open[i].value
        for i in x.board:
            print(i)
    else:
        print("suck my dick")

    print(len(x.outties))
    # print(x.board)
