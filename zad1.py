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

        plainTextText = Text(rootB, height=15)
        encryptedTextText = Text(rootB, height=15)
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

        #encryptedText = encryptedText.replace(" ", "")
        decryptedText = list(encryptedText)
        i = 0
        for row in range(0, linesAmount):
            currentPosition = row
            while currentPosition < len(decryptedText):
                decryptedText[currentPosition] = encryptedText[i]
                i += 1
                if row is 0 or row is linesAmount - 1:
                    currentPosition += 2 * linesAmount - 2
                else:
                    currentPosition += (linesAmount - 1 - (currentPosition) % (linesAmount - 1)) * 2

        plainTextText.delete('1.0', END)
        plainTextText.insert(END, "".join(decryptedText))
        return "".join(decryptedText)



class PrzestawieniaMacierzowe():
    def __init__(self):
        global rootB, plainTextText, encryptedTextText, key
        key = '3-4-1-5-2'
        rootB = Toplevel()
        rootB.title('Transpozycja z ustalonym haslem (3-4-1-5-2)')
        rootB.minsize(width=500, height=200)
        rootB.configure(bg=maincolor)

        plainTextL = Label(rootB, text='Tekst odkodowany: ', background=maincolor)
        encryptedL = Label(rootB, text='Tekst zakodowany: ', background=maincolor)

        plainTextL.grid(row=1, sticky=W, padx=10, pady=10)
        encryptedL.grid(row=2, sticky=W, padx=10, pady=10)

        plainTextText = Text(rootB, height=15)
        encryptedTextText = Text(rootB, height=15)

        plainTextText.grid(row=1, column=1, sticky=E + W, padx=10, pady=10)
        encryptedTextText.grid(row=2, column=1, sticky=E + W, padx=10, pady=10)

        encodeB = Button(rootB, command=self.encrypt, text='Zakoduj')
        decodeB = Button(rootB, command=self.decrypt, text='Odkoduj')
        encodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)
        decodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)

        rootB.mainloop()

    def encrypt(self):
        plain_text = plainTextText.get('1.0', 'end').rstrip()
        if not plain_text:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do zakodowania.')
            rlbl.pack()
            return

        key_arr = self.parse_key(key)
        tab_height = int((len(plain_text) + len(key_arr) - 1) / len(key_arr))
        matrix = [[0 for x in range(len(key_arr))] for y in range(tab_height)]

        for i in range(tab_height):
            for j in range(len(key_arr)):
                matrix[i][j] = ''
        # print(matrix)

        count = 0
        for i in range(tab_height):
            for j in range(len(key_arr)):
                if len(plain_text) > count:
                    matrix[i][j] = plain_text[count]
                    count += 1
        # print(matrix)
        encrypted_text = ''
        for i in range(tab_height):
            for j in range(len(key_arr)):
                encrypted_text += matrix[i][key_arr[j] - 1]

        encrypted = ''.join(encrypted_text).replace(".", "")
        encryptedTextText.delete('1.0', END)
        encryptedTextText.insert(END, encrypted)
        return encrypted

    def decrypt(self):
        encrypted_text = encryptedTextText.get('1.0', 'end').rstrip()
        encrypted_text = encrypted_text.replace(".", "")
        encrypted_text = encrypted_text.replace(".", "")
        encrypted_text = encrypted_text.replace(",", "")
        encrypted_text = encrypted_text.replace("\"", "")

        if not encrypted_text:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do odkodowania.')
            rlbl.pack()
            return

        key_arr = self.parse_key(key)

        decrypted_text = ''

        i = 0
        while i < len(encrypted_text):
            split_text = encrypted_text[i:i + 5]
            # print(split_text)
            if len(split_text) == 1:
                decrypted_text += split_text[0]
                break
            elif len(split_text) == 2:
                decrypted_text += split_text[0] + split_text[1]
            elif len(split_text) == 3:
                decrypted_text += split_text[1] + split_text[2] + split_text[0]
            elif len(split_text) == 4:
                decrypted_text += split_text[2] + split_text[3] + split_text[0] + split_text[1]
            else:
                decrypted_text += split_text[2]
                decrypted_text += split_text[4]
                decrypted_text += split_text[0]
                decrypted_text += split_text[1]
                decrypted_text += split_text[3]
            i += 5
        decrypted_clean = ''.join(decrypted_text).replace(".", "")
        plainTextText.delete('1.0', END)
        plainTextText.insert('1.0', decrypted_clean)
        return decrypted_clean

    def parse_key(self, key_str):
        temp = key.split("-")
        key_numbers = []

        for i in temp:
            try:
                key_numbers.append(int(i))
            except ValueError:
                return None

        return key_numbers


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

        plainTextText = Text(rootB, height=15)
        encryptedTextText = Text(rootB, height=15)
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
            rlbl = Label(r, text='\n[!] Podales nieprawidlowy klucz.')
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

        # put our plaintext in 2D array that is Key-length wide
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
        # create the key-order (for example 1-5-3-4)
        for value in charList:
            position = listedChars.index(value)
            order.append(position)
            listedChars[position] = ' '

        encryptedText = ''
        # encrypt our plaintext and put it in Decrypted box
        for columnNumber in order:
            for index, value in enumerate(encryptedArray):
                encryptedText += encryptedArray[index][columnNumber]

        encryptedTextText.delete('1.0', END)
        encryptedTextText.insert(END, encryptedText)
        return encryptedText


    def decrypt(self):
        encrypted_text = encryptedTextText.get('1.0', 'end').rstrip()
        if not encrypted_text:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do odkodowania.')
            rlbl.pack()
            return

        try:
            key = linesEntry.get()
        except:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Podales nieprawidlowy klucz.')
            rlbl.pack()
            return

        # parsing key
        import string

        key_parsed = [0 for x in range(len(key))]
        counter = 0
        for k in range(len(string.ascii_uppercase[:30])):
            for i in range(len(key)):
                if key[i] == string.ascii_uppercase[k]:
                    key_parsed[i] = counter
                    counter += 1

        # init matrix arrays
        tab_height = int((len(encrypted_text) + len(key_parsed) - 1) / len(key_parsed))
        matrix = [['' for x in range(len(key_parsed))] for y in range(tab_height)]
        last_line_count = len(encrypted_text) - (tab_height - 1) * len(key_parsed)

        decrypted_arr = ['' for x in range(2 * len(encrypted_text) + len(key_parsed))]
        count = 0
        for i in range(len(key_parsed)):
            key_count = -1
            for k in range(len(key_parsed)):
                if key_parsed[k] == i:
                    key_count = k
                    break

            for j in range(tab_height):
                if (j == tab_height - 1) and (key_count >= last_line_count):
                    break
                matrix[j][key_count] = encrypted_text[count]
                count += 1

        count = 0
        for i in range(tab_height):
            for j in range(len(key_parsed)):
                if matrix[i][j] == '':
                    break
                decrypted_arr[count] = matrix[i][j]
                count += 1

        decrypted_text = ''
        for i in range(len(decrypted_arr)):
            if decrypted_arr[i] == '':
                plainTextText.delete('1.0', END)
                plainTextText.insert(END, decrypted_text)
                return decrypted_text
            decrypted_text += decrypted_arr[i]


