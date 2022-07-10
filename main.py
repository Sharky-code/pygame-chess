#I would want to make 2 modes for the chess placing: click to show location, click available destination to go there, and hold and release onto destination
#Change of storage: now how it works it that it stores the chess location instead of storing the entier chess board

#accidentally git pulled it oh no

import pygame
import os

width, height = 900, 750
backgroundColor = (255,255,255)
continueGame = True

#using this system, it is easier to decide where the piece can go imo
#also pawn objects can be easily shown if they have been moved or not (with the last boolean)
#castling is also much easier with this method
#i used to make a whole chess table and i had to rewrite the entire thing . - .
chessStorage = [
        ['blackrook', [0, 0], True],
        ['blackknight', [1, 0], True],
        ['blackbishop', [2, 0], True],
        ['blackqueen', [3, 0], True],
        ['blackking', [4, 0], True],
        ['blackbishop', [5, 0], True],
        ['blackknight', [6, 0], True],
        ['blackrook', [7, 0], True],

        ['blackpawn', [0, 1], True, True],
        ['blackpawn', [1, 1], True, True],
        ['blackpawn', [2, 1], True, True],
        ['blackpawn', [3, 1], True, True],
        ['blackpawn', [4, 1], True, True],
        ['blackpawn', [5, 1], True, True],
        ['blackpawn', [6, 1], True, True],
        ['blackpawn', [7, 1], True, True],

        ['whiterook', [0, 7], True],
        ['whiteknight', [1, 7], True],
        ['whitebishop', [2, 7], True],
        ['whitequeen', [3, 7], True],
        ['whiteking', [4, 7], True],
        ['whitebishop', [5, 7], True],
        ['whiteknight', [6, 7], True],
        ['whiterook', [7, 7], True],

        ['whitepawn', [0, 6], True, True],
        ['whitepawn', [1, 6], True, True],
        ['whitepawn', [2, 6], True, True],
        ['whitepawn', [3, 6], True, True],
        ['whitepawn', [4, 6], True, True],
        ['whitepawn', [5, 6], True, True],
        ['whitepawn', [6, 6], True, True],
        ['whitepawn', [7, 6], True, True],
        ]
pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Chess')
gameFont = pygame.font.SysFont('Arial', 30)

"""
REWRITE GOAL:
    - WHEN PRESS ON THE ITEM, THE ITEM IS STILL THERE, BUT NOT DISPLAYED (MAKE A NODISPLAY TAG) (DONE)
    - WHEN RELEASE ON LEGAL SPOT, THE ITEM WILL CHANGE POSITION, AND THE DISPLAY TAG WILL BE TRUE 
    - MAKE IT READABLE YOU GOOF (MOSTLY DONE)
    - ADD SELF.PRESSED SO THE CLICK MODE WORKS AND IT WON'T MESS UP MUCH (DO THIS NOW)
"""

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Task = MAKE THE SELF.PRESSED SO AFTER YOU FINISH USING TWO CLICK MODE YOU WON'T BE IN TWO CLICK MODE YET AGAIN.
# ALSO MAKE IT SO THAT IF YOU PRESS THE STUFF AGAIN AFTER TWO CLICK MODE YOU WILL NOT MOVE AND NOTHING WILL CHANGE (TURN WILL NOT BE CHANGED)

