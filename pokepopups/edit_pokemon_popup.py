import requests
import tkinter as tk
from tkinter import ttk, messagebox


class EditPokemonPopup(tk.Frame):
    """ Popup Frame to Add a Student """

    def __init__(self, parent, manager_id, member_id, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)

        self._manager_id = manager_id
        self._member_id = member_id

        self._close_cb = close_callback
        self.grid(rowspan=3, columnspan=2)
        ttk.Label(self, text='Edit your Pokemon!').grid(row=1, column=1)

        ttk.Label(self, text="New Nickname*:").grid(row=2, column=1)
        self._nickname = ttk.Entry(self)
        self._nickname.grid(row=2, column=2)

        ttk.Label(self, text="Held Item:").grid(row=3, column=1)
        self._item = ttk.Entry(self)
        self._item.grid(row=3, column=2)

        ttk.Label(self, text='*Required field').grid(row=4, column=1)

        ttk.Button(self, text="Submit", command=self._submit_cb).grid(row=5, column=1)
        ttk.Button(self, text="Close", command=self._close_cb).grid(row=5, column=2)

    def _submit_cb(self):
        """ Submit the Add Student """
        data = dict()
        data['nickname'] = self._nickname.get()
        data['item'] = self._item.get()

        if self._validate_input(data['nickname']):
            return

        response = requests.put(f"http://127.0.0.1:5000/{self._manager_id}/member/{self._member_id}", json=data)

        if response.status_code == 204:
            messagebox.showinfo(title='Success',
                                message=f'Pokemon updated.')
            self._close_cb()
        else:
            messagebox.showerror(title='Unknown error', message=f'An unknown error occurred.')

    @staticmethod
    def _validate_input(name):
        if str(name) == '':
            messagebox.showerror(title='Input error', message='Field: New Nickname is required.')
            return True
        return False
