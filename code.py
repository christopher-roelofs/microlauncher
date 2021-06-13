import board
import terminalio
import displayio
from adafruit_display_text import label
import os
from gamepadshift import GamePadShift
import digitalio
from time import sleep


class SytemBoard:
    def __init__(self,board):
        self.board = board
        self.a_button = 2
        self.b_button = 1
        self.start_button = 4
        self.select_button = 8

        if self.board == "pygamer":
            self.a_button = 2
            self.b_button = 1
            self.start_button = 4
            self.select_button = 8

red = 0xff0000
orange = 0xffa500
yellow = 0xffff00
green = 0x008000
blue = 0x0000FF
purple = 0x800080
pink = 0xffc0cb
white = 0xFFFFFF
black = 0x000000

myBoard = SytemBoard('pygamer') 

applist = []
menuindex = 0

for filename in os.listdir():
    if 'app_' in filename or 'main.py' in filename or 'game_' in filename:
        applist.append(filename)
applist = sorted(applist)

bc = digitalio.DigitalInOut(board.BUTTON_CLOCK)
bo = digitalio.DigitalInOut(board.BUTTON_OUT)
bl = digitalio.DigitalInOut(board.BUTTON_LATCH)

gamepad = GamePadShift(bc,bo,bl)

display_group = displayio.Group(max_size=20)


file_text = '                              ' 
file_label = label.Label(terminalio.FONT, text=file_text)
file_label.x = 10
file_label.y = 40
file_label.text = applist[0]
display_group.append(file_label)

header_text = "Program Launcher v1"
header_label = label.Label(terminalio.FONT, text=header_text)
header_label.x = 25
header_label.y = 10
display_group.append(header_label)

count_text = "                          "
count_label = label.Label(terminalio.FONT, text=count_text)
count_label.x = 10
count_label.y = 60
count_label.text = 'File {} / {}'.format(str(menuindex + 1),str(len(applist)))
display_group.append(count_label)

directions_text = "<- File Up    File Down ->"
directions_label = label.Label(terminalio.FONT, text=directions_text)
directions_label.x = 0
directions_label.y = 110
display_group.append(directions_label)



board.DISPLAY.show(display_group)

while True:
    pressed = gamepad.get_pressed()

    if pressed == myBoard.select_button and menuindex > 0:
        menuindex -=1
        file_label.text = applist[menuindex]


    if pressed == myBoard.start_button and menuindex < len(applist) -1:
        menuindex +=1
        file_label.text = applist[menuindex]

    if pressed == myBoard.a_button:
        board.DISPLAY.show(None)
        bc.deinit()
        bo.deinit()
        bl.deinit()
        sleep(.1)
        __import__(applist[menuindex].strip('.py'))

    count_label.text = 'File {} / {}'.format(str(menuindex + 1),str(len(applist)))

    while pressed:
        # Wait for all buttons to be released.
        pressed = gamepad.get_pressed()
        sleep(0.1)
    



