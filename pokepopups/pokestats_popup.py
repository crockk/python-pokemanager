import requests
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import re
import string


class PokeStatsPopup(tk.Frame):

    def __init__(self, stats, parent, close_callback):

        tk.Frame.__init__(self, parent)
        self.pack()

        self._close_cb = close_callback

        self._total_by_type = stats['total_by_type']
        self._total_eggs = stats['total_eggs']
        self._total_KO = stats['total_KO']
        self._total_steps = stats['total_steps']
        self._player_name = stats['player_name']

        w = tk.Label(self, text=f"Statistics for: {self._player_name}", bg="snow3", fg="black")
        w.pack(fill=X)
        w = tk.Label(self, text=f"Total KO'd: {self._total_KO}", bg="pink2", fg="black")
        w.pack(fill=X)
        w = tk.Label(self, text=f"Total steps walked: {self._total_steps}", bg="pink2", fg="black")
        w.pack(fill=X)
        w = tk.Label(self, text=f"Total eggs: {self._total_eggs}", bg="pink2", fg="black")
        w.pack(fill=X)
        w = tk.Label(self, text=f"Total by type:", bg="pink2", fg="black")
        w.pack(fill=X)

        text = tk.Text(self, width=20, height=5, font='Arial 8')
        text.tag_configure("center", justify='center')
        for type, num in self._total_by_type.items():
            text.insert("1.0", f'{type} type: {num}\n')
        text.tag_add("center", "1.0", "end")
        text.config(state=tk.DISABLED)
        text.pack(fill=X)

        w = ttk.Button(self, text="Close", command=self._close_cb)
        w.pack()


