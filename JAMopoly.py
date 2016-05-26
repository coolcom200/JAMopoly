try:
    from tkinter import *
except ImportError:
    from Tkinter import *
import time, random
    
root = Tk()
root.title(string = "Monopoly") 
screen = Canvas(root, width=1000, height=1000, background="white")
screen.pack()

class Property:
    def __init__(self, name, cost, color,):
        self.name = name
        self.cost = cost
        self.color = color

Property1 = Property("123", 123, "Blue")






PropNames = [(["Library"], ["Auditorim "]), (["Cafiteria"], ["Gymnasium"]), (["Drama room"], ["Computer"]),
             (["Tech room"], ["Art room"]), (["Com-Tech"], ["Math"]), (["Biology"], ["Phsics"]),
             (["Chemisty"],["Zoology"]), (["French"],["History"])]

gridOverlay = True
if gridOverlay:
    spacing = 20 #Spacing between grid lines
    for x in range(0, 1000, spacing): #Draw vertical lines
        screen.create_line(x, 10, x, 1000, fill="red")
        screen.create_text(x, 0, text=str(x), font="Times 8", anchor = N) #Label lines with coordinates

    for y in range(0, 1000, spacing): #Draw horizontal lines
        screen.create_line(20, y, 1000, y, fill="red")
        screen.create_text(4, y, text=str(y), font="Times 8", anchor = W) #Label lines with coordinates


##quitB = Button(root, text="Quit Tetros", font = "Times 12 bold")
##b=screen.create_window(300, 470, window = quitB)

def find_centre(x,y,x2,y2):
    cx = (x + x2) / 2
    cy = (y + y2) / 2
    return cx,cy


def make_board(centrex, centrey, widthCentre, cellLength, cellWidth, color):
    # screen.create_oval(centrex-20,centrey-20,centrex+20,centrey+20)
    widthCentre = ( 9 * cellWidth )/2
    xCord = centrex - widthCentre
    xCord2 = xCord + cellWidth
    yCord = centrey  -widthCentre
    yCord2 = yCord + cellLength
    yyCord = centrey + widthCentre + cellLength
    yyCord2 = yyCord + cellLength
    xxCord = centrex - widthCentre - cellLength
    xxCord2 = xxCord +cellLength
    for i in range (1, 10):
        StreetName = PropNames[i%len(PropNames)]
        sq = screen.create_rectangle(xCord, yCord, xCord2, yCord2, fill = color)
        ds = screen.create_rectangle(xCord, yyCord, xCord2, yyCord2, fill = color)
        findCords = sq
        xCord = xCord2
        xCord2 += cellWidth
        for x in range(0,2):
            StreetName=PropNames[i%len(PropNames)][x]
            cords = screen.coords(findCords)
            centre = find_centre(cords[0], cords[1] ,cords[2], cords[3])
            screen.create_text(centre[0], centre[1], text = StreetName, font="Times 7", anchor = N)
            findCords = ds

    xCord2 = xCord + cellLength
    for i in range (1, 10):
        yCord = yCord2
        yCord2 += cellWidth
        sq = screen.create_rectangle(xCord, yCord, xCord2, yCord2, fill = color)
        ds = screen.create_rectangle(xxCord, yCord, xxCord2, yCord2, fill = color)


    screen.update()
    time.sleep(0.2)


# def make_row(orientation,startx, starty, spacingx, spacingy):
#     for x in range (1,4):
#         for i in range(1,9):
#             if x % 2 == 0:
#                 spacingx = 100
#                 starty+= 70
#             else:
#                 startx+=spacingx
#             box = screen.create_rectangle(startx, starty, startx + spacingx, starty + spacingy, fill = "#a6ffac")
#             cords = screen.coords(box)
#             centre = find_centre(startx, starty, startx + spacingx, starty + spacingy)
#             screen.create_text(centre[0], centre[1], text = "SOS", font="Times 8", anchor = N)
#             screen.update()
#             time.sleep(0.3)
#             print("R")
#         startx = startx + spacingx
#
#
# def make_board():
#     make_row("Up",100,100,70,100)
#     # screen.create_rectangle(70,100,170,200,fill="#a6ffac")
#     # make_row("DOWN",70,130,70,70)
#     # screen.create_rectangle(730,100,830,200,fill="#a6ffac")
#     # make_row("DOWN",730,130,70,70)
#     # screen.create_rectangle(70,760,170,860,fill="#a6ffac")
#     # make_row("Up",100,760,70,100)
#     # screen.create_rectangle(730,760,830,860,fill="#a6ffac")
#

make_board(350, 250, 200, 70, 50, "#a6ffac")
screen.mainloop()




