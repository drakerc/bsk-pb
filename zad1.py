import sys
from functools import partial

reload(sys)
sys.setdefaultencoding('Cp1250')
from Tkinter import *

global maincolor, error
maincolor = '#0288d1'
error = '#ff0000'


class RailFence():
    def __init__(self):
        global rootB, plainTextText, encryptedTextText, linesEntry
        rootB = Toplevel()
        rootB.title('Rail Fence')
        rootB.minsize(width=500, height=200)
        rootB.configure(bg=maincolor)

        plainTextL = Label(rootB, text='Tekst odkodowany: ', background=maincolor)
        encryptedL = Label(rootB, text='Tekst zakodowany: ', background=maincolor)
        linesL = Label(rootB, text='Ilosc linii (n): ', background=maincolor)

        plainTextL.grid(row=1, sticky=W, padx=10, pady=10)
        encryptedL.grid(row=2, sticky=W, padx=10, pady=10)
        linesL.grid(row=3, sticky=W, padx=10, pady=10)

        plainTextText = Text(rootB, height=5)
        encryptedTextText = Text(rootB, height=5)
        linesEntry = Entry(rootB)

        plainTextText.grid(row=1, column=1, sticky=E + W, padx=10, pady=10)
        encryptedTextText.grid(row=2, column=1, sticky=E + W, padx=10, pady=10)
        linesEntry.grid(row=3, column=1, sticky=E + W, padx=10, pady=10)

        encodeB = Button(rootB, command=self.encrypt, text='Zakoduj')
        decodeB = Button(rootB, command=self.decrypt, text='Odkoduj')
        encodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)
        decodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)

        rootB.mainloop()

    def levelSetter(self, direction, currentLevel):
        if direction is 0:
            return currentLevel + 1
        return currentLevel - 1

    def encrypt(self):
        plainText = plainTextText.get('1.0', 'end').rstrip()
        if not plainText:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do zakodowania.')
            rlbl.pack()
            return

        try:
            linesAmount = int(linesEntry.get())
        except:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Podales nieprawidlowa ilosc poziomow n.')
            rlbl.pack()
            return

        encryptedCharsByLevel = []
        # TODO: find a better, cleaner way to initialize an array
        for i in range(0, linesAmount):
            encryptedCharsByLevel.append([])
            encryptedCharsByLevel[i] = ''

        encryptedText = ''
        currentLevel = 0
        direction = 0  # go down
        for character in plainText:
            encryptedCharsByLevel[currentLevel] += character
            if currentLevel is linesAmount - 1:
                direction = 1  # change direction to go up
            if currentLevel is 0:
                direction = 0  # go down

            currentLevel = self.levelSetter(direction, currentLevel)

        for value in encryptedCharsByLevel:
            encryptedText += value

        encryptedTextText.delete('1.0', END)
        encryptedTextText.insert(END, encryptedText)
        return encryptedText


    def offset(self, even, lines, line):
        if line is 0 or line is lines - 1:
            return (lines - 1) * 2

        if even:
            return 2 * line
        return 2 * (lines - 1 - line)

    def decrypt(self):
        encryptedText = encryptedTextText.get('1.0', 'end').rstrip()
        if not encryptedText:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do odkodowania.')
            rlbl.pack()
            return

        try:
            linesAmount = int(linesEntry.get())
        except:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Podales nieprawidlowa ilosc poziomow n.')
            rlbl.pack()
            return

        decryptedChars = [["" for col in range(len(encryptedText))] for row in range(linesAmount)]
        readCharacters = 0

        for line in range(0, linesAmount):
            even = False

            if line is 0:
                pos = 0
            else:
                pos = self.offset(1, linesAmount, line) / 2

            while pos < len(encryptedText) and readCharacters is not len(encryptedText):
                decryptedChars[line][pos] = encryptedText[readCharacters]
                readCharacters += 1

                pos += self.offset(even, linesAmount, line)
                even = not even

        decryptedString = ''
        for i in range(len(encryptedText)):
            for j in range(0, linesAmount):
                decryptedString += decryptedChars[j][i]

        plainTextText.delete('1.0', END)
        plainTextText.insert(END, decryptedString)
        return decryptedString



