from tkinter import *
from tkinter.ttk import Notebook
from tkinter import messagebox
import time
import math
import random

__author__ = "Leon Fattakhov"
__copyright__ = "Copyright 2016"
__credits__ = ["Jason Schattman", "Ethan Guo", "Advait Maybhate", "Kevin Lu", "Zach Chapman", "Jeff Dugan"]
__license__ = "GPL"
__version__ = "19"
__maintainer__ = "Leon Fattakhov"
__status__ = "Stable Release"

# Create Main Window
root = Tk()
root.title(string="Leonopoly")
screen = Canvas(root, width=1000, height=650, background="white")

# Disable Resizable properties
root.resizable(width=False, height=False)
screen.pack()
screenRun = False

# Images
startImage = PhotoImage(file='Intro.gif')
endImage = PhotoImage(file='End.gif')
gameImage = PhotoImage(file='Game.gif')
fImage = PhotoImage(file='f2.gif')
nImage = PhotoImage(file='n2.gif')
rImage = PhotoImage(file='r2.gif')
bImage = PhotoImage(file='b2.gif')
iImage = PhotoImage(file='i2.gif')
qImage = PhotoImage(file='q2.gif')

# Create starting background image
screen.create_image(0, 0, image=startImage, anchor=NW)

# Create buttons and windows on Canvas
NewButton = Button(text='New Game', font='Times 24', relief='groove', background='#b59dff', activebackground='#6fcb9f',
                   command=lambda: New_game())
NewBwin = screen.create_window(800, 500, window=NewButton)
IntButton = Button(text='Instructions', font='Times 24', relief='groove', background='#b59dff',
                   activebackground='#6fcb9f', command=lambda: instructions())
IntBwin = screen.create_window(800, 600, window=IntButton)

# Create drop down menu
menubar = Menu(root)
menuB = Menu(menubar, tearoff=0)
menuB2 = Menu(menubar, tearoff=0)
menuB3 = Menu(menubar, tearoff=1)
menuB.add_command(label="New Game", command=lambda: New_game())
menuB.add_command(label="End Game", state='disabled', command=lambda: end_game())
menuB.add_separator()
menuB.add_command(label="Exit", command=root.destroy)
menuB3.add_command(label='Inquire', command=lambda: inquire())
menuB3.add_command(label='Stop Inquire', command=lambda: inquire(False))
menuB2.add_command(label='Instructions', command=lambda: instructions())
menuB2.add_command(label='Key Map', command=lambda: keymap())
menubar.add_cascade(label="File", menu=menuB)
menubar.add_cascade(label='Information', menu=menuB3)
menubar.add_cascade(label='Help', menu=menuB2)
root.configure(menu=menubar)


def grid():
    spacing = 20  # Spacing between grid lines
    for x in range(0, 1000, spacing):  # Draw vertical lines
        screen.create_line(x, 10, x, 1000, fill="red")
        screen.create_text(x, 0, text=str(x), font="Times 8", anchor=N)  # Label lines with coordinates

    for y in range(0, 1000, spacing):  # Draw horizontal lines
        screen.create_line(20, y, 1000, y, fill="red")
        screen.create_text(4, y, text=str(y), font="Times 8", anchor=W)  # Label lines with coordinates


# Finds Centre of given Coordinates
def find_centre(x, y, x2, y2):
    cx = (x + x2) / 2
    cy = (y + y2) / 2
    return cx, cy


# Sets Variables that are used in the game
def setInitValues():
    global LL, rollpos, curTurn
    LL = []
    curTurn = 0
    rollpos = []


def dice_roll():
    # Generates random dice roll and returns it
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return dice1, dice2


# Player Class contains all information relating to the instance of the player
# ranging from their properties to their money. It also stores their position on the board.
# The class also contains the object ID of their token(playing piece)
class Player:
    def __init__(self, player, money=1000, color="RED", figurePosition=0):
        self.playerName = player
        self.color = color
        self.figureP = figurePosition
        self.money = money
        self.propList = []
        self.labels = []

    def draw_pos(self, pointer):
        self.figObjID = pointer

    def properties(self, tile):
        self.propList.append(tile)

    def app_labels(self, label):
        self.labels.append(label)

    def street_house(self, streetList):
        self.streetList = streetList


# Sets up names based on the number of players
def playerSetUp(playerNum, diff):
    global top, EntFrame
    top = Toplevel()
    top.title("Player Setup")
    EntFrame = Frame(top)
    EntFrame.pack()
    # -----Player 1----- #
    entyL = Label(EntFrame, text="Enter Your Name Player 1")
    entyL.pack()
    pName = Entry(EntFrame)
    pName.pack()
    pName.focus_set()
    # -----Player 2----- #
    entyL2 = Label(EntFrame, text="Enter Your Name Player 2")
    entyL2.pack()
    pName2 = Entry(EntFrame)
    pName2.pack()

    # -----Extra Players----- #
    pName3 = None
    pName4 = None
    if playerNum == 3:
        entyL3 = Label(EntFrame, text="Enter Your Name Player 3")
        entyL3.pack()

        pName3 = Entry(EntFrame)
        pName3.pack()



    elif playerNum == 4:
        entyL3 = Label(EntFrame, text="Enter Your Name Player 3")
        entyL3.pack()
        pName3 = Entry(EntFrame)
        pName3.pack()
        entyL4 = Label(EntFrame, text="Enter Your Name Player 4")
        entyL4.pack()
        pName4 = Entry(EntFrame)
        pName4.pack()

    submit = Button(EntFrame, text="Submit", relief='groove', command=lambda: preG(pName, pName2, pName3, pName4, diff))
    submit.pack()


