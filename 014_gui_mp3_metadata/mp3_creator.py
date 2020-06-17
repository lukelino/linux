#! /usr/bin/python3
import tkinter as tk
from tkinter import filedialog as fd
import gui_mp3_metadata
import os


def main():
    window = tk.Tk()
    window.title('Set track number')
    directory = fd.askdirectory(initialdir='/')
    entry = tk.Entry(window, width=80)
    entry.insert(0, directory)
    entry.pack()
    for elem in os.listdir(directory):
        tk.Label(text=elem).pack()
    tk.Button(window, text="Start", command=lambda: gui_mp3_metadata.create_numbers(entry.get())).pack()
    tk.Button(window, text="Quit", command=lambda: window.destroy()).pack()
    window.mainloop()


if __name__ == '__main__':
    main()
