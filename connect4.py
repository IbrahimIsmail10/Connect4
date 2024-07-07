import random
import copy

list1=[]
list2 =[]
#define min and max for alpha and beta
MAX = float('-inf') #for alpha = -infinity
MIN = float('inf') #for beta  = infinity 
#define the two players
AI_Agent = "R"
Computer= "Y"
EMPTY = 0
def evaluate_window(window, piece):
    # print(piece)    
    score = 0
    opp_piece = Computer  # Assuming "Computer" is a string variable
    if piece == Computer:
        opp_piece = AI_Agent  # Assuming "AI_Agent" is a string variable
    
    if window.count(piece) == 4:
        return 10000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(EMPTY) == 1 and window.count(piece) == 3:
        score += 5    
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    elif window.count(piece) == 2 and window.count(EMPTY) == 1 and window.count(piece) == 1:
        score += 5
    elif window.count(EMPTY) == 2 and window.count(piece) == 2:
        score += 2
    elif window.count(piece) == 1 and window.count(EMPTY) == 1 and window.count(piece) == 2:
        score += 5     

    # Additional conditions to prevent opp_piece from winning
    if window.count(opp_piece) == 4:
        return -10000
    elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 5
    # elif window.count(EMPTY) == 1 and window.count(opp_piece) == 3:
    #     score -= 5
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 2
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 1 and window.count(opp_piece) == 1:
        score -= 5
    elif window.count(opp_piece) == 1 and window.count(EMPTY) == 1 and window.count(opp_piece) == 2:
        score -= 5
    return score



def score_state(board, piece):
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


#print board like connect 4 game
def print_board(board):
    for row in range(6):
        print("| ", end="")
        for col in range(7):
            print(board[row][col], "| ", end="")
        print()
    print("-----------------------------")
#define board of 2 dimensions with 6 rows and 7 colums to create connect 4 game   
board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
#define function that calc score of one of players 
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
     if len(moves) == 0 or winning_move(board,AI_Agent) or winning_move(board,Computer):
          return True
     else:
          return False
def drop_piece(board ,row,col,player):
     board[row][col] = player     
#function get all possible moves that you can do
def Move_Options(board):
    avalibale_move =[]
    for j in range (7):
        if board[0][j] == 0:
            for i in reversed(range(6)):
                if board[i][j] == 0:
                    avalibale_move.append((i,j))
                    break
    return avalibale_move    
#implement minmax algorithm with alpha&beta purning 
def MinMax_Algorithm(board , depth , maxstate,alpha,beta,player):
    opp_piece = Computer
    if player == Computer: opp_piece = AI_Agent
    moves = Move_Options(board)
    is_terminal = is_terminal_game(board)
    if (depth ==0 or is_terminal):
        if(is_terminal):
            if (winning_move(board,player)):
               return (None,100000)
            elif(winning_move(board,Computer)):
                 return (None,-100000)
            else:
                 return (None,0)
        else: 
            score =score_state(board,player)
            return (None,score)   

    #if maxstate is true that means we are in max mode
    if (maxstate):
        max_val = MAX
        cur = random.choice(moves)
        for current_move in moves:
            new_board = copy.deepcopy(board)
            #moves is represent as pair of 2 numbers(i,j), i for rows and j for columns
            # move[0] represent first number in pair (row number)
            # move[1] represent second number in pair (culumn number)
            drop_piece(new_board,current_move[0],current_move[1] ,player)
            #call the algorithm recursivally with depth-1 and in other mode(that mean if we in max level we call min level and so on..)
            value = MinMax_Algorithm(new_board,depth-1,False,alpha,beta,player)[1]
            # max_val = max(max_val,value)
            if value > max_val:
                max_val = value
                cur = current_move
            alpha = max(value,alpha)
            if alpha >= beta:
                break
        return cur,max_val
    #if maxstate is false we are in min mode
    else:
        min_val = MIN
        cur2 = random.choice(moves)
        for current_move in moves:
             new_board =copy.deepcopy(board)
             drop_piece(new_board,current_move[0],current_move[1] ,opp_piece)
             value = MinMax_Algorithm(new_board,depth-1,True,alpha,beta,player)[1]
            #  min_val = min(min_val,value)
             if value < min_val:
                 min_val = value
                 cur2 = current_move
             beta = min(beta,value)
             if alpha >= beta:
                break
        return cur2,min_val
    