# Retrieves information from playerSetUp Entry widgets and assigns each player their token(playing piece)
def preG(pName, pName2, pName3, pName4, diff):
    global player1, player2, player3, player4, totalP
    # Set Game Difficulty
    if diff == 'Medium':
        money = 700
    elif diff == 'Hard':
        money = 500
    else:
        money = 1000

    totalP = 2
    # Retrieve information from entry widget
    entrLValue = pName.get()
    entrL2Value = pName2.get()
    # Create instance of Player class
    player1 = Player(entrLValue, money)
    player2 = Player(entrL2Value, money)

    player3 = None
    if pName3 != None:
        entrL3Value = pName3.get()
        player3 = Player(entrL3Value, money)

        totalP = 3
    player4 = None

    if pName4 != None:
        entrL4Value = pName4.get()
        player4 = Player(entrL4Value, money)
        totalP = 4

    # Creates Figure Assignment
    def showFigure(y, interface, color, text):
        interface.create_text(50, y, text=text, anchor=N)
        interface.create_rectangle(45, y + 20, 55, y + 30, fill=color)

    EntFrame.destroy()
    can = Canvas(top, width=100, height=120)
    can.pack()

    showFigure(0, can, "Black", 'Player 1 ' + player1.playerName)
    # -----Player 2----- #
    showFigure(30, can, "Pink", "Player 2 " + player2.playerName)

    if player3 != None:
        showFigure(60, can, "Grey34", "Player 3 " + player3.playerName)

    if player4 != None:
        showFigure(90, can, "Gold", "Player 4 " + player4.playerName)

    Button(top, text='Start', relief='groove', command=lambda: start_game(totalP)).pack()


# Uses a spinbox with a "readonly" parameter to allow for user to select total number of players
def game_setUp():
    global top

    def get_value():
        value = w.get()
        value = int(value)
        difficulty = diff.get()
        top.destroy()
        playerSetUp(value, difficulty)
        screen.focus_force()

    top = Toplevel()
    top.title("Player Setup")
    top.tkraise(screen)
    labelPlayerNum = Label(top, text="Select The Number of Players")
    labelPlayerNum.pack()
    w = Spinbox(top, from_=2, to=4, state="readonly")
    w.pack()
    var = StringVar()  # allows for default values to be set
    NameLabel = Label(top, text='Difficulty')
    NameLabel.pack()
    # Difficulty Spinbox
    diff = Spinbox(top, state='readonly', values=('Easy', 'Medium', 'Hard'),
                   textvariable=var)  # forces user to choose between the given values
    var.set('Easy')
    diff.pack()
    submit = Button(top, text="Submit", relief='groove', command=get_value)
    submit.pack()
    top.focus_force()


# rounds values to nearest roundTO value
def roundup(Num, roundTO):
    return int(math.ceil(Num / roundTO)) * roundTO


# Stores all information relating to each tile(instance of Property class)
# it contains the total cost for the property the street group it is in who owns it(this is a reference to the player's
# instance of the Player class) and how many houses/ hotels are on it. It also determines the cost of the tile the
# rent price and the house cost.

class Property:
    def __init__(self, name, x1, y1, x2, y2, color='Green', cost=10, group=0, owner="Bank", home=0, hotel=0, ):
        self.name = name
        self.cost = cost
        self.color = color
        self.rent = int(self.cost / 10)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.home = home
        self.hotel = hotel
        self.owner = owner
        self.group = group
        self.labels = []

    def rentPrice(self, ret):
        if self.home == 'Hotel' or self.home == 5:
            self.home = 0
            self.hotel = 1
        if ret:
            strr = ''
            rentCost = ''
            hotel = 0
            rentInfo = ''
            for home in range(5):
                if hotel == 0:
                    if home == 0:
                        rentCost = self.cost / 10 - 4
                    elif home == 1:
                        rentCost = ((self.cost / 2) - 20)
                    elif home == 2:
                        rentCost = ((self.cost / 2) - 20) * 3
                    elif home == 3:
                        rentCost = roundup(6 * ((self.cost / 2) - 20) + 140, 50)
                    elif home == 4:
                        rentCost = 210 + (7 * ((self.cost / 2) - 20))
                    if home == 0:
                        rentInfo = ('Rent $' + str(int(rentCost)) + '\n')
                    elif home == 1:
                        rentInfo = ("With " + str(home) + " house $" + str(int(rentCost)) + '\n')
                    else:
                        rentInfo = ("With " + str(home) + " houses $" + str(int(rentCost)) + '\n')
                    strr += str(rentInfo)
                else:
                    rentCost = 600 + (5 * ((self.cost / 2) - 20))
            strr += 'With a Hotel $' + str(int(600 + (5 * ((self.cost / 2) - 20))))

            return strr

        else:  # Calculate rent cost based on home and hotel values
            if self.hotel == 0:
                if self.home == 0:
                    self.rent = self.cost / 10 - 4
                elif self.home == 1:
                    self.rent = ((self.cost / 2) - 20)
                elif self.home == 2:
                    self.rent = ((self.cost / 2) - 20) * 3
                elif self.home == 3:
                    self.rent = roundup(6 * ((self.cost / 2) - 20) + 140, 50)
                elif self.home == 4:
                    self.rent = 210 + (7 * ((self.cost / 2) - 20))
            else:
                self.rent = 600 + (5 * ((self.cost / 2) - 20))
            return self.rent

    def houseCost(self):  # Cost for upgrades
        return (self.cost / 2) + 20

    def tileDeedsinfo(self): # Pop up window with all information about property
        top = Toplevel()
        top.minsize(width=150, height=50)
        top.title("Inquire")
        top.lift(aboveThis=screen)
        TopScreen = Canvas(top, width=150, height=200)
        TopScreen.pack()
        TopScreen.create_rectangle(0, 0, 150, 50, fill=self.color)
        TopScreen.create_text(75, 25, text=self.name, font='Times -20 bold')
        TopScreen.create_text(75, 60, text=self.rentPrice(True) + '\nCost for house $' + str((self.cost / 2) + 20),
                              font='Times -15 bold', anchor=N)

    def prop_add(self, labelID):
        self.labels.append(labelID)


