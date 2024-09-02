class C4Agent:

    # Decide the best move for the given player's symbol on the current board
    def move(self, player_symbol, board, last_move):
        search_depth = 5  # We'll look 5 moves ahead
        _, best_column = self.minimax(board, search_depth, player_symbol, -float('inf'), float('inf'), True)
        
        # If we didn't get a best column from minimax, just pick the first available column
        if best_column is None:
            for i in range(7):
                if len(board[i]) < 6:
                    return i
        return best_column

    # Recursive function to determine the best move
    def minimax(self, board, depth, symbol, alpha, beta, maximizing):
        # Base case: if we've searched to the desired depth or if game is over, evaluate the board
        if depth == 0 or self.is_terminal(board):
            return self.evaluate(board, symbol), None

        # Initialize some variables based on whether we're maximizing or minimizing
        if maximizing:
            best_score = -float('inf')
            best_column = None
            for column in range(7):
                if len(board[column]) < 6:
                    new_board = board.copy()
                    new_board[column] = new_board[column] + symbol
                    child_score, _ = self.minimax(new_board, depth-1, symbol, alpha, beta, False)
                    if child_score > best_score:
                        best_score = child_score
                        best_column = column
                    alpha = max(alpha, child_score)
                    if beta <= alpha:
                        break
            return best_score, best_column
        else:
            best_score = float('inf')
            best_column = None
            for column in range(7):
                if len(board[column]) < 6:
                    new_board = board.copy()
                    if symbol == 'O':
                        opponent_symbol = 'X'
                    else:
                        opponent_symbol = 'O'
                    new_board[column] = new_board[column] + opponent_symbol
                    child_score, _ = self.minimax(new_board, depth-1, symbol, alpha, beta, True)
                    if child_score < best_score:
                        best_score = child_score
                        best_column = column
                    beta = min(beta, child_score)
                    if beta <= alpha:
                        break
            return best_score, best_column

    # Check if game is over (either someone won or board is full)
    def is_terminal(self, board):
        if any(len(column) == 6 for column in board):
            return True
        if self.evaluate(board, 'X') == 100 or self.evaluate(board, 'O') == 100:
            return True
        return False

    # Gives a score to the current board, higher is better for the given symbol
    def evaluate(self, board, symbol):
        if symbol == 'O':
            opponent_symbol = 'X'
        else:
            opponent_symbol = 'O'
        
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        # Check each position in the board
        for x in range(7):
            for y in range(len(board[x])):
                # For each position, check in every direction
                for dx, dy in directions:
                    score += self.check_direction(board, x, y, dx, dy, symbol) * 10
                    score -= self.check_direction(board, x, y, dx, dy, opponent_symbol)

        # Give extra points for controlling the center of the board
        for y in range(len(board[3])):
            if board[3][y] == symbol:
                score += 2
            elif board[3][y] == opponent_symbol:
                score -= 2

        return score

    # Check how many symbols in a row exist in a given direction from a starting point
    def check_direction(self, board, x, y, dx, dy, symbol):
        count = 0
        for i in range(4):  # Check for up to 4 in a row
            xi, yi = x + dx*i, y + dy*i
            if 0 <= xi < 7 and 0 <= yi < 6 and (yi < len(board[xi]) and board[xi][yi] == symbol):
                count += 1
            else:
                break

        if count == 4:
            return 100
        elif count == 3:
            return 10
        elif count == 2:
            return 1
        return 0
