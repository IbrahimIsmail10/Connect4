import random
import math 
import copy
MAX = -math.inf
MIN = math.inf
board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
AI_Agent = "R"
Computer = "Y"
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4
EMPTY = 0


def print_board(board):
    for row in range(6):
        print("| ", end="")
        for col in range(7):
            print(board[row][col], "| ", end="")
        print()
    print("-----------------------------")
def drop_piece(board ,row,col,player):
     board[row][col] = player    
def Get_score(board,player):
    score = 0
    #check if player wins in the digonal
    for i in range(3):
        for j in range(4):
            #its list of 4 element which i loop in board to get if there 4 element in one digonal
            # we loop with k time becouse if there 4 connected that mean you win  
            line1 = [board[i+k][j+k] for k in range(4)] 
            if line1 == [player,player,player,player]:
                score +=100
                return score
    for i in range(3, 6):
        for j in range(4):
            line1 = [board[i-k][j+k] for k in range(4)] 
            if line1 == [player,player,player,player]:
                score +=100
                return score      


    #check if the player win horizontal by connect 4 in one row 
    for i in range(6): #we have 6 rows
        for j in range(4):
            #list that store 4 element that get out from condation
            line2 = [board[i][j+k] for k in range(4)]
            if line2 == [player,player,player,player]:  
                score+=100  
                return score


    #check if the player win vertical by connect 4 in one column 
    for j in range(7): #we have 6 rows
        for i in range(3):
            #list that store 4 element that get out from condation
            line3 = [board[i+k][j] for k in range(4)]
            if line3 == [player,player,player,player]:  
                score+=100  
                return score

    return score  
def winning_move(board,player):
     value = Get_score(board,player)
     if(value == 100):
          return True
     else:
          return False
def is_terminal_game(board):
     moves = Move_Options(board)
     if len(moves) == 0 or winning_move(board,"AI_Agent") or winning_move(board,"Computer"):
          return True
     else:
          return False
def Move_Options(board):
    avalibale_move =[]
    for j in range (7):
        if board[0][j] == 0:
            for i in reversed(range(6)):
                if board[i][j] == 0:
                    avalibale_move.append((i,j))
                    break
    return avalibale_move  
def evaluate_window(window, piece):
	score = 0
	opp_piece = Computer
	if piece == Computer:
		opp_piece = AI_Agent

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
		score -=2   

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = Move_Options(board)
    is_terminal = is_terminal_game(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_Agent):
                return (None, 100000000000000)
            elif winning_move(board, Computer):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_Agent))
    if maximizingPlayer:
        value = MAX
        column = random.choice(valid_locations)
        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, col[0], col[1], AI_Agent)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col         
            # value = max(value,new_score)            
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column,value

    else: # Minimizing player
        value = MIN
        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            drop_piece(b_copy, col[0],col[1] , Computer)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column,value
def make_move(board,depth,player,type):
    moves = Move_Options(board)
    if(len(moves)== 0):
        return
    best_move = random.choice(moves)
    best_score = MAX
    for current_move in moves:
        print("in")
        new_board = copy.deepcopy(board)
        drop_piece(new_board,current_move[0],current_move[1],player)
        # if type == "simple":
        #     value = Simple_MinMax_Algorithm(new_board,depth,True)
        # else:
            # value = MinMax_Algorithm(new_board,depth,True,MAX,MIN)
        value = minimax(new_board,depth,True,MAX,MIN)[1]
        print(value)

        # print (current_move,"          ",value)    
        if value > best_score :
            best_score = value
            best_move = current_move
    print("AI Agent Select Best Move = ",best_move,"  ",best_score)        
    drop_piece(board,best_move[0],best_move[1],player)
def Game_manual (board,depth,type):
    if type == "simple":
        print("Using Simple Algorithm ")  
    else:
        print("Using Alpha-Beta Algorithm ")  
    score1 = 0
    score2 = 0
    while True:
        #first AI Agent play using a minmax algorithm 
        make_move(board , depth,AI_Agent,type)
        print_board(board)
        score1 = Get_score(board,AI_Agent)
        #after every move agent do it in board we check if it win or not 
        if score1 == 100:
            break
        #second player is computer, it play randomly not using any algorithm 
        moves = Move_Options(board)
        #check if the board is full and no one is win so we get out of loop and the result is draw
        if(len(moves)==0):
            break
        print(moves)
        index = int (input("enter the place: "))
        # print("Computer select randomly: ",moves[index])
        drop_piece(board,moves[index][0],moves[index][1],Computer)
        # board[moves[index][0]][moves[index][1]] = Computer
        print_board(board)
        score2 = Get_score(board,Computer)
        #after every move computer do it in board we check if it win or not 
        if score2 == 100 :
            break
    #check which one is win in game or game ended draw    
    if(score1 > 0 and score2 == 0):
        print("score1= ",score1)
        print("AI Agent win")
    elif(score2 > 0 and score1 == 0):
        print("score2= ",score2)
        print("Human win")
    else:
        print(score1,"   ",score2)
        print("DRAW")
# valid_locations = Move_Options(board)
# column = random.choice(valid_locations)
# print(column)
# print(tmp,"       ",tmp[0][0],"       ",tmp[0][1],"     ",tmp[1])

Game_manual(board,5,"alpha")

def MOVE_AI_VS_COMPUTER(board,depth,player,type):
    moves = Move_Options(board)
    if(len(moves)== 0):
        return
    best_move = None
    best_score = MAX
    if type == "simple":
        best_move,best_score = Simple_MinMax_Algorithm(board,depth,True)
    else:
        best_move,best_score = MinMax_Algorithm(board,depth,True,MAX,MIN,player)
    print("AI Agent Select Best Move = ",best_move," score =",best_score)        
    drop_piece(board,best_move[0],best_move[1],player)


def make_move(board,depth,player,type):
    moves = Move_Options(board)
    if(len(moves)== 0):
        return
    best_move = None
    best_score = MAX
    if type == "simple":
        best_move,best_score = Simple_MinMax_Algorithm(board,depth,True)
    else:
        best_move,best_score = MinMax_Algorithm(board,depth,True,MAX,MIN,player)
    print("AI Agent Select Best Move = ",best_move," score =",best_score)        
    drop_piece(board,best_move[0],best_move[1],player)
    list1.append(best_move)
    return best_move[1]