# Creates a title deeds card that provides a description of the rent pricing the housing cost
# uses the mouse x and y to find what is under the mouse, then finds the value of the object ID (Key). The Value is a
# instance of the property class.
def info(event):
    CordsofTile = screen.coords(CURRENT)
    try:
        # Finds everything enclosed around the CordsofTile and returns the objectID
        objectID = screen.find_enclosed(CordsofTile[0] - 1, CordsofTile[1] - 1, CordsofTile[2] + 1, CordsofTile[3] + 1)
        strCorrection = str(objectID[0]).replace('(', '')
        strCorrection = strCorrection.replace(')', '')
        strCorrection = strCorrection.replace(',', '')
        try:
            if (dictObjIDTiles[int(
                    strCorrection)].owner) == 'None':  # prevents Free Food, Free Gas, Free Parking and GO from being given a title deeds card
                pass
            else:
                dictObjIDTiles[int(strCorrection)].tileDeedsinfo()

        except KeyError:  # prevents from objects such as buttons from being selected and producing a KeyError
            pass
    except IndexError:
        pass


def inquire(on=True):
    if on:  # Turns on and off inquire tool
        screen.configure(cursor='question_arrow')  # Changes cursor to a question_arrow
        screen.bind("<Button-1>", info)
    else:
        screen.configure(cursor='arrow')  # Changes cursor back to default
        screen.unbind("<Button-1>")  # Unbinds Button-1


def items():
    # Creates all the tiles information (Instances of Property class)
    global tiles
    tile1 = Property('GO', 550, 530, 620, 600, "Yellow", 0, 0, "None")
    tile2 = Property('Alpine', 500, 530, 550, 600, "#7CFC00", 60, 1)
    tile3 = Property('Avenue', 450, 530, 500, 600, "#7CFC00", 80, 1)
    tile4 = Property('Ayr', 400, 530, 450, 600, "#7CFC00", 100, 1)
    tile5 = Property('Baden', 350, 530, 400, 600, '#00FA9A', 100, 2)
    tile6 = Property('Blair', 300, 530, 350, 600, '#00FA9A', 120, 2)
    tile7 = Property('Breslau', 250, 530, 300, 600, '#00FA9A', 150, 2)
    tile8 = Property('Bridge', 200, 530, 250, 600, "#FF1493", 170, 3)
    tile9 = Property('Crest', 150, 530, 200, 600, "#FF1493", 200, 3)
    tile10 = Property('Drift', 100, 530, 150, 600, "#FF1493", 220, 3)
    tile11 = Property('Free Food', 30, 530, 100, 600, "Yellow", 0, 0, "None")
    tile12 = Property('Edna', 30, 480, 100, 530, '#AFEEEE', 140, 4)
    tile13 = Property('Elgin', 30, 430, 100, 480, '#AFEEEE', 140, 4)
    tile14 = Property('Elizabeth ', 30, 380, 100, 430, '#AFEEEE', 180, 4)
    tile15 = Property('Empire', 30, 330, 100, 380, '#D2691E', 190, 5)
    tile16 = Property('Floradale', 30, 280, 100, 330, '#D2691E', 230, 5)
    tile17 = Property('Forest', 30, 230, 100, 280, '#D2691E', 250, 5)
    tile18 = Property('Hill', 30, 180, 100, 230, "#F0E68C", 280, 6)
    tile19 = Property('Bluevale', 30, 130, 100, 180, "#F0E68C", 300, 6)
    tile20 = Property('Eastwood', 30, 80, 100, 130, "#F0E68C", 290, 6)
    tile21 = Property('Free Parking', 30, 10, 100, 80, "Yellow", 0, 0, "None")
    tile22 = Property('Elmira', 100, 10, 150, 80, "#00FA9A", 200, 7)
    tile23 = Property('Heights', 150, 10, 200, 80, "#00FA9A", 250, 7)
    tile24 = Property('Galt', 200, 10, 250, 80, "#00FA9A", 270, 7)
    tile25 = Property('Glenview', 250, 10, 300, 80, "#FFA500", 300, 8)
    tile26 = Property('River', 300, 10, 350, 80, "#FFA500", 290, 8)
    tile27 = Property('Huron', 350, 10, 400, 80, "#FFA500", 280, 8)
    tile28 = Property('Jacob', 400, 10, 450, 80, '#96ceb4', 300, 9)
    tile29 = Property('KW', 450, 10, 500, 80, '#96ceb4', 350, 9)
    tile30 = Property('SJAM', 500, 10, 550, 80, '#96ceb4', 370, 9)
    tile31 = Property('Free Gas', 550, 10, 620, 80, "Yellow", 0, 0, "None")
    tile32 = Property('Southwood', 550.0, 80.0, 620.0, 130.0, '#FF5470', 390, 10)
    tile33 = Property('Waterloo', 550.0, 130.0, 620.0, 180.0, '#FF5470', 380, 10)
    tile34 = Property('Oxford', 550.0, 180.0, 620.0, 230.0, '#FF5470', 350, 10)
    tile35 = Property('Candy Land', 550.0, 230.0, 620.0, 280.0, '#BFAFB2', 400, 11)
    tile36 = Property('Silicon Way', 550.0, 280.0, 620.0, 330.0, '#BFAFB2', 450, 11)
    tile37 = Property('Minescape', 550.0, 330.0, 620.0, 380.0, '#BFAFB2', 440, 11)
    tile38 = Property('Hazel Lane', 550.0, 380.0, 620.0, 430.0, '#FF8866', 430, 12)
    tile39 = Property('Juciy Drive', 550.0, 430.0, 620.0, 480.0, '#FF8866', 490, 12)
    tile40 = Property('Bella Place', 550.0, 480.0, 620.0, 530.0, '#FF8866', 500, 12)
    tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8,
             tile9, tile10, tile11, tile12, tile13, tile14, tile15,
             tile16, tile17, tile18, tile19, tile20, tile21, tile22,
             tile23, tile24, tile25, tile26, tile27, tile28, tile29,
             tile30, tile31, tile32, tile33, tile34, tile35, tile36,
             tile37, tile38, tile39, tile40]


