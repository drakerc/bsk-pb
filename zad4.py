import numpy as np

from functools import partial
from tkinter import *

global maincolor, error, Des
maincolor = '#0288d1'
error = '#ff0000'


class CiphertextAutokey():
    def __init__(self):
        global rootB, seedText, inputEntry, outputEntry
        rootB = Toplevel()
        rootB.title('DES')
        rootB.minsize(width=500, height=200)
        rootB.configure(bg=maincolor)

        seedL = Label(rootB, text='Poczatkowy klucz: ', background=maincolor)
        inputL = Label(rootB, text='Nazwa pliku wejsciowego (z rozszerzeniem): ', background=maincolor)
        outputL = Label(rootB, text='Nazwa pliku wyjsciowego (z rozszerzeniem): ', background=maincolor)

        seedL.grid(row=2, sticky=W, padx=10, pady=10)
        inputL.grid(row=3, sticky=W, padx=10, pady=10)
        outputL.grid(row=4, sticky=W, padx=10, pady=10)

        seedText = Text(rootB, height=1)
        inputEntry = Text(rootB, height=1)
        outputEntry = Text(rootB, height=1)

        seedText.insert('1.0', 'przykladowy klucz')
        inputEntry.insert('1.0', 'input.pdf')
        outputEntry.insert('1.0', 'output.bin')

        seedText.grid(row=2, column=1, sticky=E + W, padx=10, pady=10)
        inputEntry.grid(row=3, column=1, sticky=E + W, padx=10, pady=10)
        outputEntry.grid(row=4, column=1, sticky=E + W, padx=10, pady=10)

        encodeB = Button(rootB, command=partial(self.start_cipher, 'encode'), text='Enkoduj')
        encodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)

        encodeB = Button(rootB, command=partial(self.start_cipher, 'decode'), text='Dekoduj')
        encodeB.grid(columnspan=2, sticky=E + W, padx=10, pady=10)

        rootB.mainloop()

    def start_cipher(self, type):
        seed = seedText.get('1.0', 'end').rstrip()
        input = inputEntry.get('1.0', 'end').rstrip()
        output = outputEntry.get('1.0', 'end').rstrip()

        if not seed or not input or not output:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Nie podales wielomianu lub poczatkowego klucza.')
            rlbl.pack()
            return

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

        # KEY LOADED FROM FILE
        try:
            key_file = open(seed, "r")
            key_arr = np.fromfile(key_file, dtype=np.uint8)
        except:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Plik seedowy nie istnieje.')
            rlbl.pack()
            return

        file_object = open(output, 'wb')
        a_str = ''
        for it in a:
            a_str += str(chr(it))

        key_str = ''
        for it in key_arr:
            key_str += str(chr(it))

        d = Des()

        # KEY IS A STANDARD STRING
        # if type == 'encode':
        #     out = d.encrypt(str(seed), a_str, True)
        # else:
        #     out = d.decrypt(str(seed), a_str, True)

        # KEY FROM A FILE
        if type == 'encode':
            out = d.encrypt(key_str, a_str, True)
        else:
            out = d.decrypt(key_str, a_str, True)


        out_arr = []
        for it in out:
            out_arr.append(ord(it))

        file_object.write(bytearray(out_arr))
        
        r = Tk()
        r.configure(bg=error)
        r.title('Informacja')
        r.geometry('350x50')
        rlbl = Label(r, text='\n[!] Algorytm zakonczyl dzialanie')
        rlbl.pack()
        return


class Menu():
    def __init__(self):
        global rootC
        rootC = Tk()
        rootC.configure(bg=maincolor)
        rootC.title('Krzysztof Kosinski, Blazej Kwapisz - program BSK')
        rootC.minsize(width=500, height=200)

        button = Button(rootC, command=partial(CiphertextAutokey), text='Algorytm DES', height=2)
        button.grid(column=2, sticky=E + W, padx=10, pady=10)

        rootC.mainloop()

