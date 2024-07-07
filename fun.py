board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 1, 0, 0, 0],
            [2, 0, 0, 1, 0, 0, 0],
            [2, 0, 1, 1, 1, 0, 0],
        ]
AI_PIECE = 1
PLAYER_PIECE = 2
EMPTY = 0
def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0
	ROW_COUNT = 6
	COLUMN_COUNT = 7
	WINDOW_LENGTH = 4

	# Score center column
	center_count = sum(row[COLUMN_COUNT // 2] == piece for row in board)
	score += center_count * 3

	# Score horizontal
	for row in board:
		for col in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
			window = row[col:col + WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	# Score vertical
	for col in range(COLUMN_COUNT):
		for row in range(ROW_COUNT - WINDOW_LENGTH + 1):
			window = [board[row + i][col] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	# Score positive sloped diagonal
	for row in range(ROW_COUNT - WINDOW_LENGTH + 1):
		for col in range(COLUMN_COUNT - WINDOW_LENGTH + 1):
			window = [board[row + i][col + i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	# Score negative sloped diagonal
	for row in range(ROW_COUNT - WINDOW_LENGTH + 1):
		for col in range(WINDOW_LENGTH - 1, COLUMN_COUNT):
			window = [board[row + i][col - i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score


# def check_connect(board, piece):
#     ROW_COUNT = 6
#     COLUMN_COUNT = 7
#     WINNING_COUNT = 4
    
#     Hscore =0
#     Vscore =0
#     Dscore =0
#     NDscore =0

#     # Check horizontal
#     for row in range(ROW_COUNT):
#         for col in range(COLUMN_COUNT - WINNING_COUNT + 1):
#             if all(board[row][col + i] == piece for i in range(WINNING_COUNT)):
#                 Hscore+=1

#     # Check vertical
#     for col in range(COLUMN_COUNT):
#         for row in range(ROW_COUNT - WINNING_COUNT + 1):
#             if all(board[row + i][col] == piece for i in range(WINNING_COUNT)):
#                 Vscore= WINNING_COUNT

#     # Check positive sloped diagonal
#     for row in range(ROW_COUNT - WINNING_COUNT + 1):
#         for col in range(COLUMN_COUNT - WINNING_COUNT + 1):
#             if all(board[row + i][col + i] == piece for i in range(WINNING_COUNT)):
#                 Dscore= WINNING_COUNT

#     # Check negative sloped diagonal
#     for row in range(ROW_COUNT - WINNING_COUNT + 1):
#         for col in range(WINNING_COUNT - 1, COLUMN_COUNT):
#             if all(board[row + i][col - i] == piece for i in range(WINNING_COUNT)):
#                 NDscore= WINNING_COUNT - 1  # Return 3 for 4 connections, 2 for 3 connections

#     return max(Hscore,Vscore,Dscore,NDscore)  # Return 0 for no connections
print(score_position(board,1))