# Runs through tiles list and creates each tile on the screen as a box with its corresponding, color, label and price
def makeB():
    global dictObjIDTiles, rollButton, finishButton, NoteBK, startOBJvalue, screenRun

    screen.create_image(0, 0, image=gameImage, anchor=NW)
    menuB.entryconfigure("End Game", state='normal')

    listObjIDTiles = []
    # Two separate loops in order for screen id of tiles to be connective for the tiles
    for i in tiles:
        tileID = screen.create_rectangle(i.x1, i.y1, i.x2, i.y2, fill=i.color)
        listObjIDTiles.append((tileID, i))
    startOBJvalue = listObjIDTiles[0][0]

    # Place name and cost on tile
    for i in tiles:
        x = find_centre(i.x1, i.y1, i.x2, i.y2)
        costStr = '\n$' + str(i.cost)
        if costStr == '\n$0':
            costStr = ''
        screen.create_text(*x, text=i.name + costStr)

    # Dictionary of object IDs(Key) to instances of the Property class (Value)
    dictObjIDTiles = dict(listObjIDTiles)
    del (listObjIDTiles)

    # Buttons for on screen interaction
    rollButton = Button(text='Roll', relief='groove', background='#b59dff', activebackground='#6fcb9f',
                        command=turn_identify)
    rollBwin = screen.create_window(250, 200, window=rollButton)
    finishButton = Button(text='Finish', relief='groove', background='#b59dff', activebackground='#6fcb9f',
                          state='disabled', command=finish_turn)
    finishBwin = screen.create_window(400, 200, window=finishButton)
    ask_build()
    screenRun = True
    roll_graphics(1, 1, True)

    # Create Notebook Graphic User Interface on a window in the Canvas
    NoteBK = Notebook()
    Window = screen.create_window(630, 0, anchor=NW, height=650, width=480, window=NoteBK)
    create_GUI_info()


# Destroys the Toplevel widget and deletes everything on screen to start the game, initializes the tiles and sets the board
def start_game(numPlayers):
    global numToPlayer
    top.destroy()
    screen.delete(ALL)
    items()
    numToPlayer = {0: player1, 1: player2, 2: player3, 3: player4}
    makeB()
    place_player_pieces(numPlayers)
    print_actions("MOVE", player1)
    rollButton.configure(state='normal')


# Creates the Notebook Panel
def create_GUI_info():
    global PF1, PF2, PF3, PF4, pToFrame, player_unicode, color
    PF1, PF2, PF3, PF4 = 0, 0, 0, 0
    color = '#acfcc4'
    # Creates labels for the tabs based on each player
    if totalP >= 2:
        PF1 = Frame(NoteBK, bg=color)
        Tab1 = NoteBK.add(PF1, text=player1.playerName + '\u2776')
        PF2 = Frame(NoteBK, bg=color)
        NoteBK.add(PF2, text=player2.playerName + '\u2777')

        # Makes labels that are inside the tab
        Label(PF1, text=player1.playerName + ' Properties', bg=color).grid()
        Label(PF2, text=player2.playerName + ' Properties', bg=color).grid()

        M1 = Label(PF1, text='| Money = $' + str(player1.money), bg=color)
        player1.app_labels(M1)
        M1.grid(row=0, column=2)

        M2 = Label(PF2, text='| Money = $' + str(player2.money), bg=color)
        M2.grid(row=0, column=2)
        player2.app_labels(M2)

        player_unicode = {player1: '\u2776', player2: '\u2777'}
        pToFrame = {player1: PF1, player2: PF2}

    if totalP >= 3:
        PF3 = Frame(NoteBK, bg=color)
        NoteBK.add(PF3, text=player3.playerName + '\u2778')

        Label(PF3, text=player3.playerName + ' Properties', bg=color).grid()
        M3 = Label(PF3, text='| Money = $' + str(player3.money), bg=color)
        M3.grid(row=0, column=2)
        player2.app_labels(M3)

        player_unicode = {player1: '\u2776', player2: '\u2777', player3: '\u2778'}
        pToFrame = {player1: PF1, player2: PF2, player3: PF3}

    if totalP == 4:
        PF4 = Frame(NoteBK, bg=color)
        NoteBK.add(PF4, text=player4.playerName + '\u2779')

        Label(PF4, text=player4.playerName + ' Properties', bg=color).grid()
        M4 = Label(PF4, text='| Money = $' + str(player4.money), bg=color)
        M4.grid(row=0, column=2)
        player2.app_labels(M4)

        player_unicode = {player1: '\u2776', player2: '\u2777', player3: '\u2778', player4: '\u2779'}
        pToFrame = {player1: PF1, player2: PF2, player3: PF3, player4: PF4}


def place_player_pieces(numPlayers):
    # places piece in corresponding spots
    goC = [tiles[0].x1, tiles[0].y1, tiles[0].x2, tiles[0].y2]
    centre = find_centre(goC[0], goC[1], goC[2], goC[3])
    piecePos1 = [centre[0] - 10, centre[1] - 10, centre[0], centre[1]]
    piecePos2 = [centre[0] - 10, centre[1] + 10, centre[0], centre[1] + 20]

    if numPlayers >= 3:
        piecePos3 = [centre[0] + 10, centre[1] + 10, centre[0] + 20, centre[1] + 20]
        player3.figure = piecePos3
        player3.color = 'Grey34'
        player3.figObjID = screen.create_rectangle(player3.figure, fill=player3.color)
    if numPlayers == 4:
        piecePos4 = [centre[0] + 10, centre[1], centre[0] + 20, centre[1] - 10]
        player4.figure = piecePos4
        player4.color = "Gold"
        player4.figObjID = screen.create_rectangle(player4.figure, fill=player4.color)

    player1.figure = piecePos1
    player1.color = "Black"
    player1.figObjID = screen.create_rectangle(player1.figure, fill=player1.color)
    player2.figure = piecePos2
    player2.color = "Pink"
    player2.figObjID = screen.create_rectangle(player2.figure, fill=player2.color)