class Transposition2CPassword():
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

        plainTextText = Text(rootB, height=15)
        encryptedTextText = Text(rootB, height=15)
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
            rlbl = Label(r, text='\n[!] Podales nieprawidlowy klucz.')
            rlbl.pack()
            return

        charList = [c for c in key]
        charList.sort()

        currentLine = 0
        passedNumbers = 0

        # remove spaces from plaintext
        plainText = "".join(plainText.split())

        encryptedArray = []
        order = []
        listedChars = list(key)
        # create the key-order (for example 1-5-3-4)
        for value in charList:
            position = listedChars.index(value)
            order.append(position)
            listedChars[position] = ' '

        charactersAmount = order[0]

        while passedNumbers < len(plainText):
            currentCharacterAmount = 0
            row = []
            while currentCharacterAmount < charactersAmount+1 and passedNumbers < len(plainText):
                row.append(plainText[passedNumbers])
                passedNumbers += 1
                currentCharacterAmount += 1
            encryptedArray.append(row)

            orderingLine = currentLine + 1
            if orderingLine > len(order) - 1:
                orderingLine = 0
                currentLine = 0
                nextOrderingCharacter = order[orderingLine]
                charactersAmount = nextOrderingCharacter
            else:
                nextOrderingCharacter = order[orderingLine]
                charactersAmount = nextOrderingCharacter
                currentLine += 1

        encryptedText = ''
        # encrypt our plaintext and put it in Decrypted box
        for columnNumber in order:
            for index, value in enumerate(encryptedArray):
                try:
                    encryptedText += encryptedArray[index][columnNumber]
                except:
                    pass

        encryptedTextText.delete('1.0', END)
        encryptedTextText.insert(END, encryptedText)
        return encryptedText


    def decrypt(self):
        encrypted_text = encryptedTextText.get('1.0', 'end').rstrip()
        if not encrypted_text:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do odkodowania.')
            rlbl.pack()
            return

        try:
            key = linesEntry.get()
        except:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Podales nieprawidlowy klucz.')
            rlbl.pack()
            return


        charList = [c for c in key]
        charList.sort()

        currentLine = 0
        passedNumbers = 0

        # remove spaces from plaintext
        encrypted_text = "".join(encrypted_text.split())

        order = []
        listedChars = list(key)
        # create the key-order (for example 1-5-3-4)
        for value in charList:
            position = listedChars.index(value)
            order.append(position)
            listedChars[position] = ' '

        charactersAmount = order[0]
        tempEncryptedArray = []
        # create a 2D mock-array that looks the same as the "encrypted" array, but is filled with X characters for now
        while passedNumbers < len(encrypted_text):
            currentRow = 0
            currentCharacterAmount = 0
            row = []
            while currentCharacterAmount < charactersAmount+1 and passedNumbers < len(encrypted_text):
                row.append('X')
                passedNumbers += 1
                currentCharacterAmount += 1
            tempEncryptedArray.append(row)

            orderingLine = currentLine + 1
            if orderingLine > len(order) - 1:
                orderingLine = 0
                currentLine = 0
                nextOrderingCharacter = order[orderingLine]
                charactersAmount = nextOrderingCharacter
            else:
                nextOrderingCharacter = order[orderingLine]
                charactersAmount = nextOrderingCharacter
                currentLine += 1

        decryptedArray = []
        currentSymbol = 0

        # create the encryption array - the one that looks like the array specified on CEZ, but in wrong order for now
        for index, value in enumerate(order):
            verticalSymbolCounter = 0
            verticalColumn = []
            for index2, value2 in enumerate(tempEncryptedArray):
                try:
                    aVariableThatCanFailIfItDoesNotExist = tempEncryptedArray[index2][value]
                    verticalSymbolCounter += 1
                except:
                    pass
            localSymbolCounter = 0
            while localSymbolCounter < verticalSymbolCounter and currentSymbol < len(encrypted_text):
                verticalColumn.append(encrypted_text[currentSymbol])
                currentSymbol += 1
                localSymbolCounter += 1
            decryptedArray.append(verticalColumn)

        # replace index with values in our order, so we'll have a proper order of columns from left to right
        flippedOrder = ['' for x in range(len(order))]
        for index, value in enumerate(order):
            flippedOrder[value] = index

        # create a new array that looks exactly like the array on CEZ with a proper column ordering from left to right
        newArray = []
        for i in flippedOrder:
            newArray.append(decryptedArray[i])

        # start reading the left-to-right array and add its values from its column by using the first letter from a row, removing it and going down as many times as amounts (orders)
        readCharacters = 0
        currentlyReadLine = 0
        decryptedText = ''
        while readCharacters < len(encrypted_text):
            if currentlyReadLine >= len(order):
                currentlyReadLine = 0
            tempAmountOfCharacters = order[currentlyReadLine]
            tempCharactersRead = 0
            while tempCharactersRead < tempAmountOfCharacters+1:
                try:
                    processedCharacter = newArray[tempCharactersRead][0]
                    del newArray[tempCharactersRead][0]
                    decryptedText += processedCharacter
                except:
                    pass
                finally:
                    tempCharactersRead += 1
                    readCharacters += 1
            currentlyReadLine += 1

        plainTextText.delete('1.0', END)
        plainTextText.insert('1.0', decryptedText)

