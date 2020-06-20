#! /usr/bin/python3

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from mutagen.id3 import ID3
import os
import sys
import re


class MetaDataSetter(tk.Frame):
    """Main engine"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.directory = tk.StringVar()     # Stores path to mp3 files
        self.check_dir = tk.StringVar()
        self.path_track = tk.StringVar()    #
        self.ending = tk.StringVar()        # mp3, FLAC
        self.endings = ['mp3', 'FLAC', 'wav']
        self.audio_files = []
        self.files_metadata_dct = {}
        self.tmp = []
        self.full_title_list = []
        self.counter = 0

        info_btn = ttk.Button(self, text='Info', command=self.get_info)
        directory_label = ttk.Label(self, text='Directory ')
        directory_entry = ttk.Entry(self, textvariable=self.directory)
        search_btn = ttk.Button(self, text='Search', command=self.search_dir)
        choose_box_txt = ttk.Label(self, text='File type ')
        choose_box = ttk.Combobox(self, textvariable=self.ending, values=self.endings)
        set_tracks_btn = ttk.Button(self, text='Set tracks', command=self.set_tracks)
        self.text_window = tk.Text(self, width=68, height=23)

        ttk.Label(self, text='').grid(row=0)
        info_btn.grid(row=1, column=0, columnspan=3)
        ttk.Label(self, text='').grid(row=2)
        directory_label.grid(row=3, column=0, sticky=tk.W)
        directory_entry.grid(row=3, column=1, sticky=(tk.W + tk.E))
        search_btn.grid(row=3, column=2, sticky=tk.E)
        choose_box_txt.grid(row=4, column=0, sticky=tk.W)
        choose_box.grid(row=4, column=1, sticky=tk.W)
        ttk.Label(self, text='').grid(row=5)
        set_tracks_btn.grid(row=6, column=0, columnspan=3)
        ttk.Label(self, text='').grid(row=7)
        self.text_window.grid(row=8, column=0, columnspan=3)
        self.columnconfigure(1, weight=1)

    @staticmethod
    def get_info():
        txt = 'Riot enables to set track numbers from its metadata\n\n2020 Łukasz Nawrot'
        mb.showinfo('Riot Info', txt)

    def search_dir(self):
        self.directory.set(fd.askdirectory(initialdir='/'))
        self.text_window.insert('end', self.directory.get())
        for file in os.listdir(self.directory.get()):
            self.text_window.insert('end', f'{file}\n')     # Prints chosen directory - files with no numbers
        self.text_window.insert('end', '\n')

    def set_tracks(self):
        """"""
        self.get_audio_files()
        if self.directory.get():
            self.create_dct_num_title()
            self.tmp_track_list()
            self.create_full_title_list()
        else:
            mb.showerror('Riot', 'Don\'t forget to choose directory first')

    def get_audio_files(self):
        if self.ending.get() and self.directory.get():
            all_files = [files for files in os.listdir(self.directory.get()) if files.endswith(self.ending.get())]
            # Create path to each audio file -- mp3 or others
            for elem in all_files:
                self.audio_files.append(os.path.join(self.directory.get(), elem))
        else:
            self.counter = 0

    def create_dct_num_title(self):
        # Find numbers
        pattern = re.compile(r"""^(\d{1,3})""")  # one, two, three or more digits
        # Take track number and create dictionary NUM:TITLE
        strange_symbol_pattern = re.compile(r"""(\*)*""")  # If '*' in metadata
        if self.audio_files:
            for f in self.audio_files:
                audio = ID3(f)
                digit = pattern.search(audio['TRCK'].text[0])  # Fit the pattern
                if int(digit.group()) in self.files_metadata_dct.keys():  # If the same track number appears again
                    # print(f'Nadpisanie utworu {digit.group()}.\nSprawdź poprawność i ilość plików.')
                    mb.showerror('Riot', f'Overwritten track {digit.group()}\nCheck files')
                    sys.exit()
                new_audio = strange_symbol_pattern.sub('', audio['TIT2'].text[0])  # Delete all '*'
                self.files_metadata_dct.setdefault(int(digit.group()), new_audio)
        else:
            mb.showerror('Riot', 'Choose correct audio type')
            self.counter = 0

    def tmp_track_list(self):
        """list [track_Num, Title]"""
        for k, v in self.files_metadata_dct.items():
            if int(k) < 10:
                self.tmp.append('0' + str(k))
                self.tmp.append(v)
            else:
                self.tmp.append(str(k))
                self.tmp.append(v)

    def create_full_title_list(self):
        self.full_title_list = [i + ' ' + j + '.' + self.ending.get() for i, j in zip(self.tmp[0::2], self.tmp[1::2])]
        for i, elem in enumerate(self.audio_files):
            # print(f'{elem}', ' --> ', f'{path}\\{full_title_list[i]}')
            self.path_track.set(f'{self.directory}\\{self.full_title_list[i]}')
            self.text_window.insert('end', self.path_track.get()[8:])
            self.text_window.insert('end', '\n')
            os.rename(elem, os.path.join(self.directory.get(), self.full_title_list[i]))
            self.counter += 1
        if self.counter > 0 and self.counter == len(self.audio_files):
            self.text_window.insert('end', f'\n{self.counter} file(s) created')
            mb.showinfo('Riot', f'Finished!\n{self.counter} files created')


class Application(tk.Tk):
    """Initialize object"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Riot')
        self.geometry('600x600')
        self.resizable(width=False, height=False)

        MetaDataSetter(self).grid(sticky=(tk.E + tk.W + tk.N + tk.S))
        self.columnconfigure(0, weight=1)


app = Application()
app.mainloop()
