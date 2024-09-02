class C4Agent:
    def move(self, symbol, board, last_move):
        depth = 5  # initial depth
        _, col = self.minimax(board, depth, symbol, -float('inf'), float('inf'), True)
        
        # if minimax doesn't return a valid move, find the first available column
        if col is None:
            for idx in range(7):
                if len(board[idx]) < 6:
                    return idx
        return col

    def minimax(self, board, depth, symbol, alpha, beta, maximizing):
        if depth == 0 or self.is_terminal(board):
            return self.evaluate(board, symbol), None

        if maximizing:
            maxEval = -float('inf')
            best_col = None
            for col in range(7):
                if len(board[col]) < 6:
                    new_board = board[:]
                    new_board[col] = new_board[col] + symbol
                    eval_child, _ = self.minimax(new_board, depth-1, symbol, alpha, beta, False)
                    if eval_child > maxEval:
                        maxEval = eval_child
                        best_col = col
                    alpha = max(alpha, eval_child)
                    if beta <= alpha:
                        break
            return maxEval, best_col
        else:
            minEval = float('inf')
            best_col = None
            for col in range(7):
                if len(board[col]) < 6:
                    new_board = board[:]
                    opponent_symbol = 'X' if symbol == 'O' else 'O'
                    new_board[col] = new_board[col] + opponent_symbol
                    eval_child, _ = self.minimax(new_board, depth-1, symbol, alpha, beta, True)
                    if eval_child < minEval:
                        minEval = eval_child
                        best_col = col
                    beta = min(beta, eval_child)
                    if beta <= alpha:
                        break
            return minEval, best_col

    def is_terminal(self, board):
        # Check if the board is full or if there's a win
        if any(len(col) == 6 for col in board):
            return True
        if self.evaluate(board, 'X') == 100 or self.evaluate(board, 'O') == 100:
            return True
        return False

    def evaluate(self, board, symbol):
        opponent_symbol = 'X' if symbol == 'O' else 'O'
        score = 0

        # Check for n-in-a-row in all directions
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for x in range(7):
            for y in range(len(board[x])):
                for dx, dy in directions:
                    score += self.check_direction(board, x, y, dx, dy, symbol) * 10
                    score -= self.check_direction(board, x, y, dx, dy, opponent_symbol)

        # Encourage center control
        for y in range(len(board[3])):
            if board[3][y] == symbol:
                score += 2
            elif board[3][y] == opponent_symbol:
                score -= 2

        return score

    def check_direction(self, board, x, y, dx, dy, symbol):
        count = 0
        for i in range(4):  # Check for 4 in a row
            xi, yi = x + dx*i, y + dy*i
            if 0 <= xi < 7 and 0 <= yi < 6 and (yi < len(board[xi]) and board[xi][yi] == symbol):
                count += 1
            else:
                break

        if count == 4:
            return 100  # Winning sequence
        elif count == 3:
            return 10   # 3 in a row
        elif count == 2:
            return 1    # 2 in a row
        else:
            return 0
