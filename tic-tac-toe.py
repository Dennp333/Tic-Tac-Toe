import copy
import random




## A Board is a [[Str, Str, Str], [Str, Str, Str], [Str, Str, Str]]


gameBoard = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
coordDict = {"a":0, "b":1, "c":2, "1":2, "2":1, "3":0}
rowsIndexDict = {2:"1", 1:"2", 0:"3"}
colsIndexDict = {0:"a", 1:"b", 2:"c"}


## Displays board
def showBoard(board):
    rowBreak = "-"*17
    showRow(board[0])
    print(rowBreak)
    showRow(board[1])
    print(rowBreak)
    showRow(board[2])
    

## Displays row
def showRow(row):
    margin = (" "*5 + "|")*2 + " "*5
    print(margin)
    print(f'  {row[0]}  |  {row[1]}  |  {row[2]}')
    print(margin)


## Given letter, determines the opposite letter
## Str -> Str
def switchLetter(letter):
    if letter == "X":
        return "O"
    else:
        return "X"


## Takes a user's input and determines the letter they've chosen
## Str -> Str
def getPlayerLetter():
    playerLetter = input("Choose X or O")
    if playerLetter == "X" or playerLetter == "O":
        return playerLetter
    else:
        print("Invalid input")
        return getPlayerLetter()


## Takes a user's input and determines their move
## Str -> Str
def getPlayerMove():
    playerMove = input("What will you play?")
    if playerMove in legalMoves(gameBoard):
        return playerMove
    else:
        print("Invalid input")
        return getPlayerMove()


## Produces the board with letter placed at coords on currentBoard
## Board, Str, Str -> Board
def move(currentBoard, letter, coords):
    col = coords[0]
    row = coords[1]
    newBoard = copy.deepcopy(currentBoard)
    newBoard[coordDict[row]][coordDict[col]] = letter
    return newBoard


## Determines if the game on board is over, and assigns a score to the cpu
## Board, Str -> (anyof Int Bool)
def gameOver(board, cpu):
    player = switchLetter(cpu)
    if win(board, cpu):
        return 10
    elif win(board, player):
        return -10
    elif full(board):
        return 0
    else:
        return False


## Determines if letter has won the game on board
## Board, Str -> Bool
def win(board, letter):
    for i in range (3):
        if (board[i][0] == letter and board[i][1] == letter and board[i][2] == letter):
            return True
        elif (board[0][i] == letter and board[1][i] == letter and board[2][i] == letter):
            return True
    if (board[0][0] == letter and board[1][1] == letter and board[2][2] == letter):
        return True
    elif (board[0][2] == letter and board[1][1] == letter and board[2][0] == letter):
        return True
    else:
        return False


## Determines if board is full
## Board -> Bool
def full(board):
    for i in range (3):
        if " " in board[i]:
            return False
    return True


## Produces a list of all possible moves on board
## Board -> [listof Str]
def legalMoves(board):
    moves = []
    for i in range (3):
        for k in range (3):
            if board[i][k] == " ":
                moves.append(colsIndexDict[k] + rowsIndexDict [i])
    return moves


## Finds the index of the best option in values
## [listof [int, int]] -> [Int, Int]
def chooseMax(values):
    scores = []
    depths = []
    maxScorers = []
    for i in range(len(values)):
        scores.append(values[i][0])
        depths.append(values[i][1])
    maxScore = max(scores)
    for i in range(len(scores)):
        if scores[i] == maxScore:
            maxScorers.append(depths[i])
    return [maxScore, min(maxScorers)]


## Finds the index of the worst option in values
## [listof [int, int]] -> [Int, Int]
def chooseMin(values):
    scores = []
    depths = []
    minScorers = []
    for i in range(len(values)):
        scores.append(values[i][0])
        depths.append(values[i][1])
    minScore = min(scores)
    for i in range(len(scores)):
        if scores[i] == minScore:
            minScorers.append(depths[i])
    return [minScore, max(minScorers)]


## Finds the move that gives the maximum end value for letter, assuming that the opponent will move to get the minimum value
## Board, Str -> [Str, Int, Int]
def maximize(currentBoard, letter):
    allMoves = legalMoves(currentBoard)
    values = []
    otherLetter = switchLetter(letter)
    for i in range(len(allMoves)):
        newBoard = move(currentBoard, letter, allMoves[i])
        gameState = gameOver(newBoard, letter)
        if gameState is False:
            minimum = minimize(newBoard, letter)
            values.append([minimum[1], minimum[2]+1])
        else:
            values.append([gameState, 0])
    maxIndex = values.index(chooseMax(values))
    return [allMoves[maxIndex], values[maxIndex][0], values[maxIndex][1]]


## Finds the minimum end value for letter, assuming that the opponent will move to get the maximum value
## Board, Str -> [Str, Int, Int]
def minimize(currentBoard, letter):
    allMoves = legalMoves(currentBoard)
    values = []
    otherLetter = switchLetter(letter)
    for i in range(len(allMoves)):
        newBoard = move(currentBoard, otherLetter, allMoves[i])
        gameState = gameOver(newBoard, letter)
        if gameState is False:
            maximum = maximize(newBoard, letter)
            values.append([maximum[1], maximum[2]+1])
        else:
            values.append([gameState, 0])
    minIndex = values.index(chooseMin(values))
    return [allMoves[minIndex], values[minIndex][0], values[minIndex][1]]


## Main
print('Welcome to Tic-Tac-Toe. To input coordinates, use the chess coordinate system.')
player = getPlayerLetter()
cpu = switchLetter(player)


if player == "X":
    showBoard(gameBoard)
    playerMove = getPlayerMove()
    gameBoard = move(gameBoard, player, playerMove)
    gameBoard = move(gameBoard, cpu, maximize(gameBoard, cpu)[0])
else:
    n = random.randint(1,8)
    if n == 1:
        cpuMove = "a3"
    elif n == 2:
        cpuMove = "c3"
    elif n == 3:
        cpuMove = "a1"
    elif n == 4:
        cpuMove = "c1"
    else:
        cpuMove = "b2"
    gameBoard = move(gameBoard, cpu, cpuMove)


while gameOver(gameBoard, player) is False:
    showBoard(gameBoard)
    playerMove = getPlayerMove()
    gameBoard = move(gameBoard, player, playerMove)
    if gameOver(gameBoard, player) is False:
        gameBoard = move(gameBoard, cpu, maximize(gameBoard, cpu)[0])


showBoard(gameBoard)
if gameOver(gameBoard, player) == 0:
    print('Tie game')
else:
    print('Hah! Loser!')