class Des:
    ENCRYPT = 1
    DECRYPT = 0

    PI = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    CP_1 = [57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4]

    CP_2 = [14, 17, 11, 24, 1, 5, 3, 28,
            15, 6, 21, 10, 23, 19, 12, 4,
            26, 8, 16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55, 30, 40,
            51, 45, 33, 48, 44, 49, 39, 56,
            34, 53, 46, 42, 50, 36, 29, 32]

    E = [32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32, 1]

    S_BOX = [
        [
         [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
        ],

        [
         [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
        ],

        [
         [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],

        [
         [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
        ],

        [
         [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
        ],

        [
         [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],

        [
         [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
        ],

        [
         [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]
    ]

    P = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]

    PI_1 = [40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25]

    SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    def __init__(self):
        self.key = None
        self.text = None
        self.keys = []

    def bit_array_to_string(self, array):
        res = ''.join([chr(int(y, 2)) for y in [''.join([str(x) for x in bytes]) for bytes in self.split_into_length(array, 8)]])
        return res

    def get_binary_value(self, val, bitsize):
        binary = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
        while len(binary) < bitsize:
            binary = '0' + binary
        return binary

    def string_to_bit_array(self, str):
        array = []
        for char in str:
            binval = self.get_binary_value(char, 8)
            for bit in list(binval):
                array.append(int(bit))
        return array

    def split_into_length(self, list, list_size): #make a list of size "n" from another list
        return [list[k:k + list_size] for k in range(0, len(list), list_size)]

    def sbox_substitute(self, to_substitute):
        splitted = self.split_into_length(to_substitute, 6)  # 6 bits
        results = []
        for i in range(len(splitted)):  # For all the sublists
            block = splitted[i]
            val = self.S_BOX[i][int(str(block[0]) + str(block[5]), 2)][int(''.join([str(x) for x in block[1:][:-1]]), 2)] # find the value from SBOX for proper row and column
            results += [int(x) for x in self.get_binary_value(val, 4)]
        return results

    def permutate(self, block, table):
        return [block[x - 1] for x in table]

    def xor(self, t1, t2):  # Xor on a whole list
        return [x ^ y for x, y in zip(t1, t2)]

    def shift(self, left, right, n):
        return left[n:] + left[:n], right[n:] + right[:n]

    def generate_keys(self):  # Algorithm that generates all the keys
        key = self.string_to_bit_array(self.key)
        key = self.permutate(key, self.CP_1)
        left, right = self.split_into_length(key, 28)  # Split it in to (g->LEFT),(d->RIGHT)
        for i in range(16):  # Apply the 16 rounds
            left, right = self.shift(left, right, self.SHIFT[i])  # Apply the shift associated with the round (not always 1)
            permutated_second_time = self.permutate(left + right, self.CP_2)
            self.keys.append(permutated_second_time)

    def encrypt(self, key, text, padding=False):
        return self.run(key, text, self.ENCRYPT, padding)

    def decrypt(self, key, text, padding=False):
        return self.run(key, text, self.DECRYPT, padding)

    def run(self, key, text, action=ENCRYPT, padding=False):
        if len(key) < 8:
            r = Tk()
            r.configure(bg=error)
            r.title('Blad')
            r.geometry('350x50')
            rlbl = Label(r, text='\n[!] Podales klucz krotszy niz 8 znakow')
            rlbl.pack()
            return
        if len(key) > 8:
            key = key[:8]

        self.key = key
        self.text = text

        if padding and action == self.ENCRYPT:
            pad_len = 8 - (len(self.text) % 8) # add padding
            self.text += pad_len * chr(pad_len)

        self.generate_keys()
        text_blocks = self.split_into_length(self.text, 8)  # split the input into 8-byte blocks (64bit)
        results = []
        for block in text_blocks:  # Loop over all the blocks of data
            block = self.permutate(self.string_to_bit_array(block), self.PI) # first permutation
            left, right = self.split_into_length(block, 32)  # g(LEFT), d(RIGHT)
            for i in range(16):  # Do the 16 rounds
                expanded_right = self.permutate(right, self.E)  # Expand right to match Ki size of 48bits by permutating using E
                if action == self.ENCRYPT:
                    tmp = self.xor(self.keys[i], expanded_right)  # If encrypt use Ki
                else:
                    tmp = self.xor(self.keys[15 - i], expanded_right)  # If decrypt start by the last key
                tmp = self.permutate(self.sbox_substitute(tmp), self.P)
                tmp = self.xor(left, tmp)
                left = right
                right = tmp
            results += self.permutate(right + left, self.PI_1)  # last permutation on what we received
        final_res = self.bit_array_to_string(results)
        if padding and action == self.DECRYPT:
            return final_res[:-ord(final_res[-1])] # remove padding
        else:
            return final_res

Menu()