class Caesar():
    def __init__(self):
        global rootB, plainTextText, encryptedTextText, linesEntry
        rootB = Toplevel()
        rootB.title('Szyfr Cezara')
        rootB.minsize(width=500, height=200)
        rootB.configure(bg=maincolor)

        plainTextL = Label(rootB, text='Tekst odkodowany: ', background=maincolor)
        encryptedL = Label(rootB, text='Tekst zakodowany: ', background=maincolor)

        plainTextL.grid(row=1, sticky=W, padx=10, pady=10)
        encryptedL.grid(row=2, sticky=W, padx=10, pady=10)

        plainTextText = Text(rootB, height=15)
        encryptedTextText = Text(rootB, height=15)

        plainTextText.grid(row=1, column=1, sticky=E + W, padx=10, pady=10)
        encryptedTextText.grid(row=2, column=1, sticky=E + W, padx=10, pady=10)

        encodeB = Button(rootB, command=self.encrypt, text='Zakoduj')
        decodeB = Button(rootB, command=self.decrypt, text='Odkoduj')
        encodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)
        decodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)

        rootB.mainloop()

    def encrypt(self):
        plain_text = plainTextText.get('1.0', 'end').rstrip()
        if not plain_text:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do zakodowania.')
            rlbl.pack()
            return

        import re, string

        plain_text = re.sub("[^a-zA-Z]", "", plain_text).upper()
        k0 = 15
        k1 = 11
        n = 26
        euler = 12

        encrypted_text = ""
        for i in range(len(plain_text)):
            current_index = string.ascii_uppercase.index(plain_text[i])
            encrypted_index = (current_index * k1 + k0) % n
            encrypted_text += string.ascii_uppercase[encrypted_index]

        encryptedTextText.delete('1.0', END)
        encryptedTextText.insert(END, encrypted_text)
        return encrypted_text


    def decrypt(self):
        encrypted_text = encryptedTextText.get('1.0', 'end').rstrip()
        if not encrypted_text:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do zakodowania.')
            rlbl.pack()
            return

        import re, string

        encrypted_text = re.sub("[^a-zA-Z]", "", encrypted_text).upper()
        k0 = 15
        k1 = 11
        n = 26
        euler = 12

        decrypted_text = ""
        for i in range(len(encrypted_text)):
            current_index = string.ascii_uppercase.index(encrypted_text[i])
            decrypted_index = (current_index + (n - k0)) * pow(k1, euler - 1) % n
            decrypted_text += string.ascii_uppercase[decrypted_index]

        plainTextText.delete('1.0', END)
        plainTextText.insert(END, decrypted_text)
        return decrypted_text

