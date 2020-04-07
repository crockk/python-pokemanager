import requests
import tkinter as tk
from tkinter import ttk, messagebox
import re


class AddPokemonPopup(tk.Frame):
    """ Popup Frame to Add a Student """

    def __init__(self, parent, close_callback):
        """ Constructor """

        tk.Frame.__init__(self, parent)

        self._close_cb = close_callback
        self.grid(rowspan=2, columnspan=2)

        ttk.Label(self, text="Name:").grid(row=1, column=1)
        self._name = ttk.Entry(self, validate='key')
        self._name.grid(row=1, column=2)
        ttk.Label(self, text="Student ID:").grid(row=2, column=1)
        self._student_id = ttk.Entry(self)
        self._student_id.grid(row=2, column=2)
        ttk.Label(self, text="Program:").grid(row=3, column=1)
        self._program = ttk.Entry(self)
        self._program.grid(row=3, column=2)
        ttk.Button(self, text="Submit", command=self._submit_cb).grid(row=4, column=1)
        ttk.Button(self, text="Close", command=self._close_cb).grid(row=4, column=2)

    def _submit_cb(self):
        """ Submit the Add Student """
        data = {}
        data['name'] = self._name.get()
        data['student_id'] = self._student_id.get()
        data['program'] = self._program.get()

        if self._validate_inputs(data):
            return

        response = requests.post("http://127.0.0.1:5000/school/student", json=data)

        if response.status_code == 200:
            self._close_cb()
        else:
            messagebox.showerror(title='Unknown error', message=f'An unknown error occurred.')

    @staticmethod
    def _validate_inputs(data):
        empty_vals = [key for key, value in data.items() if str(value) == '']

        if len(empty_vals) == 1:
            empty_vals = ''.join(empty_vals).capitalize()
            messagebox.showerror(title='Missing fields', message=f'The following field is required: {empty_vals}')
            return True
        if len(empty_vals) > 1:
            empty_vals = ', '.join(empty_vals).capitalize()
            messagebox.showerror(title='Missing fields', message=f'The following fields are required: {empty_vals}')
            return True

        if not ''.join(data['name'].replace('.', '').split()).isalpha():
            messagebox.showerror(title='Input error', message='Field: "Name" accepts only alphabetical characters and periods.')
            return True

        if type(data['student_id']) is not str:
            messagebox.showerror(title='Input error', message='Field: "Student ID" must be string')
            return True
        if not re.match(r"^A\d+$", data['student_id']):
            messagebox.showerror(title='Input error', message='Field: "Student ID" must be in format: A00000000')
            return True

        if len(str(data['program'])) > 3 or not data['program'].isalpha():
            messagebox.showerror(title='Input error', message='Field: "Program" must be a 3 character, alphabetical string')
            return True

        return False