class MovePieces:
    def __init__(self):
        self.threatened = None
        self.turn = 'white'
    
        # drag and drop logic
        self.dragModeCoord = None
        self.dragModeName = None
        self.dragModeInfo = None
        self.pressed = False

        # double click logic
        self.samePieceClick = None

        #legal chess piece move logic
        self.selectedChessPieceLegalMoves = None

    def drawTable(self):
        global chessStorage

        chessSideIcon = [['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],[str(i+1) for i in range(8)]]

        for x in range(8):
            screen.blit(gameFont.render(chessSideIcon[0][x],False,(0,0,0)),(80 + x*80, 10))
            screen.blit(gameFont.render(chessSideIcon[1][x],False,(0,0,0)),(10, 80 + x*80))

            for y in range(8):
                #draw the table (makes it yellow if its special) (ill change the special conditions later)
                pygame.draw.rect(screen, (161, 152, 77) if self.samePieceClick == [x, y] else (207, 106, 66) if self.selectedChessPieceLegalMoves != None and [x, y] in self.selectedChessPieceLegalMoves else ((153, 94, 64) if (x * 3 + y) % 2 == 1 else (232, 215, 167)), pygame.Rect(50 + x*80, 50 + y*80, 80, 80)) #chessStorage[[z[1] for z in chessStorage].index([x, y])][0]
                # if self.selectedChessPieceLegalMoves != None and [x, y] in self.selectedChessPieceLegalMoves else (166, 129, 88)

        for x in chessStorage:
            #draws the margins
            if x[2]:
                screen.blit(pygame.transform.scale(pygame.image.load(os.path.join('icons', f'{x[0]}.png')), (70, 70)),(50 + 5 + x[1][0] * 80, 50 + 5 + x[1][1] * 80))
          
   
    def selectPiece(self):
        '''
        logic:
        if you press and hold on an object, the object become invisible. A new object will follow your mouse but that is only
        for display. Then when you release, the object will change position, and no longer be invisible. If there is a object
        already in the spot, it will delete it. If you click and hold on an empty space you will not be able to select any p-
        iece when if you hover on them. This is partly because it makes the interface neater and makes the two click mode ea-
        sier to make.
        If you press and hold on an object, and release it on the same spot, two click mode will be activated. Click on anot-
        her spot to choose where it will go. Again, it will replace the piece that is already in the position. You'll have to
        release your mouse to select on something again.
        '''
        xe = int((pygame.mouse.get_pos()[0] - 50 - (pygame.mouse.get_pos()[0]-50)%80) / 80)
        x = xe if xe in range(8) else None

        ye = int((pygame.mouse.get_pos()[1] - 50 - (pygame.mouse.get_pos()[1]-50)%80) / 80)
        y = ye if ye in range(8) else None

        #for debugging
        screen.blit(gameFont.render(f'{x} {y}', False, (255,0,0)), (0,0))

        if pygame.mouse.get_pressed()[0]:
            if (self.dragModeCoord == self.dragModeName == None) and self.samePieceClick == None and chessStorage[[z[1] for z in chessStorage].index([x, y])][0][:5] == self.turn if [x, y] in [z[1] for z in chessStorage] else 0:
                """
                if self.dragModeCoord in [z[1] for z in chessStorage]:
                    chessStorage[[z[1] for z in chessStorage].index(self.dragModeCoord)][2] = True
                """
                if [x, y] in [z[1] for z in chessStorage] and self.pressed:
                    #info is for debugging only
                    self.dragModeCoord = [x, y]
                    self.dragModeName = chessStorage[[z[1] for z in chessStorage].index([x, y])][0]
                    self.dragModeInfo = chessStorage[[z[1] for z in chessStorage].index([x, y])]

                    #make the original chess piece invisible
                    if self.samePieceClick == None:
                        chessStorage[[z[1] for z in chessStorage].index(self.dragModeCoord)][2] = False

                    print( movePieces.availableSpots([x, y]) )
                else:
                    self.pressed = False

            #two click mode
            if self.samePieceClick != None and None not in [x, y]:
                if self.selectedChessPieceLegalMoves != None and [x, y] in self.selectedChessPieceLegalMoves:
                    if [x, y] == self.samePieceClick:
                        pass
                    else:
                        #delete a piece if it overlaps
                        if [x, y] in [z[1] for z in chessStorage] and len(chessStorage[[z[1] for z in chessStorage].index([x, y])]):
                            del chessStorage[[z[1] for z in chessStorage].index([x, y])]

                        if len(chessStorage[[z[1] for z in chessStorage].index(self.samePieceClick)]) == 4:
                            chessStorage[[z[1] for z in chessStorage].index(self.samePieceClick)][3] = False
                        chessStorage[[z[1] for z in chessStorage].index(self.samePieceClick)][1] = [x, y]

                    #change the turn
                    self.turn = "black" if self.turn == "white" else "white"
                        
                    self.samePieceClick = None
                    self.pressed = False
                    self.selectedChessPieceLegalMoves = None

                elif [x, y] == self.samePieceClick:
                    self.samePieceClick = None
                    self.selectedChessPieceLegalMoves = None
                    self.pressed = False

            elif None in [x, y]:
                self.samePieceClick = None
                self.selectedChessPieceLegalMoves = None

            #blit out icons for drag Mode
            if self.dragModeName != None:
                screen.blit(pygame.transform.scale(pygame.image.load(os.path.join('icons', f'{self.dragModeName}.png')), (70, 70)),(pygame.mouse.get_pos()[0] - 30, pygame.mouse.get_pos()[1] - 30))

                # chessStorage[[z[1] for z in chessStorage].index(self.samePieceClick)][1] = [x, y]
        else:
            #drag mode stuff
            if None not in [x, y] and [x, y] != self.dragModeCoord != None:
                if self.selectedChessPieceLegalMoves != None and [x, y] in self.selectedChessPieceLegalMoves:
                    #Delete item if it is on top of it
                    if [x, y] in [z[1] for z in chessStorage] and len(chessStorage[[z[1] for z in chessStorage].index([x, y])]):
                        del chessStorage[[z[1] for z in chessStorage].index([x, y])]

                    if len(chessStorage[[z[1] for z in chessStorage].index(self.dragModeCoord)]) == 4:
                        chessStorage[[z[1] for z in chessStorage].index(self.dragModeCoord)][3] = False
                    #change the location of the selected chess piece if it is in a different place or not outside the chess board
                    chessStorage[[z[1] for z in chessStorage].index(self.dragModeCoord)][1] = [x, y]
                    self.dragModeCoord = [x, y]

                    self.selectedChessPieceLegalMoves = None

                    #change turn
                    self.turn = "black" if self.turn == "white" else "white"

            elif None not in [x, y] and self.dragModeCoord != None and [x, y] == self.dragModeCoord:
                #if self.samePieceClick == None and [x, y] == self.dragModeCoord:
                self.samePieceClick = [x, y]
            
            elif None not in [x, y] and self.dragModeCoord != None:
                self.selectedChessPieceLegalMoves = None

            #make the object reappear in drag mode
            if self.dragModeCoord in [z[1] for z in chessStorage]:
                chessStorage[[z[1] for z in chessStorage].index(self.dragModeCoord)][2] = True
                if self.samePieceClick == None:
                    self.selectedChessPieceLegalMoves = None
            
            #reset data for next time
            self.dragModeCoord = self.dragModeName = self.dragModeInfo = None
            self.pressed = True

        #for debugging
        #"""
        print("self.dragModeCoord", self.dragModeCoord)
        print("self.dragModeName", self.dragModeName)
        print("self.dragModeInfo", self.dragModeInfo)
        print("x, y ", [x, y])
        print("You in box with chess piece?", [x, y] in [z[1] for z in chessStorage])
        print("self.samePieceClick", self.samePieceClick)
        print("self.selectedChessPieceLegalMoves", self.selectedChessPieceLegalMoves)
        try:
            print(chessStorage[[z[1] for z in chessStorage].index(self.samePieceClick)])
        except:
            print('Nope')
        print()
        
        if [x, y] in [z[1] for z in chessStorage]:
            print(chessStorage[[z[1] for z in chessStorage].index([x, y])])
        #"""

    def availableSpots(self, chessPiecePos):
        chessPieceName = chessStorage[[z[1] for z in chessStorage].index(chessPiecePos)][0][5:]
        finalList = []

        if chessPieceName == "rook":
            [x, y] = chessPiecePos
            for a in range(4): #4 directions that it will have to create
                for c in range(1, 8): # the range is 8 because the chess board can only go 8 at most anyways so you don't have to limit the stuff and add so much logic
                    trail = [[x - c, y], [x, y - c], [x + c, y], [x, y + c]]
                    if trail[a] in [z[1] for z in chessStorage]:
                        if chessStorage[[z[1] for z in chessStorage].index(trail[a])][0][:5] != self.turn:
                            finalList.append(trail[a])
                        break
                    else:
                        finalList.append(trail[a])

        if chessPieceName == "bishop":
            [x, y] = chessPiecePos
            for a in range(4): #4 directions that it will have to create
                for c in range(1, 8):
                    trail = [[x - c, y - c], [x + c, y - c], [x + c, y + c], [x - c , y + c]]
                    if trail[a] in [z[1] for z in chessStorage]:
                        if chessStorage[[z[1] for z in chessStorage].index(trail[a])][0][:5] != self.turn:
                            finalList.append(trail[a])
                        break
                    else:
                        finalList.append(trail[a])

        if chessPieceName == "queen":
            [x, y] = chessPiecePos
            for a in range(8): #8 directions that it will have to create (diagonal and leftrightupdown)
                for c in range(1, 8):
                    trail = [[x - c, y - c], [x + c, y - c], [x + c, y + c], [x - c , y + c], [x - c, y], [x, y - c], [x + c, y], [x, y + c]]
                    if trail[a] in [z[1] for z in chessStorage]:
                        if chessStorage[[z[1] for z in chessStorage].index(trail[a])][0][:5] != self.turn:
                            finalList.append(trail[a])
                        break
                    else:
                        finalList.append(trail[a])

        if chessPieceName == "knight":
            [x, y] = chessPiecePos
            trail = [[x + 2, y + 1], [x + 2, y - 1], [x - 2, y + 1], [x - 2, y - 1], [x + 1, y + 2], [x - 1, y + 2], [x + 1, y - 2], [x - 1, y - 2]]
            for a in range(8): #for this time, you can't use the same method, because it doesn't move in a line.
                if trail[a] in [z[1] for z in chessStorage]:
                    if chessStorage[[z[1] for z in chessStorage].index(trail[a])][0][:5] != self.turn:
                        finalList.append(trail[a])
                else:
                    finalList.append(trail[a])

        if chessPieceName == "king":
            [x, y] = chessPiecePos
            trail = [[x, y + 1], [x + 1, y + 1], [x + 1, y], [x + 1, y - 1], [x, y - 1], [x - 1, y - 1], [x - 1, y], [x - 1, y + 1]]
            for a in range(8): #for this time, you can't use the same method, because it doesn't move in a line.
                if trail[a] in [z[1] for z in chessStorage]:
                    if chessStorage[[z[1] for z in chessStorage].index(trail[a])][0][:5] != self.turn:
                        finalList.append(trail[a])
                else:
                    finalList.append(trail[a])

        if chessPieceName == "pawn":
            #pawn is special because it attacks diagonally but it moves 1/2 times forward first time then 1 time forward
            [x, y] = chessPiecePos
            pawnPieceTeam = chessStorage[[z[1] for z in chessStorage].index(chessPiecePos)][0][:5]

            twoStepYet = chessStorage[[z[1] for z in chessStorage].index(chessPiecePos)][3]
            trail = {"white" : [[x, y - 1], [x, y - 2]], "black" : [[x, y + 1], [x, y + 2]]}[ chessStorage[[z[1] for z in chessStorage].index(chessPiecePos)][0][:5]]
            detectEnemy = {"white" : [[x - 1, y - 1], [x + 1, y - 1]], "black": [[x - 1, y + 1], [x + 1, y + 1]]}[pawnPieceTeam]

            for m in range(2):
                if detectEnemy[m] in [z[1] for z in chessStorage] and chessStorage[[z[1] for z in chessStorage].index(detectEnemy[m])][0][:5] != self.turn:
                    finalList.append(detectEnemy[m])

            for a in range(2):
                if trail[a] not in [z[1] for z in chessStorage] and ((a == 0) or twoStepYet):
                    finalList.append(trail[a])
                elif trail[a] in [z[1] for z in chessStorage]:
                    break
            
            if detectEnemy in [z[1] for z in chessStorage]:
                finalList.append(detectEnemy)

        self.selectedChessPieceLegalMoves = finalList
        return finalList

movePieces = MovePieces()
while continueGame:
    screen.fill(backgroundColor)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: continueGame = False

    movePieces.drawTable()
    movePieces.selectPiece()

    pygame.display.flip()
    pygame.time.Clock().tick(30)