#define the simple version of min max algorithm
def Simple_MinMax_Algorithm(board ,depth , maxstate):
    moves = Move_Options(board)
    is_terminal = is_terminal_game(board)
    if (depth ==0 or is_terminal):
        if(is_terminal):
            if (winning_move(board,AI_Agent)):
               return (None,100000)
            elif(winning_move(board,Computer)):
                 return (None,-100000)
            else:
                 return (None,0)
        else: 
            return (None,score_state(board,AI_Agent))
    #if maxstate is true that means we are in max mode
    if (maxstate):
        max_val = MAX
        cur =random.choice(moves)
        for current_move in moves:
            new_board = copy.deepcopy(board)
            #moves is represent as pair of 2 numbers(i,j), i for rows and j for columns
            # move[0] represent first number in pair (row number)
            # move[1] represent second number in pair (culumn number)
            drop_piece(new_board,current_move[0],current_move[1] ,AI_Agent)
            #call the algorithm recursivally with depth-1 and in other mode(that mean if we in max level we call min level and so on..)
            value = Simple_MinMax_Algorithm(new_board,depth-1,False)[1]
            if value > max_val:
                 min_val = value
                 cur = current_move
        return cur,max_val     
    #if maxstate is false we are in min mode
    else:
        min_val = MIN
        cur2 =random.choice(moves)
        for current_move in moves:
             new_board =copy.deepcopy(board)
             drop_piece(new_board,current_move[0],current_move[1] ,Computer)
             value = Simple_MinMax_Algorithm(new_board,depth-1,True)[1]
             if value < min_val:
                 min_val = value
                 cur2 = current_move
        return cur2,min_val
    

#define function that select best move to take
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

#function of the game 
def Game (board,depth,type):
    if type == "simple":
        print("Using Simple Algorithm ")  
    else:
        print("Using Alpha-Beta Algorithm ")  
    score1 = 0
    score2 = 0
    while True:
        moves = Move_Options(board)
        if(is_terminal_game(board)):
            score1 = 0
            score2 = 0
            break
        #first AI Agent play using a minmax algorithm 
        make_move(board , depth,AI_Agent,type)
        print_board(board)
        score1 = winning_move(board,AI_Agent)
        #after every move agent do it in board we check if it win or not 
        if score1:
            break
        #second player is computer, it play randomly not using any algorithm 
        #check if the board is full and no one is win so we get out of loop and the result is draw
        
        # index = random.randint(0,len(moves)-1)
        # list2.append(moves[index])
        # make_move(board,depth,Computer,type)
        # print("Computer select randomly: ",moves[index])
        # drop_piece(board,moves[index][0],moves[index][1],Computer)
        make_move(board,depth,Computer,type)
        print_board(board)
        score2 = winning_move(board,Computer)
        #after every move computer do it in board we check if it win or not 
        if score2:
            break
    #check which one is win in game or game ended draw    
    if(winning_move(board,AI_Agent)):
        print("score1= ",Get_score(board,AI_Agent))
        print("AI Agent win")
    elif(winning_move(board,Computer)):
        print("score2= ",Get_score(board,Computer))
        print("Computer win")
    else:
        print("DRAW")


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
        list2.append(moves[index])
        # print("Computer select randomly: ",moves[index])
        board[moves[index][0]][moves[index][1]] = Computer
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
        board[moves[index][0]][moves[index][1]] = Computer
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

type = input("Enter Which Algorithm You Want To Use? ")
Game(board,5,type)
print_board(board)
print(Move_Options(board))