class Vigenere():
    def __init__(self):
        global rootB, plainTextText, encryptedTextText, linesEntry
        rootB = Toplevel()
        rootB.title('Szyfr Vigenere\'a')
        rootB.minsize(width=500, height=200)
        rootB.configure(bg=maincolor)

        plainTextL = Label(rootB, text='Tekst odkodowany: ', background=maincolor)
        encryptedL = Label(rootB, text='Tekst zakodowany: ', background=maincolor)
        linesL = Label(rootB, text='Haslo (klucz): ', background=maincolor)

        plainTextL.grid(row=1, sticky=W, padx=10, pady=10)
        encryptedL.grid(row=2, sticky=W, padx=10, pady=10)
        linesL.grid(row=3, sticky=W, padx=10, pady=10)

        plainTextText = Text(rootB, height=15)
        encryptedTextText = Text(rootB, height=15)
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
        plain_text = plainTextText.get('1.0', 'end').rstrip()
        if not plain_text:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do zakodowania.')
            rlbl.pack()
            return

        key = linesEntry.get()
        if not key or len(key) > plain_text:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Wprowadzono nieprawidlowy klucz.')
            rlbl.pack()
            return

        import re, string

        plain_text = re.sub("[^a-zA-Z]", "", plain_text).upper()
        key = re.sub("[^a-zA-Z]", "", key).upper()

        # check if key length is < decrypted text length
        if len(key) < len(plain_text):
            i = 0
            original_key_len = len(key)
            while len(key) != len(plain_text):
                key += key[i % original_key_len]
                i += 1
        elif len(key) > len(plain_text):
            print('len(key) > len(string)!')
            return None

        encrypted_text = ""
        plain_array = list(plain_text.upper())
        for i in range(len(plain_array)):
            # translating plain char -> encrypted char
            index_plain = string.ascii_uppercase.index(plain_array[i])
            index_key = string.ascii_uppercase.index(key[i])
            encrypted_text += string.ascii_uppercase[(index_plain + index_key) % len(string.ascii_uppercase)]

        encryptedTextText.delete('1.0', END)
        encryptedTextText.insert(END, encrypted_text)
        return encrypted_text



    def decrypt(self):
        encrypted_text = encryptedTextText.get('1.0', 'end').rstrip()
        if not encrypted_text:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do zakodowania.')
            rlbl.pack()
            return

        key = linesEntry.get()
        if not key or len(key) > encrypted_text:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Wprowadzono nieprawidlowy klucz.')
            rlbl.pack()
            return

        import re, string

        encrypted_text = re.sub("[^a-zA-Z]", "", encrypted_text).upper()
        key = re.sub("[^a-zA-Z]", "", key).upper()

        # check if key length is < encrypted text length
        if len(key) < len(encrypted_text):
            i = 0
            original_key_len = len(key)
            while len(key) != len(encrypted_text):
                key += key[i % original_key_len]
                i += 1
        elif len(key) > len(encrypted_text):
            print('len(key) > len(string)!')
            return None

        decrypted_text = ""
        encrypted_array = list(encrypted_text)
        for i in range(len(encrypted_array)):
            # translating encrypted char -> decrypted
            index_encrypted = string.ascii_uppercase.index(encrypted_array[i])
            index_key = string.ascii_uppercase.index(key[i])
            decrypted_text += string.ascii_uppercase[(index_encrypted - index_key) % len(string.ascii_uppercase)]

        plainTextText.delete('1.0', END)
        plainTextText.insert(END, decrypted_text)
        return decrypted_text


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

        transpositionWithPassword2CB = Button(rootC,
                               command=partial(Transposition2CPassword), text='Przestawienia macierzowe z haslem (2C)', height=2)
        transpositionWithPassword2CB.grid(column=1, sticky=E + W, padx=10, pady=10)

        caesarB = Button(rootC,
                    command=partial(Caesar), text='Szyfr Cezara', height=2)
        caesarB.grid(column=1, sticky=E + W, padx=10, pady=10)

        vigenereB = Button(rootC,
                    command=partial(Vigenere), text='Szyfr Vigenere\'a', height=2)
        vigenereB.grid(column=1, sticky=E + W, padx=10, pady=10)

        rootC.mainloop()


Menu()
