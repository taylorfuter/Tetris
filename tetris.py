# 15-112, Summer 2, Homework 4.2
######################################
# Full name: Taylor Futernick
# Andrew ID: tfuterni
# Section: C
######################################
####################################
# use the run function as-is
####################################
from tkinter import *
import random

def init(data):
    # set board dimensions and margin
    data.rows,data.cols,data.margin =15,10, 20# make board
    data.emptyColor = "blue"
    data.board = [([data.emptyColor]*data.cols) for row in range(data.rows)]
    iPiece = [[True, True, True, True]]
    jPiece = [[True, False, False],[True, True, True]]
    lPiece = [[False, False, True],[True, True, True]]
    oPiece = [[True, True],[True, True]]
    sPiece = [[False, True, True],
        [True, True, False]]
    tPiece = [[False, True, False],
        [True, True, True]]
    zPiece = [[True, True, False],
        [False, True, True]]
    data.tetrisPieces = [iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece]
    data.tetrisPieceColors = ["red", "yellow", "magenta", "pink",
                              "cyan", "green", "orange"]
    data.fallingColor,data.score="",0
    data.fallingPieceCol,data.fallingPieceRow=data.cols//2,0
    data.isGameOver,data.isPaused=False,False
    data.gallingPiece=newFallingPiece(data)

def newFallingPiece(data):
    piece=random.randint(0,len(data.tetrisPieces)-1)
    data.fallingPiece=data.tetrisPieces[piece]
    data.fallingColor=data.tetrisPieceColors[piece]
    #set col to width/2 - width of piece/2
    data.fallingPieceCol=data.cols//2-(len(data.fallingPiece[0])//2)

def isLegalMove(data):
    row,col=data.fallingPieceRow,data.fallingPieceCol
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j]:
                #If not a legal move return false
                if not(0<=i+data.fallingPieceRow<len(data.board) and \
                0<=j+data.fallingPieceCol<len(data.board[0]) and \
                    data.board[i+row][j+col]==data.emptyColor):
                        return False
    return True

def rotatefallingPiece(data):
    fallingPiece,row=data.fallingPiece,data.fallingPieceRow
    col,newBoard=data.fallingPieceCol,[]
    oldCenterRow=row+len(fallingPiece)//2
    oldCenterCol = col + len(fallingPiece[0])//2 #equation from site
    for i in range(len(data.fallingPiece[0])-1,-1,-1): #first row backwards
        newRow=[]
        for j in range(0,len(data.fallingPiece)): #loop through cols
            newRow.append(data.fallingPiece[j][i])
        newBoard.append(newRow)
    data.fallingPiece=newBoard
    data.fallingPieceRow=oldCenterRow-len(newBoard)//2 #equation from site
    data.fallingPieceCol = oldCenterCol-len(newBoard[0])//2 #same as ^
    if isLegalMove(data)==False: #reset the piece if illegal
        data.fallingPiece=fallingPiece
        data.fallingPieceCol=col
        data.fallingPieceRow=row


def moveFallingPiece(data,drow,dcol):
    data.fallingPieceRow+=drow
    data.fallingPieceCol+=dcol
    if not isLegalMove(data): #reset the piece
        data.fallingPieceCol-=dcol
        data.fallingPieceRow-=drow
        return False
    return True

def placeFallingPiece(data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j]: #set color on board
                data.board[i+data.fallingPieceRow]\
                [j+data.fallingPieceCol]=data.fallingColor

# getCellBounds from grid-demo.py
def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if event.keysym=="r": init(data) #reset
    if event.keysym=="p":data.isPaused=not data.isPaused
    if data.isPaused:return #stop movement
    if event.keysym=="Left":
        moveFallingPiece(data,0,-1)
    elif event.keysym=="Right":
        moveFallingPiece(data,0,1)
    elif event.keysym=="Down":
        moveFallingPiece(data,1,0)
    elif event.keysym=="Up":
        rotatefallingPiece(data)

def isFullRow(data,r):
    for i in range(len(data.board[r])):
        if data.board[r][i]==data.emptyColor:
            return False
    return True

def removeFullRows(data):
    numRem=0
    newBoard=[[data.emptyColor]*len(data.board[0])
    for i in range(len(data.board))] #set empty board
    newRow=len(data.board)-1 #last row
    for oldRow in range(len(data.board)-1,-1,-1): #rows from bottom
        if isFullRow(data,oldRow)==False:
            newBoard[newRow]=data.board[oldRow] #copy if not full
            newRow-=1
        else:numRem+=1 #remove the row
    data.score+=(numRem**2) #add square of num removed
    data.board=newBoard

def timerFired(data):
    if data.isPaused:return #do nothing
    if moveFallingPiece(data,1,0)==False: #can't go down
        placeFallingPiece(data)
        data.fallingPieceRow=0 #next piece starts to fall from top
        newFallingPiece(data) #get new piece
        removeFullRows(data) #see if row is full
        if isLegalMove(data)==False: #next piece fails immediately
            data.isGameOver=True


def drawGame(canvas, data):
    if data.isGameOver: #display game over message
        canvas.create_text(data.width/2,data.height/2,
                        font=("Times", "24", "bold"),text="GAME OVER")
        canvas.create_text(data.width/2,data.height/1.5,
            font=("Times", "14", "bold"),text="Score: "+str(data.score))
        return
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    drawBoard(canvas, data)
    drawFallingPiece(canvas,data)

def drawFallingPiece(canvas,data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j]:
                drawCell(canvas,data,i+data.fallingPieceRow,
                         j+data.fallingPieceCol,data.fallingColor)

def drawBoard(canvas, data):
    # draw grid of cells
    scoreY=10
    #display score
    canvas.create_text(data.width/2,scoreY,text=str(data.score))
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col,data.board[row][col])


def drawCell(canvas, data, row, col,color):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m = 1 # cell outline margin
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=color)

def redrawAll(canvas, data):
    drawGame(canvas, data)

####################################
# use the run function as-is
####################################

def run1(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 300 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# run(300, 300)

####################################
# playTetris() [calls run()]
####################################

def run():
    rows = 19
    cols = 10
    margin = 20 # margin around grid
    cellSize = 20 # width and height of each cell
    width = 2*margin + cols*cellSize
    height = 2*margin + rows*cellSize
    run1(width, height)

run()