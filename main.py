import sys

sys.setrecursionlimit(10_000)


#########################
## 2-SAT Solver Method ##
#########################

bool_list = [True,False]

def new_formula(formula,curr_var,curr_bool):
    # Sort shortest to longest (one-chains, then ...)
    new = []
    for section in formula:
        insert, add = [],True
        for var,boo in section:
            if var != curr_var:
                insert.append((var,boo))
            elif not boo ^ curr_bool:
                add = False
                break
        if add:
            new.append(insert)
    return new

def recurse(formula,var,boolean):
    new_form = new_formula(formula,var,boolean)
    dict1 = satisfying_assignment(new_form)
    if dict1 is not None:
        dict1[var] = boolean
        return dict1
    return None

def satisfying_assignment(formula):
    if len(formula) == 0:
        return {}
    formula.sort(key = len)
    if not formula[0]:
        return None
    curr_var = formula[0][0][0]
    for boo in bool_list:
        result = recurse(formula,curr_var,boo)
        if result is not None: return result
    return None

def cnf(l1):
    return [[((coord),True) for coord in l1]] + [[(l1[c1],False),(l1[c2],False)]
         for c1 in range(len(l1)) for c2 in range(c1+1,len(l1))]
    
def helper(dimension):
    answer = []
    for r in range(dimension):
        for c in range(dimension):
            answer += cnf([(r,c,val) for val in range(1,dimension+1)])
        for val in range(1,dimension+1):
            answer += cnf([(r,c,val) for c in range(dimension)])
            answer += cnf([(c,r,val) for c in range(dimension)])
    return answer,dimension

def subgrid(dimension,square):
    answer = []
    for val in range(1,dimension+1):
        for r in range(0,dimension,square):
            for c in range(0,dimension,square):
                answer += cnf([(s_r,s_c,val) for s_r in 
                    range(r,r+square) for s_c in range(c,c+square)])
    return answer

def already_there(sudoku_board,dimension):
    return [[((r,c,sudoku_board[r][c]),True)] for r in range(dimension)
        for c in range(dimension) if sudoku_board[r][c]]


def sudoku_board_to_sat_formula(sudoku_board):
    answer,dimension = helper(len(sudoku_board))
    answer.extend(subgrid(dimension,int(dimension ** 0.5)))
    answer.extend(already_there(sudoku_board,dimension))
    return answer


def assignments_to_sudoku_board(assignments, n):
    if assignments is None: return assignments
    board = [[0]*n for _ in range(n)]
    for (r,c,val),boo in assignments.items():
        if boo:
            board[r][c] = val
    return board


###########################
## Backtracking Solution ##
###########################

def valid(board,row,col):
    already = set(board[row]) | {board[r][col] for r in range(9)} | {board[r][c]
        for r in range(row//3*3,row//3*3+3) for c in range(col//3*3,col//3*3+3)}
    return [val for val in range(1,10) if val not in already]

      
def Solver(sudoku_board):
    dimension = len(sudoku_board)
    for row in range(dimension):
        for col in range(dimension):
            if sudoku_board[row][col] != 0:
                continue
            for trial in valid(sudoku_board,row,col):
                sudoku_board[row][col] = trial
                result = Solver(sudoku_board)
                if result is not None:
                    return result
            sudoku_board[row][col] = 0
            return None
    return sudoku_board   

def Regrid(grid_values):
    conversion = {"": 0, "1": 1, "2": 2, "3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9}
    return [[conversion[j] for j in grid_values[i*9:i*9+9]] for i in range(9)]

def UnRegrid(grid):
    new_grid = []
    for row in grid:
        new_grid.extend(row)
    return new_grid
