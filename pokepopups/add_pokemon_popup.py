import requests
import tkinter as tk
from tkinter import ttk, messagebox
import re


class AddPokemonPopup(tk.Frame):
    """ Popup Frame to Add a Pokemon """

    def __init__(self, parent, manager_id, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)

        self._manager_id = manager_id

        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        ttk.Label(self, text="Pokedex Number*:").grid(row=1, column=1)
        self._pokedex_num = ttk.Entry(self, validate='key')
        self._pokedex_num.grid(row=1, column=2)
        ttk.Label(self, text="Nickname:").grid(row=2, column=1)
        self._nickname = ttk.Entry(self)
        self._nickname.grid(row=2, column=2)
        ttk.Label(self, text="Source:").grid(row=3, column=1)
        self._source = ttk.Entry(self)
        self._source.grid(row=3, column=2)
        ttk.Label(self, text="Item:").grid(row=4, column=1)
        self._item = ttk.Entry(self)
        self._item.grid(row=4, column=2)
        ttk.Label(self, text="Ability:").grid(row=5, column=1)
        self._ability = ttk.Entry(self)
        self._ability.grid(row=5, column=2)

        ttk.Label(self, text='*Required field').grid(row=6, column=1)

        ttk.Button(self, text="Submit", command=self._submit_cb).grid(row=7, column=1)
        ttk.Button(self, text="Close", command=self._close_cb).grid(row=7, column=2)

    def _submit_cb(self):
        """ Submit the Add Student """
        data = {}
        data['pokedex_num'] = self._pokedex_num.get()
        data['nickname'] = self._nickname.get()
        data['source'] = self._source.get()
        data['item'] = self._item.get()
        data['ability'] = self._ability.get()

        if self._validate_input(data['pokedex_num']):
            return

        response = requests.post(f"http://127.0.0.1:5000/{self._manager_id}/pokemon", json=data)

        if response.status_code == 200:
            messagebox.showinfo(title='Success',
                                message=f'Pokemon successfully created.')
            self._close_cb()
        else:
            messagebox.showerror(title='Unknown error', message=f'An unknown error occurred.')

    @staticmethod
    def _validate_input(pokenum):
        if str(pokenum) == '':
            messagebox.showerror(title='Input error', message='Field: Pokedex Number is required.')
            return True

        try:
            pokenum = int(pokenum)
        except ValueError as err:
            messagebox.showerror(title='Input error', message='Field: Pokedex Number must be an integer between 1 and 10.')
            return True

        if pokenum > 10 or pokenum < 1:
            messagebox.showerror(title='Input error', message='Field: Pokedex Number must be between 1 and 10.')
            return True
        return False

        # empty_vals = [key for key, value in data.items() if str(value) == '']
        #
        # if len(empty_vals) == 1:
        #     empty_vals = ''.join(empty_vals).capitalize()
        #     messagebox.showerror(title='Missing fields', message=f'The following field is required: {empty_vals}')
        #     return True
        # if len(empty_vals) > 1:
        #     empty_vals = ', '.join(empty_vals).capitalize()
        #     messagebox.showerror(title='Missing fields', message=f'The following fields are required: {empty_vals}')
        #     return True
        #
        # if not ''.join(data['name'].replace('.', '').split()).isalpha():
        #     messagebox.showerror(title='Input error', message='Field: "Name" accepts only alphabetical characters and periods.')
        #     return True
        #
        # if type(data['student_id']) is not str:
        #     messagebox.showerror(title='Input error', message='Field: "Student ID" must be string')
        #     return True
        # if not re.match(r"^A\d+$", data['student_id']):
        #     messagebox.showerror(title='Input error', message='Field: "Student ID" must be in format: A00000000')
        #     return True
        #
        # if len(str(data['program'])) > 3 or not data['program'].isalpha():
        #     messagebox.showerror(title='Input error', message='Field: "Program" must be a 3 character, alphabetical string')
        #     return True