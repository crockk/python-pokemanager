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
        self.config(background='indian red')
        self._widget_bg = 'gray14'
        self._text_bg = 'light sky blue'
        self._text_fg = 'black'
        self._button_bg = 'light goldenrod'
        self._button_fg = 'black'
        self._button_select = 'hand2'

        self._close_cb = close_callback

        self._total_by_type = stats['total_by_type']
        self._total_eggs = stats['total_eggs']
        self._total_KO = stats['total_KO']
        self._total_steps = stats['total_steps']
        self._player_name = stats['player_name']

        w = tk.Label(self, text=f"Statistics for: {self._player_name}", bg='indian red', fg='black')
        w.pack(fill=X)
        w = tk.Label(self, text=f"Total KO'd: {self._total_KO}", bg=self._widget_bg, fg='white')
        w.pack(fill=X)
        w = tk.Label(self, text=f"Total steps walked: {self._total_steps}", bg=self._widget_bg, fg='white')
        w.pack(fill=X)
        w = tk.Label(self, text=f"Total eggs: {self._total_eggs}", bg=self._widget_bg, fg='white')
        w.pack(fill=X)
        w = tk.Label(self, text=f"Total by type:", bg=self._widget_bg, fg='white')
        w.pack(fill=X)

        text = tk.Text(self, width=20, height=5, font='Arial 8', bg=self._text_bg, fg=self._text_fg)
        text.tag_configure("center", justify='center')
        for type, num in self._total_by_type.items():
            text.insert("1.0", f'{type} type: {num}\n')
        text.tag_add("center", "1.0", "end")
        text.config(state=tk.DISABLED)
        text.pack(fill=X)

        w = tk.Button(self, text="Close", command=self._close_cb, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select)
        w.pack()


