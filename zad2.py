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
        global rootB, polynomialText, seedText, iterationsEntry, resultsText
        rootB = Toplevel()
        rootB.title('Rail Fence')
        rootB.minsize(width=500, height=200)
        rootB.configure(bg=maincolor)

        polynomialL = Label(rootB, text='Wielomian: ', background=maincolor)
        seedL = Label(rootB, text='Seed:: ', background=maincolor)
        iterationsL = Label(rootB, text='Ilosc wygenerowanych znakow: ', background=maincolor)
        resultsL = Label(rootB, text='Wyniki: ', background=maincolor)


        polynomialL.grid(row=1, sticky=W, padx=10, pady=10)
        seedL.grid(row=2, sticky=W, padx=10, pady=10)
        iterationsL.grid(row=3, sticky=W, padx=10, pady=10)

        polynomialText = Text(rootB, height=2)
        seedText = Text(rootB, height=2)
        iterationsEntry = Entry(rootB)

        resultsText = Text(rootB, height=15)

        polynomialText.grid(row=1, column=1, sticky=E + W, padx=10, pady=10)
        seedText.grid(row=2, column=1, sticky=E + W, padx=10, pady=10)
        iterationsEntry.grid(row=3, column=1, sticky=E + W, padx=10, pady=10)
        resultsText.grid(row=4, column=1, sticky=E + W, padx=10, pady=10)


        encodeB = Button(rootB, command=self.encrypt, text='Zakoduj')
        encodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)

        rootB.mainloop()


    def encrypt(self):
        resultsText.delete('1.0', END)
        polynomial = polynomialText.get('1.0', 'end').rstrip()
        seed = seedText.get('1.0', 'end').rstrip()

        #polynomial = str(polynomial)
        if not polynomial:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales tekstu do zakodowania.')
            rlbl.pack()
            return

        try:
            iterations = int(iterationsEntry.get())
        except:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Podales nieprawidlowa ilosc poziomow n.')
            rlbl.pack()
            return

        polyArray = []
        for i in polynomial:
            polyArray.append(i)

        seedArray = []
        for i in seed:
            seedArray.append(i)

        currentAutomataState = seedArray
        ones = [num for num, value in enumerate(polyArray) if value == '1' and num != len(polyArray)-1]

        currentIteration = 1
        while currentIteration <= iterations:
            currentXorsLeft = len(ones)-1
            byteToBeXored = bool(int(currentAutomataState[-1]))

            while currentXorsLeft >= 0:
                byteToBeXored = bool(int(currentAutomataState[ones[currentXorsLeft]])) != byteToBeXored
                currentXorsLeft -= 1

            currentAutomataState = [currentAutomataState[-1]] + currentAutomataState[:-1]
            currentAutomataState[0] = int(byteToBeXored)

            resultsText.insert(END, str(iterations) + ': ' + 'Wygenerowana liczba: ' + str(int(byteToBeXored)))
            resultsText.insert(END, '\nObecny stan automatu: ' + "".join(str(x) for x in currentAutomataState) + '\n')

            currentIteration += 1



class Menu():
    def __init__(self):
        global rootC
        rootC = Tk()
        rootC.configure(bg=maincolor)
        rootC.title('Krzysztof Kosinski, Blazej Kwapisz - program BSK')
        rootC.minsize(width=500, height=200)

        railFenceB = Button(rootC, command=partial(RailFence), text='Algorytm Rail Fence', height=2)
        railFenceB.grid(column=1, sticky=E + W, padx=10, pady=10)

        rootC.mainloop()


Menu()