# Deletes old display information and redraws the new information on the side panel
def update_side_bar(player):
    # deletes current labels
    for i in player.labels:
        i.destroy()

    # redraws all Property labels
    for i in range(len(player.propList)):
        frameToUse = pToFrame[player]
        label = Label(frameToUse, text=player.propList[i].name, bg=color)
        label.grid(column=0)
        player.app_labels(label)

    # Draws money label
    Mon = Label(pToFrame[player], text='| Money = $' + str(int(player.money)), bg=color)
    Mon.grid(row=0, column=2)
    player.app_labels(Mon)


# Creates instructions Toplevel widget
def instructions():
    global top
    top = Toplevel()
    top.title('Instructions')
    text = "OBJECT… The object of the game is to become the wealthiest player through buying and renting. " \
           "The winner is the player that has the most money when a person goes bankrupt." \
           "\n\nPLAY… Your token is placed on “GO,” click ‘Roll’ or press r on the keyboard to roll the dice." \
           " Your token is moved by the number of spaces indicated on the dice. " \
           "After you have completed your turn, press ‘Finish’. If you pass “GO” during your turn, you collect $200." \
           "\n\nBUYING PROPERTY… Whenever you land on an unowned property you may buy that property from the Bank at its price." \
           " You will be offered to purchase it. If you chose to do so you will receive the Title Deed showing ownership" \
           " on your tab of the statistics panel. If you do not wish to buy the property it will remain unsold. " \
           "\n\nPAYING RENT… When you land on property owned by another player, the owner collects rent from you in" \
           " accordance with the list printed on its Title Deed card. Having houses or hotels on properties increases " \
           "rent cost. The game will automatically pay for your rent. " \
           "\n\n“Free Parking”, “Free Food”, “Free Gas”… A player landing on any of these tiles " \
           "does not receive any money, property or reward of any kind. This is just a “free” resting place. " \
           "\n\nHOUSES… When you own all the properties in a color-group you may buy houses from the Bank and erect " \
           "them on those properties. If you buy houses, you may place them on any one of those properties or purchase " \
           "houses for different properties in the same color group. The price " \
           "you must pay the Bank for each house is shown on your Title Deed card for the property on which you erect " \
           "the house.\n\nHOTELS… When a player has four houses on each property of a complete color-group, he/she may buy" \
           " a hotel from the Bank and erect it on any property of the color-group. Only one hotel may be erected on any" \
           " one property.\n\nBANKRUPTCY… You are declared bankrupt if you owe more than you can pay either to another " \
           "player or to the Bank. The game ends when one player is bankrupt the other players ranking is based on their " \
           "current net worth."
    # Set scrollbar for the panel
    scBr = Scrollbar(top)
    scBr.pack(side=RIGHT, fill=Y)
    textBox = Text(top, wrap=WORD, height=30, width=50,
                   yscrollcommand=scBr.set)  # assigns the scrollbar to work with the text window
    textBox.pack(fill=BOTH, expand=YES)  # allows window to be resized
    # Puts text in textbox
    textBox.insert(END, text)
    textBox.configure(state="disabled")  # Disables user from entering text
    scBr.configure(command=textBox.yview)  # Stretches scrollbar to fill the height of the widget


# Checks if player owns a street
def check_street(player):
    tempList = []
    matchList = []
    streetList = []
    val = False
    stGrid = []
    for i in player.propList:
        tempList.append(i.group)
        matchList.append(i)
    for inn in range(1, 13):
        Pcount = tempList.count(inn)
        if Pcount == 3:
            indices = [i for i, x in enumerate(tempList) if x == inn]  # returns a list of the indices that match inn
            for i in indices:
                stGrid.append(matchList[i])
            streetList.append(stGrid)
            player.street_house(streetList)
            stGrid = []
            val = True

    return val


# Rolls dice and draws the roll
def roll_graphics(roll1, roll2, loop=False):
    global rollpos
    cordsd1 = [270, 130, 311, 171]
    cordsd2 = [cordsd1[2] + 20, cordsd1[1], cordsd1[2] + 60, cordsd1[3]]
    rollpos = []

    # Dice boxes
    screen.create_rectangle(cordsd1, fill='white')
    screen.create_rectangle(cordsd2, fill='white')

    def make_dots(cordsd1, cordsd2, spacing, size, roll):
        global dots
        # dot spacing is laid out as such
        # ┏━━━┓
        # ┃a   e┃
        # ┃b d f┃
        # ┃c   g┃
        # ┗━━━┛
        a = (cordsd1 + spacing, cordsd2 + spacing, cordsd1 + spacing + size, cordsd2 + spacing + size)
        b = (cordsd1 + spacing, cordsd2 + spacing * 3.333, cordsd1 + spacing + size, cordsd2 + spacing * 3.333 + size)
        c = (cordsd1 + spacing, cordsd2 + spacing * 6, cordsd1 + spacing + size, cordsd2 + spacing * 6 + size)
        d = (cordsd1 + spacing * 3.333, cordsd2 + spacing * 3.333, cordsd1 + spacing * 3.333 + size,
             cordsd2 + spacing * 3.333 + size)
        e = (cordsd1 + spacing * 6, cordsd2 + spacing, cordsd1 + spacing * 6 + size, cordsd2 + spacing + size)
        f = (cordsd1 + spacing * 6, cordsd2 + spacing * 3.333, cordsd1 + spacing * 6 + size,
             cordsd2 + spacing * 3.333 + size)
        g = (cordsd1 + spacing * 6, cordsd2 + spacing * 6, cordsd1 + spacing * 6 + size, cordsd2 + spacing * 6 + size)
        dots = {1: (d, d), 2: (a, g), 3: (a, d, g), 4: (a, c, e, g), 5: (a, c, d, e, g), 6: (a, b, c, e, f, g)}

        for i in dots[roll]:
            rollpos.append(screen.create_oval(i, fill='black'))

    # Makes the dice roll
    SleepT = 0.1
    if loop is False:
        for i in range(1, 15):
            make_dots(cordsd1[0], cordsd1[1], 5, 7, (i % 6) + 1)
            make_dots(cordsd2[0], cordsd2[1], 5, 7, ((i + 2) % 6) + 1)  # Offsets the two dice so they do not roll the same numbers
            screen.update()
            time.sleep(SleepT)
            SleepT += 0.023
            if i != 1:
                for x in rollpos:
                    screen.delete(x)

    make_dots(cordsd1[0], cordsd1[1], 5, 7, roll1)
    make_dots(cordsd2[0], cordsd2[1], 5, 7, roll2)

