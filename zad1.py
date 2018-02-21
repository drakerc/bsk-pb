# def encrypt(text, keyNo):
#     length = len(text)
#     centerLength = length / (keyNo-1)
#
#     if length % (keyNo-1) == 0:
#         outsideLengths = centerLength / 2
#         differenceBetweenArrayElements = 2 * (keyNo-1)
#         i = 0
#         while (i < outsideLengths):
#
#
#
import sys
from functools import partial

reload(sys)
sys.setdefaultencoding('Cp1250')
from Tkinter import *

global maincolor
maincolor = '#0288d1'

class RailFence():
    def __init__(self):
        global rootB, plainTextText, encryptedTextText, linesEntry
        rootB = Toplevel()
        rootB.title('Rail Fence')
        rootB.minsize(width=500, height=200)
        rootB.configure(bg=maincolor)

        plainTextL = Label(rootB, text='Tekst odkodowany: ', background = maincolor)
        encryptedL = Label(rootB, text='Tekst zakodowany: ', background = maincolor)
        linesL = Label(rootB, text='Ilosc linii (n): ', background = maincolor)

        plainTextL.grid(row=1, sticky=W, padx=10, pady=10)
        encryptedL.grid(row=2, sticky=W, padx=10, pady=10)
        linesL.grid(row=3, sticky=W, padx=10, pady=10)

        plainTextText = Text(rootB, height=5)
        encryptedTextText = Text(rootB, height=5)
        linesEntry = Entry(rootB)

        plainTextText.grid(row=1, column=1, sticky=E + W, padx=10, pady=10)
        encryptedTextText.grid(row=2, column=1, sticky=E + W, padx=10, pady=10)
        linesEntry.grid(row=3, column=1, sticky=E + W, padx=10, pady=10,)

        encodeB = Button(rootB, command=self.railFenceEncrypt, text='Zakoduj')
        decodeB = Button(rootB, command=self.railFenceDecrypt, text='Odkoduj')
        encodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)
        decodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)

        rootB.mainloop()


    def railFenceLevelSetter(self, direction, currentLevel):
        if direction is 0:
            return currentLevel + 1
        return currentLevel - 1


    def railFenceEncrypt(self):
        plainText = plainTextText.get('1.0', 'end').rstrip()
        linesAmount = int(linesEntry.get())

        encryptedCharsByLevel = []
        # TODO: find a better, cleaner way to initialize an array
        for i in range(0, linesAmount):
            encryptedCharsByLevel.append([])
            encryptedCharsByLevel[i] = ''

        encryptedText = ''
        currentLevel = 0
        direction = 0 # go down
        for character in plainText:
            encryptedCharsByLevel[currentLevel] += character
            if currentLevel is linesAmount-1:
                direction = 1 # change direction to go up
            if currentLevel is 0:
                direction = 0 # go down

            currentLevel = self.railFenceLevelSetter(direction, currentLevel)

        for value in encryptedCharsByLevel:
            encryptedText += value

        encryptedTextText.insert(END, encryptedText)
        return encryptedText

    def railFenceDecrypt(self):
        return 1


class PrzestawieniaMacierzowe():
    def __init__(self):
        print 'hello'


class Menu():
    def __init__(self):
        global rootC
        rootC = Tk()
        rootC.configure(bg=maincolor)
        rootC.title('Krzysztof Kosinski, Blazej Kwapisz - program BSK')
        rootC.minsize(width=500, height=200)

        railFenceB = Button(rootC,
                       command=partial(RailFence), text='Algorytm Rail Fence', height=2)
        railFenceB.grid(column=1, sticky=E + W, padx=10, pady=10)

        przestawienia = Button(rootC,
                       command=partial(PrzestawieniaMacierzowe), text='Przestawienia macierzowe', height=2)
        przestawienia.grid(column=1, sticky=E + W, padx=10, pady=10)

        rootC.mainloop()

Menu()