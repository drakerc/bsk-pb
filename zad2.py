import sys
from functools import partial

# reload(sys)
# sys.setdefaultencoding('Cp1250')
from tkinter import *

global maincolor, error
maincolor = '#0288d1'
error = '#ff0000'


class RailFence():
    def __init__(self):
        global rootB, polynomialText, seedText, iterationsEntry, resultsText
        rootB = Toplevel()
        rootB.title('LFSR')
        rootB.minsize(width=500, height=200)
        rootB.configure(bg=maincolor)

        polynomialL = Label(rootB, text='Wielomian: ', background=maincolor)
        seedL = Label(rootB, text='Poczatkowy klucz: ', background=maincolor)
        iterationsL = Label(rootB, text='Ilosc wygenerowanych znakow (liczba iteracji): ', background=maincolor)
        resultsL = Label(rootB, text='Wyniki: ', background=maincolor)


        polynomialL.grid(row=1, sticky=W, padx=10, pady=10)
        seedL.grid(row=2, sticky=W, padx=10, pady=10)
        iterationsL.grid(row=3, sticky=W, padx=10, pady=10)
        resultsL.grid(row=4, sticky=W, padx=10, pady=10)

        polynomialText = Text(rootB, height=1)
        seedText = Text(rootB, height=1)
        iterationsEntry = Entry(rootB)

        resultsText = Text(rootB, height=20)

        polynomialText.grid(row=1, column=1, sticky=E + W, padx=10, pady=10)
        seedText.grid(row=2, column=1, sticky=E + W, padx=10, pady=10)
        iterationsEntry.grid(row=3, column=1, sticky=E + W, padx=10, pady=10)
        resultsText.grid(row=4, column=1, sticky=E + W, padx=10, pady=10)

        encodeB = Button(rootB, command=self.encrypt, text='Generuj')
        encodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)

        rootB.mainloop()


    def encrypt(self):
        resultsText.delete('1.0', END)
        polynomial = polynomialText.get('1.0', 'end').rstrip()
        seed = seedText.get('1.0', 'end').rstrip()

        if not polynomial or not seed:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales wielomianu lub poczatkowego klucza.')
            rlbl.pack()
            return

        try:
            iterations = int(iterationsEntry.get())
        except:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Podales nieprawidlowa liczbe iteracji.')
            rlbl.pack()
            return

        polyArray = []
        for i in polynomial:
            polyArray.append(i)

        seedArray = []
        for i in seed:
            seedArray.append(i)

        otherSymbolsPoly = [num for num, value in enumerate(polyArray) if value != '1' and value != '0']
        otherSymbolsSeed = [num for num, value in enumerate(seedArray) if value != '1' and value != '0']
        if len(otherSymbolsPoly) > 0 or len(otherSymbolsSeed) > 0 or len(seedArray) is not len(polyArray):
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x100')
            rlbl = Label(r, text='\n[!] Wprowadziles nieprawidlowe znaki lub \ndlugosc ziarna nie jest taka sama jak \nnajwiekszy stopien wielomianu.')
            rlbl.pack()
            return

        currentAutomataState = seedArray
        ones = [num for num, value in enumerate(polyArray) if value == '1' and num != len(polyArray)-1]

        #resultsText.insert(END, str('0') + ' iteracja: ' + 'Wygenerowana liczba: ' + str(int(currentAutomataState[-1])) + '\n')

        currentIteration = 1
        while currentIteration <= iterations:
            currentXorsLeft = len(ones)-1
            byteToBeXored = bool(int(currentAutomataState[-1]))

            while currentXorsLeft >= 0:
                byteToBeXored = bool(int(currentAutomataState[ones[currentXorsLeft]])) != byteToBeXored
                currentXorsLeft -= 1
            resultsText.insert(END, str(currentIteration) + ' iteracja: ' + 'wychodzi: ' + str(int(currentAutomataState[-1])) + '\n')

            currentAutomataState = [currentAutomataState[-1]] + currentAutomataState[:-1] # przesuniecie w prawo
            currentAutomataState[0] = int(byteToBeXored)

            currentStateString = "".join(str(x) for x in currentAutomataState)

            test = currentAutomataState[-1]

            #resultsText.insert(END, str(currentIteration) + ' iteracja: ' + 'Wygenerowana liczba: ' + str(int(test)))

            resultsText.insert(END, str(currentIteration) + ' iteracja: ' + 'Wygenerowana liczba: ' + str(int(byteToBeXored)))
            resultsText.insert(END, '\nObecny stan automatu: ' + currentStateString + ' (' + str(int(currentStateString, 2)) + ')' + '\n')
            resultsText.insert(END, '------------------'+ '\n')

            currentIteration += 1