# Moves tokens to centre of each tile
def move(player, roll):
    Totalroll = sum(roll)
    Posroll = player.figureP + Totalroll
    Gx1 = tiles[Posroll % 40].x1
    Gy1 = tiles[Posroll % 40].y1
    Gx2 = tiles[Posroll % 40].x2
    Gy2 = tiles[Posroll % 40].y2
    centre = find_centre(Gx1, Gy1, Gx2, Gy2)
    cords = screen.coords(player.figObjID)
    createFigure = centre[0] - 5, centre[1] - 5, centre[0] + 5, centre[1] + 5
    screen.coords(player.figObjID, createFigure)
    screen.tag_raise(player.figObjID)
    print_actions("TO", player, tiles[Posroll % 40])
    player.figureP = Posroll


# Creates a cheat sheet for keyboard shortcuts
def keymap():
    top = Toplevel()
    top.title('Key Map')
    top.resizable(height=False, width=False)
    # Uses the compound to allow for text and image to be in the same label
    fLabel = Label(top, image=fImage, text='Finish Turn', font='Times 15 bold italic', compound='left')
    # Sticky forces the labels to line up on the left
    fLabel.grid(sticky='W')
    bLabel = Label(top, image=bImage, text='Build Houses', font='Times 15 bold italic', compound='left')
    bLabel.grid(sticky='W')
    iLabel = Label(top, image=iImage, text='Instructions', font='Times 15 bold italic', compound='left')
    iLabel.grid(sticky='W')
    rLabel = Label(top, image=rImage, text='Roll Dice', font='Times 15 bold italic', compound='left')
    rLabel.grid(sticky='W', row=0, column=1)
    nLabel = Label(top, image=nImage, text='New Game', font='Times 15 bold italic', compound='left')
    nLabel.grid(sticky='W', row=1, column=1)
    qLabel = Label(top, image=qImage, text='Quit', font='Times 15 bold italic', compound='left')
    qLabel.grid(sticky='W', row=2, column=1)


# Displays status of homes and hotels next to the property
def screen_house(prop):
    trimx, trimy, Ttrimx, Ttrimy = 0, 0, 0, 0
    location = tiles.index(prop)
    if location > 30:
        y1 = (prop.y1 + prop.y2) / 2
        x1 = prop.x1
        anc = E
        trimx = 1
        Ttrimx = trimx - 7
        Ttrimy = 4

    elif location > 20:
        x1 = (prop.x1 + prop.x2) / 2
        y1 = prop.y2
        anc = N
        Ttrimx = trimx
        Ttrimy = 15

    elif location > 10:
        y1 = (prop.y1 + prop.y2) / 2
        x1 = prop.x2
        anc = W
        trimx = 6
        Ttrimx = trimx + 6
        Ttrimy = 4


    else:
        x1 = (prop.x1 + prop.x2) / 2
        y1 = prop.y1
        trimy = 6
        anc = S
    # Changes the value of the number based on the properties hotel and house count
    if prop.home == 0 and prop.hotel == 1:
        HValue = 'Hotel'
        unicode = ''
    elif prop.home == 5:
        HValue = 'Hotel'
        unicode = ''
    elif prop.home == 0:
        HValue = ''
        unicode = ''
    else:
        HValue = prop.home
        unicode = '\u2302'

    # Creates the text
    house = screen.create_text(x1 + trimx, y1 + trimy, text=unicode, font='times 25', anchor=anc)
    houseNum = screen.create_text(x1 + Ttrimx, y1 + Ttrimy, text=HValue, anchor=anc)
    # Adds labels to list so replacing labels when necessary can be done
    prop.prop_add(house)
    prop.prop_add(houseNum)


def update_houseValue(listt):
    for i in listt:
        screen.delete(i)


# Makes a spinbox and label for each property
def create_house_label(tkInterface, column, row, text, objAd):
    global LL
    if objAd.hotel == 1 or objAd.home == 5:
        default = 'Hotel'
    else:
        default = objAd.home

    var = StringVar()  # allows for default values to be set
    NameLabel = Label(tkInterface, text='\u2302 ' + text + ' \u2302')
    NameLabel.grid(column=column, row=row)
    box = Spinbox(tkInterface, state='readonly', values=(0, 1, 2, 3, 4, 'Hotel'),
                  textvariable=var)  # forces user to choose between the given values
    var.set(default)
    box.grid(row=row + 1, column=column)
    costLabel = Label(tkInterface, text='Cost per House $' + str((objAd.cost / 2) + 20))
    costLabel.grid(column=column, row=row + 2)
    LL.append([box, objAd])


# Makes actual panel for purchasing homes and hotels using the create_house_label procedure
def build_house(player, index):
    frame.destroy()
    newFrame = Frame(top)
    newFrame.grid()
    for i in range(0, 3):
        objAd = player.streetList[index][i]
        create_house_label(newFrame, i, 0, objAd.name, objAd)

    moneyLabel = Label(newFrame, text=player.playerName + player_unicode[player] + ' has $' + str(player.money))
    moneyLabel.grid()
    sendButton = Button(newFrame, text='Purchase', relief='groove', command=lambda: purchase_house(player, objAd))
    sendButton.grid(column=2, row=3)
    subTButton = Button(newFrame, text='Subtotal', relief='groove', command=lambda: subTotal(player, objAd))
    subTButton.grid(column=1, row=3)


# Predicts cost for purchasing houses
def subTotal(player, objAd):
    money = purchase_house(player, objAd, True)
    totCost = player.money - money
    # Creates and information messagebox to convey the information
    if money < 0:
        money = 'be bankrupt'
    else:
        money = 'have $' + str(money)
    text = 'The total cost for the properties is $' + str(totCost) + ' You would ' + money
    top.tkraise(screen)
    messagebox.showinfo('Sub Total', text)


