import requests
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import re
import string


class PokeHatchPopup(tk.Frame):

    def __init__(self, new_pokemon, parent, close_callback):

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

        w = tk.Label(self, text=f"You hatched new Pokemon!", bg='indian red', fg='black')
        w.pack(fill=X)

        for p in new_pokemon:
            w = tk.Label(self, text=f"Your egg {p['old_egg_id']} hatched into {p['nickname']}({p['id']})", bg=self._widget_bg, fg='white')
            w.pack(fill=X)

        w = tk.Button(self, text="Close", command=self._close_cb, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select)
        w.pack()


