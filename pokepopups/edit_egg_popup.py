import requests
import tkinter as tk
from tkinter import ttk, messagebox


class EditEggPopup(tk.Frame):
    """ Popup Frame to Add a Student """

    def __init__(self, parent, manager_id, member_id, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)
        self.config(background='indian red')
        self._text_bg = 'indian red'
        self._entry_bg = 'light sky blue'
        self._entry_fg = 'black'
        self._button_bg = 'light goldenrod'
        self._button_fg = 'black'
        self._button_select = 'hand2'

        self._manager_id = manager_id
        self._member_id = member_id

        self._close_cb = close_callback
        self.grid(rowspan=3, columnspan=2)
        tk.Label(self, text='Edit your Egg!', bg='indian red', fg='black').grid(row=1, column=1)

        tk.Label(self, text="New Nickname*:", bg=self._text_bg, fg='black').grid(row=2, column=1)
        self._nickname = tk.Entry(self, bg=self._entry_bg, fg=self._entry_fg)
        self._nickname.grid(row=2, column=2)

        tk.Label(self, text='*Required field', bg=self._text_bg, fg='black').grid(row=6, column=1)

        tk.Button(self, text="Submit", command=self._submit_cb, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select).grid(row=7, column=1)
        tk.Button(self, text="Close", command=self._close_cb, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select).grid(row=7, column=2)

    def _submit_cb(self):
        """ Submit the Add Student """
        data = dict()
        data['nickname'] = self._nickname.get()
        data['item'] = ''

        if self._validate_input(data['nickname']):
            return

        response = requests.put(f"http://127.0.0.1:5000/{self._manager_id}/member/{self._member_id}", json=data)

        if response.status_code == 204:
            messagebox.showinfo(title='Success',
                                message=f'Egg updated.')
            self._close_cb()
        else:
            messagebox.showerror(title='Unknown error', message=f'An unknown error occurred.')

    @staticmethod
    def _validate_input(name):
        if str(name) == '':
            messagebox.showerror(title='Input error', message='Field: New Nickname is required.')
            return True
        return False