# Creates panel to choose which street to upgrade
def build_screen(player):
    global top, LL, frame
    LL = []
    top = Toplevel()
    top.title('Buy Houses')
    top.tkraise(screen)
    frame = Frame(top)
    frame.grid()
    for i in range(0, len(player.streetList)):
        streetTiles(player, i, i) # creates button that corresponds to the property upgrade window


def streetTiles(player, i, c):
    Button(frame, text=player.streetList[i][0].name + '\n' + player.streetList[i][1].name + '\n' + player.streetList[i][
        2].name, relief='flat',
           background=player.streetList[i][2].color, command=lambda: build_house(player, i)).grid(row=0, column=c)


# Buys houses or hotels for the property charges the player accordingly
def purchase_house(player, prop, ret=False):
    tempList_values = []
    bought = True
    shown = False

    if ret:
        tempMoney = player.money

    for i in LL:
        x = i[0].get()
        tempList_values.append([x, i[1]])

    for i in tempList_values:
        if i[0] == 'Hotel':
            i[0] = 5

        if ret:
            num_ad = int(i[0]) - i[1].home
            if num_ad > 0:
                tempMoney -= num_ad * i[1].houseCost()

        # Checks for any errors that could occur(ie:buying less houses than you already have)
        if int(i[0]) == i[1].home:
            bought = False
        if int(i[1].home) > int(i[0]):
            bought = False

        else:
            if ret is False:
                num_ad = int(i[0]) - i[1].home

                if player.money - num_ad * i[1].houseCost() < 0:

                    # Shows error message when you buy more than you can afford
                    if shown is False:
                        messagebox._show("Error", "You could not afford to purchase some of the property upgrades")

                    bought = False
                    shown = True

                elif bought:
                    player.money -= num_ad * i[1].houseCost()
                    i[1].home = int(i[0])
                    update_side_bar(player)
                    update_houseValue(i[1].labels)
                    screen_house(i[1])
                    bought = True
    if ret:
        return tempMoney

    top.destroy()

    if bought:
        print_actions('BUILD', player, prop)

    finishButton.configure(state='normal')
    check_bankruptcy(player)


# Displays button for option to Build a house
def ask_build():
    global buildButton
    buildButton = Button(text='Build', relief='groove', background='#b59dff', activebackground='#6fcb9f',
                         command=lambda: build_screen(turn_identify(True)))
    buildBW = screen.create_window(325, 200, window=buildButton)
    buildButton.configure(state='disabled')


# Purchase tiles, subtracts money from player and adds property to their statistics
def makePurchase(player, tileAd):
    player.money -= tileAd.cost
    player.properties(tileAd)
    tileAd.owner = player
    update_side_bar(player)
    check_street(player)
    screen.create_text(tileAd.x1 + 2, tileAd.y1, text=player_unicode[player], anchor=NW)
    print_actions("BUY", player, tileAd)  # Displays on screen that the player bought that property


# Pays rent depending on the property
def pay_rent(playerFrom, propAddress):
    amountDue = propAddress.rentPrice(False)
    propAddress.owner.money += amountDue  # finds tiles owner by using the property class that's owner is an instance of the player class (see line for more information)
    playerFrom.money -= amountDue
    check_bankruptcy(playerFrom)

    # Updates both players side bar
    update_side_bar(playerFrom)
    update_side_bar(propAddress.owner)

    # Prevents the on screen actions display from printing that the player is bankrupt
    if Bankrupt is False:
        print_actions('RENT', playerFrom, propAddress)


# Determines if a player needs to pay rent, or if they can buy a tile
def propPurchaseCheck(player):
    try:
        if player.figureP > 40:
            player.figureP -= 40
            pass_GO(player)  # Adds money to player when they pass go

        objectID = screen.find_below(player.figureP + startOBJvalue) # finds object id of what is below the playing figure
        strCorrection = str(objectID[0]).replace('(', '')
        strCorrection = strCorrection.replace(')', '')
        strCorrection = strCorrection.replace(',', '')

        try:
            objAd = dictObjIDTiles[(int(strCorrection) + 1)]  # attempts to find who the owner of the tile is by
            # looking for a matching instance of the property class(value of the dictionary) to the objectID of the
            #  tile(key of the dictionary)

            ownerT = objAd.owner  # finds owner which can be an instance of the player class or a string

            if ownerT == 'None':  # prevents player from buying Free Food, Free Gas, Free Parking and GO
                pass

            elif ownerT == "Bank":  # if bank is the owner than the tile can be purchase

                if player.money > objAd.cost:  # checks that player can afford the property
                    # Pop up dialog will ask if the want to purchase the property
                    decision = messagebox.askquestion("Purchase", 'Would you like to purchase {}'.format(objAd.name))
                    if decision == 'yes':
                        makePurchase(player, objAd)
                    elif decision == 'no':
                        pass

            elif ownerT != player:  # if the player is not themselves then they will pay rent to the other player
                pay_rent(player, objAd)

            if check_street(player):  # Checks if a player owns 3 title deeds of the same street
                buildButton.configure(state='normal')  # if so then the build Button is activated

        except KeyError:
            pass
    except IndexError:
        pass


# Makes text with actions fly across the screen
def flying_text(words, timer=0.075):
    global dispAct
    rollButton.configure(state='disabled')
    finishButton.configure(state='disabled')
    dispAct = screen.create_text(240, 260, text=words, justify=CENTER, font="Times 24 bold italic")

    # moves text using tkinter built in move command, then deletes dispAct when it makes it across the screen
    for i in range(0, 37):
        screen.move(dispAct, i, 0)
        screen.update()
        time.sleep(timer)
    screen.delete(dispAct)


