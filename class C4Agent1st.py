class C4Agent:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.depth_limit = 7

    def move(self, symbol, board, last_move):
        # Check for defensive moves first
        for col in range(self.cols):
            if len(board[col]) < 6:
                temp_board = board.copy()
                temp_board[col] += symbol
                if self.has_winning_position(temp_board, symbol):
                    return col
        
        # Check for offensive moves
        opponent_symbol = 'O' if symbol == 'X' else 'X'
        for col in range(self.cols):
            if len(board[col]) < 6:
                temp_board = board.copy()
                temp_board[col] += opponent_symbol
                if self.has_winning_position(temp_board, opponent_symbol):
                    return col

        _, move = self.minimax(board, self.depth_limit, True, symbol, -float('inf'), float('inf'))
        return move

    def minimax(self, board, depth, maximizing, symbol, alpha, beta):
        if depth == 0 or self.is_terminal_node(board):
            return self.evaluate_board(board, symbol), None
        
        valid_moves = [col for col, val in enumerate(board) if len(val) < 6]
        
        if maximizing:
            maxEval = -float('inf')
            bestMove = valid_moves[0]
            for col in valid_moves:
                board_copy = board.copy()
                board_copy[col] += symbol
                eval_current, _ = self.minimax(board_copy, depth - 1, False, symbol, alpha, beta)
                if eval_current > maxEval:
                    maxEval = eval_current
                    bestMove = col
                alpha = max(alpha, eval_current)
                if beta <= alpha:
                    break
            return maxEval, bestMove
        else:
            minEval = float('inf')
            bestMove = valid_moves[0]
            opponent_symbol = 'O' if symbol == 'X' else 'X'
            for col in valid_moves:
                board_copy = board.copy()
                board_copy[col] += opponent_symbol
                eval_current, _ = self.minimax(board_copy, depth - 1, True, symbol, alpha, beta)
                if eval_current < minEval:
                    minEval = eval_current
                    bestMove = col
                beta = min(beta, eval_current)
                if beta <= alpha:
                    break
            return minEval, bestMove

    def evaluate_board(self, board, symbol):
        score = 0
        opponent = 'O' if symbol == 'X' else 'X'

        # Add central column control
        center_array = [board[3][i] for i in range(len(board[3]))]
        center_count = center_array.count(symbol)
        score += center_count * 3

        for row in range(self.rows):
            for col in range(self.cols - 3):
                window = [board[c][row] for c in range(col, col + 4) if row < len(board[c])]
                if len(window) == 4:
                    score += self.evaluate_window(window, symbol)

        for col in range(self.cols):
            for row in range(len(board[col]) - 3):
                window = board[col][row:row + 4]
                score += self.evaluate_window(window, symbol)

        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                window = [board[col + i][row + i] for i in range(4) if row + i < len(board[col + i])]
                score += self.evaluate_window(window, symbol)

                window = [board[col + i][row + 3 - i] for i in range(4) if row + 3 - i < len(board[col + i])]
                score += self.evaluate_window(window, symbol)

        return score

    def evaluate_window(self, window, symbol):
        score = 0
        opponent = 'O' if symbol == 'X' else 'X'
        if window.count(symbol) == 4:
            score += 100
        elif window.count(symbol) == 3 and window.count('.') == 1:
            score += 10
        elif window.count(symbol) == 2 and window.count('.') == 2:
            score += 5

        if window.count(opponent) == 3 and window.count('.') == 1:
            score -= 80

        return score

    def is_terminal_node(self, board):
        return self.has_winning_position(board, 'X') or self.has_winning_position(board, 'O') or all(len(col) == 6 for col in board)

    def has_winning_position(self, board, symbol):
        for col in range(self.cols):
            for row in range(len(board[col])):
                if self.check_win_from_position(board, row, col, symbol):
                    return True
        return False

    def check_win_from_position(self, board, row, col, symbol):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 0
            for i in range(4):
                r, c = row + dr * i, col + dc * i
                if 0 <= c < self.cols and 0 <= r < len(board[c]) and board[c][r] == symbol:
                    count += 1
                else:
                    break
            if count == 4:
                return True
        return False