class PrzestawieniaMacierzowe():
    def __init__(self):
        print 'hello'



class TranspositionPassword():
    def __init__(self):
        global rootB, plainTextText, encryptedTextText, linesEntry
        rootB = Toplevel()
        rootB.title('Transpozycja z haslem')
        rootB.minsize(width=500, height=200)
        rootB.configure(bg=maincolor)

        plainTextL = Label(rootB, text='Tekst odkodowany: ', background=maincolor)
        encryptedL = Label(rootB, text='Tekst zakodowany: ', background=maincolor)
        linesL = Label(rootB, text='Haslo (klucz): ', background=maincolor)

        plainTextL.grid(row=1, sticky=W, padx=10, pady=10)
        encryptedL.grid(row=2, sticky=W, padx=10, pady=10)
        linesL.grid(row=3, sticky=W, padx=10, pady=10)

        plainTextText = Text(rootB, height=5)
        encryptedTextText = Text(rootB, height=5)
        linesEntry = Entry(rootB)

        plainTextText.grid(row=1, column=1, sticky=E + W, padx=10, pady=10)
        encryptedTextText.grid(row=2, column=1, sticky=E + W, padx=10, pady=10)
        linesEntry.grid(row=3, column=1, sticky=E + W, padx=10, pady=10)

        encodeB = Button(rootB, command=self.encrypt, text='Zakoduj')
        decodeB = Button(rootB, command=self.decrypt, text='Odkoduj')
        encodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)
        decodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)

        rootB.mainloop()

    def encrypt(self):
        plainText = plainTextText.get('1.0', 'end').rstrip()
        if not plainText:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do zakodowania.')
            rlbl.pack()
            return

        key = linesEntry.get()
        if not key:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Podales nieprawidlowa ilosc poziomow n.')
            rlbl.pack()
            return

        import math

        charList = [c for c in key]
        charList.sort()

        currentLine = 0
        currentNumber = 0
        passedNumbers = 0

        plainText = "".join(plainText.split())

        floatDivideLenghts = float(float(len(plainText)) / float(len(key)))
        encryptedArray = [["" for col in range(len(key))] for row in range(int(math.ceil(floatDivideLenghts)))]

        while currentNumber < len(key) and passedNumbers < len(plainText):
            encryptedArray[currentLine][currentNumber] = plainText[passedNumbers]
            passedNumbers += 1
            if currentNumber is len(key)-1:
                currentNumber = 0
                currentLine += 1
            else:
                currentNumber += 1

        order = []
        listedChars = list(key)
        for value in charList:
            position = listedChars.index(value)
            order.append(position)
            listedChars[position] = ' '

        encryptedText = ''
        for columnNumber in order:
            for index, value in enumerate(encryptedArray):
                encryptedText += encryptedArray[index][columnNumber]

        encryptedTextText.delete('1.0', END)
        encryptedTextText.insert(END, encryptedText)
        return encryptedText


    def decrypt(self):
        encryptedText = encryptedTextText.get('1.0', 'end').rstrip()
        if not encryptedText:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do odkodowania.')
            rlbl.pack()
            return

        try:
            linesAmount = int(linesEntry.get())
        except:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Podales nieprawidlowa ilosc poziomow n.')
            rlbl.pack()
            return



class Menu():
    def __init__(self):
        global rootC
        rootC = Tk()
        rootC.configure(bg=maincolor)
        rootC.title('Krzysztof Kosinski, Blazej Kwapisz - program BSK')
        rootC.minsize(width=500, height=200)

        railFenceB = Button(rootC, command=partial(RailFence), text='Algorytm Rail Fence', height=2)
        railFenceB.grid(column=1, sticky=E + W, padx=10, pady=10)

        przestawienia = Button(rootC,
                               command=partial(PrzestawieniaMacierzowe), text='Przestawienia macierzowe', height=2)
        przestawienia.grid(column=1, sticky=E + W, padx=10, pady=10)

        transpositionWithPasswordB = Button(rootC,
                               command=partial(TranspositionPassword), text='Przestawienia macierzowe z haslem (2b)', height=2)
        transpositionWithPasswordB.grid(column=1, sticky=E + W, padx=10, pady=10)

        rootC.mainloop()


Menu()