# Uses the flying_text procedure to display what occurred
def print_actions(action, player, propertyy=0):
    unicode_val = player_unicode[player]
    # if player wishes to remain anonymous they will be refereed to as 'Player [NUMBER]'
    if player.playerName == '':
        name = 'Player ' + unicode_val + "  "
    else:
        name = player.playerName + ' ' + unicode_val + "  "

    # changes text to display based on the parameters given
    if action == "BUY":
        text = name + "purchased " + propertyy.name

    elif action == "RENT":
        text = name + "payed $" + str(propertyy.rentPrice(
            False)) + ' in rent to ' + propertyy.owner.playerName + "\n for landing on " + propertyy.name

    elif action == "BUILD":
        text = name + 'built houses'

    elif action == 'BANKR':
        text = name + 'has gone bankrupt'

    elif action == 'MOVE':
        text = 'It is ' + name + "'s turn"

    elif action == "TO":
        text = name + 'moved to ' + propertyy.name

    # Makes the text fly across the screen
    flying_text(text)



def end_game():
    # checks if player is sure that they want to end the game
    choice = messagebox.askquestion("Quit", 'Are you sure you want to quit?', icon='warning')
    if choice == 'yes':
        # Displays the rankings
        netWorth()


# Binds all key presses to root
def RootKeyHandler(event):
    key = event.keysym
    key.lower()  # forces each key press to be lowercase
    if key == 'i':
        instructions()
    elif key == 'n':
        New_game()
    elif key == 'q':
        end_game()

    if screenRun:
        if key == 'r':
            rollButton.invoke()  # Invokes the button commands
        elif key == 'f':
            finishButton.invoke()
        elif key == 'b':
            buildButton.invoke()


# Adds $300 each time a player passes GO
def pass_GO(player):
    player.money += 300
    update_side_bar(player)


# Calculates net worth of each player based on their properties, houses and overall money, then ranks the players
def netWorth(bankruptP=None):
    tempList = []
    moneyList = []

    # Adds the money and house and the cost of the property together to calculate the players total monetary value
    for i in range(totalP):
        player = numToPlayer[i]
        money = player.money

        for i in (player.propList):
            if i.hotel == 1 or i.home == 'Hotel':
                homes = 5
            else:
                homes = i.home

            money += int(i.cost) + int(homes) * i.houseCost()
        moneyList.append(money)
        tempList.append([money, player])

    for i in tempList:
        if i[1] == bankruptP:
            i[0] = 0
            moneyList[0] = 0

    moneyToPlayer = dict(tempList)
    del tempList
    moneyList.sort(reverse=True)
    strr = ''
    prR = True
    # Sorts the players in a ranking system
    for i in moneyList:
        name = moneyToPlayer[i]

        if moneyList.count(i) == totalP:
            strr = 'Tie, each player has $' + str(i)
            prR = False

        if moneyList.count(i) > 1:
            indices = [z for z, x in enumerate(moneyList) if x == i]
            if len(indices) >= 2 and prR is True:
                strr += "The remaining players finished in a tie each with $" + str(moneyList[indices[0]]) + '\n'
                prR = False

        if bankruptP != None:
            if moneyToPlayer[i].figObjID == bankruptP.figObjID:
                money = 0
        else:
            money = i
        if prR:
            strr += '#' + str(moneyList.index(i) + 1) + ' ' + name.playerName + player_unicode[moneyToPlayer[i]] \
                    + ' has a net value of $' + str(int(money)) + '\n'

    # Makes the end game screen
    final_screen(strr)


# Makes the concluding screen
def final_screen(text):
    global screen
    screen.destroy()  # destroys the main Canvas
    # Overlays a new Canvas
    Nscreen = Canvas(root, width=1000, height=650)
    Nscreen.pack()
    screen = Nscreen

    # Creates a text and image Label displaying the final image and the rankings
    im = Label(screen, image=endImage, text="Rankings\n\n" + text, font='Times 24 bold italic', compound='center')

    # Makes the buttons to replay or to quit out of the game entirely
    NewButton = Button(text='New Game', font='Times 24', relief='groove', background='#b59dff',
                       activebackground='#6fcb9f', command=lambda: New_game())
    ExitButton = Button(text='Quit', font='Times 24', relief='groove', background='#b59dff', activebackground='#6fcb9f',
                        command=root.destroy)

    # Places everything on screen
    screen.create_window(0, 0, window=im, anchor=NW)
    screen.create_window(700, 450, window=NewButton, anchor=NW)
    screen.create_window(700, 550, window=ExitButton, anchor=NW)


# Checks for bankruptcy and if it occurs calls netWorth to conclude the game
def check_bankruptcy(player):
    global Bankrupt
    Bankrupt = False
    if player.money < 0:
        Bankrupt = True
        print_actions('BANKR', player)
        netWorth(player)


def turn(player):
    # Disables roll button and then rolls the dice
    rollButton.configure(state='disabled', disabledforeground='grey')
    diceAmt = dice_roll()

    for i in rollpos:
        screen.delete(i)

    roll_graphics(*diceAmt)  # rolls the dice with graphics(SIDE NOTE: *diceAmt means roll_graphics(diceAmt[0],diceAmt[1]))
    move(player, diceAmt)  # moves the figure to the correct position on the board
    propPurchaseCheck(player)  # Checks if the tile is own or not
    finishButton.configure(state='normal')  # enables the finish turn button


# Finds whose turn it currently is
def turn_identify(ret=False):
    global curTurn
    rollButton.configure(state='disabled')
    curTurn = (curTurn % totalP)
    player = numToPlayer[curTurn]

    if ret is False:
        turn(player)
    else:
        return player


# Finishes a players turn allowing the next player to roll the dice
def finish_turn():
    global curTurn
    # Disables the build button
    buildButton.configure(state='disabled')
    top.destroy()
    curTurn += 1  # changes the current turn value
    player = numToPlayer[curTurn % totalP]  # finds who's turn it is
    print_actions('MOVE', player)  # Displays the current turn on screen
    # disables the finish button and activates the roll button
    finishButton.configure(state='disabled', disabledforeground='grey')
    rollButton.configure(state='normal')


# Starts the Core Game
def New_game():
    game_setUp()
    setInitValues()
    top.protocol("WM_DELETE_WINDOW", lambda: None)  # Disables 'X' on game_setUp screen


root.bind("<Key>", RootKeyHandler)
root.mainloop()
