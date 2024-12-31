# ارزیابی وضعیت بازی
def evaluate(board):
    # بررسی ردیف‌ها
    for row in board:
        if row == ['X', 'X', 'X']:
            return 1
        elif row == ['O', 'O', 'O']:
            return -1
    # بررسی ستون‌ها
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == 'X':
            return 1
        elif board[0][col] == board[1][col] == board[2][col] == 'O':
            return -1
    # بررسی قطرها
    if board[0][0] == board[1][1] == board[2][2] == 'X' or board[0][2] == board[1][1] == board[2][0] == 'X':
        return 1
    elif board[0][0] == board[1][1] == board[2][2] == 'O' or board[0][2] == board[1][1] == board[2][0] == 'O':
        return -1
    return 0

# تابع Minimax
def minimax(board, depth, isMax):
    score = evaluate(board)
    if score == 1:
        return score
    if score == -1:
        return score
    if not any('_' in row for row in board):
        return 0  # بازی مساوی
    
    if isMax:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'X'
                    best = max(best, minimax(board, depth + 1, not isMax))
                    board[i][j] = '_'
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'O'
                    best = min(best, minimax(board, depth + 1, not isMax))
                    board[i][j] = '_'
        return best

# یافتن بهترین حرکت
def find_best_move(board):
    best_val = -1000
    best_move = (-1, -1)
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = 'X'
                move_val = minimax(board, 0, False)
                board[i][j] = '_'
                
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
                    
    return best_move

# تست با وضعیت فعلی بازی
board = [
    ['X', 'O', 'X'],
    ['O', 'O', 'O'],
    ['_', '_', 'O']
]

best_move = find_best_move(board)
print(f"The best Move for (X) is : {best_move}")