class CiphertextAutokey():
    def __init__(self):
        global rootB, polynomialText, seedText, inputEntry, outputEntry
        rootB = Toplevel()
        rootB.title('LFSR')
        rootB.minsize(width=500, height=200)
        rootB.configure(bg=maincolor)

        polynomialL = Label(rootB, text='Wielomian: ', background=maincolor)
        seedL = Label(rootB, text='Poczatkowy klucz: ', background=maincolor)
        inputL = Label(rootB, text='Nazwa pliku wejsciowego (z rozszerzeniem): ', background=maincolor)
        outputL = Label(rootB, text='Nazwa pliku wyjsciowego (z rozszerzeniem): ', background=maincolor)

        polynomialL.grid(row=1, sticky=W, padx=10, pady=10)
        seedL.grid(row=2, sticky=W, padx=10, pady=10)
        inputL.grid(row=3, sticky=W, padx=10, pady=10)
        outputL.grid(row=4, sticky=W, padx=10, pady=10)

        polynomialText = Text(rootB, height=1)
        seedText = Text(rootB, height=1)
        inputEntry = Text(rootB, height=1)
        outputEntry = Text(rootB, height=1)

        polynomialText.insert('1.0', '11001')
        seedText.insert('1.0', '11111')
        inputEntry.insert('1.0', 'decodedphoto.jpg')
        outputEntry.insert('1.0', 'output.bin')


        polynomialText.grid(row=1, column=1, sticky=E + W, padx=10, pady=10)
        seedText.grid(row=2, column=1, sticky=E + W, padx=10, pady=10)
        inputEntry.grid(row=3, column=1, sticky=E + W, padx=10, pady=10)
        outputEntry.grid(row=4, column=1, sticky=E + W, padx=10, pady=10)

        encodeB = Button(rootB, command=partial(self.ciphertext, 'encrypt'), text='Enkoduj')
        encodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)

        encodeB = Button(rootB, command=partial(self.ciphertext, 'decrypt'), text='Dekoduj')
        encodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)

        rootB.mainloop()

    def generateLsfr(self, ones, currentAutomataState):
        currentXorsLeft = len(ones)-1
        byteToBeXored = bool(int(currentAutomataState[-1]))

        while currentXorsLeft >= 0:
            byteToBeXored = bool(int(currentAutomataState[ones[currentXorsLeft]])) != byteToBeXored
            currentXorsLeft -= 1

        currentAutomataState = [currentAutomataState[-1]] + currentAutomataState[:-1] # przesuniecie w prawo
        currentAutomataState[0] = int(byteToBeXored)

        return byteToBeXored, currentAutomataState


    def ciphertext(self, mode):
        polynomial = polynomialText.get('1.0', 'end').rstrip()
        seed = seedText.get('1.0', 'end').rstrip()
        input = inputEntry.get('1.0', 'end').rstrip()
        output = outputEntry.get('1.0', 'end').rstrip()

        if not polynomial or not seed or not input or not output:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales wielomianu lub poczatkowego klucza.')
            rlbl.pack()
            return

        import numpy as np

        try:
            f = open(input, "r")
            a = np.fromfile(f, dtype=np.uint8)
        except:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Plik wejsciowy nie istnieje.')
            rlbl.pack()
            return

        file_object = open(output, 'wb')

        polyArray = []
        for i in polynomial:
            polyArray.append(i)

        seedArray = []
        for i in seed:
            seedArray.append(i)

        otherSymbolsPoly = [num for num, value in enumerate(polyArray) if value != '1' and value != '0']
        otherSymbolsSeed = [num for num, value in enumerate(seedArray) if value != '1' and value != '0']
        if len(otherSymbolsPoly) > 0 or len(otherSymbolsSeed) > 0 or len(seedArray) is not len(polyArray):
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x100')
            rlbl = Label(r, text='\n[!] Wprowadziles nieprawidlowe znaki lub \ndlugosc ziarna nie jest taka sama jak \nnajwiekszy stopien wielomianu.')
            rlbl.pack()
            return

        currentAutomataState = seedArray
        ones = [num for num, value in enumerate(polyArray) if value == '1' and num != len(polyArray)-1]

        if mode is 'encrypt':
            for i in range(0, len(a)):
                result, automata = self.encryptSelectBit(a, ones, currentAutomataState, a[i])
                file_object.write(result)
                currentAutomataState = automata
        else:
            for i in range(0, len(a)):
                result, automata = self.decryptSelectBit(a, ones, currentAutomataState, a[i])
                file_object.write(result)
                currentAutomataState = automata
        r = Tk()
        r.configure(bg=error)
        r.title('Informacja')
        r.geometry('350x50')
        rlbl = Label(r, text='\n[!] Algorytm zakonczyl dzialanie')
        rlbl.pack()
        return

    def encryptSelectBit(self, a, ones, currentAutomataState, byteInputCharacter):
        textEncryptionResult = 0
        for j in range(0, 8):
            byteToBeXored, currentAutomataState = self.generateLsfr(ones, currentAutomataState)

            byteInputCharacter = byteInputCharacter

            byteToXor = str(int(byteInputCharacter) & 2**j)
            movedByteToXor = int(byteToXor) >> j

            byteToBeXored = movedByteToXor != byteToBeXored

            currentAutomataState[0] = int(byteToBeXored)
            textEncryptionResult = textEncryptionResult | (int(byteToBeXored) << j)
        return bytes([textEncryptionResult]), currentAutomataState

    def decryptSelectBit(self, a, ones, currentAutomataState, byteInputCharacter):
        textEncryptionResult = 0
        for j in range(0, 8):
            byteToBeXored, currentAutomataState = self.generateLsfr(ones, currentAutomataState)

            byteInputCharacter = byteInputCharacter

            byteToXor = str(int(byteInputCharacter) & 2**j)
            movedByteToXor = int(byteToXor) >> j

            byteToBeXored = movedByteToXor != byteToBeXored

            currentAutomataState[0] = int(movedByteToXor)

            textEncryptionResult =  textEncryptionResult | (int(byteToBeXored) << j)
        return bytes([textEncryptionResult]), currentAutomataState

class Menu():
    def __init__(self):
        global rootC
        rootC = Tk()
        rootC.configure(bg=maincolor)
        rootC.title('Krzysztof Kosinski, Blazej Kwapisz - program BSK')
        rootC.minsize(width=500, height=200)

        railFenceB = Button(rootC, command=partial(RailFence), text='LFSR', height=2)
        railFenceB.grid(column=1, sticky=E + W, padx=10, pady=10)

        ciphertextAutokey = Button(rootC, command=partial(CiphertextAutokey), text='Ciphertext Autokey', height=2)
        ciphertextAutokey.grid(column=2, sticky=E + W, padx=10, pady=10)

        rootC.mainloop()

Menu()
