import requests
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import re
import string


class StatsPopup(tk.Frame):

    def __init__(self, stats, parent, close_callback):

        tk.Frame.__init__(self, parent)
        self.pack()

        self._close_cb = close_callback

        self._num_quarantined_stu = stats['num_quarantined_students']
        self._num_quarantined_teach = stats['num_quarantined_teachers']
        self._total_people = stats['total_people']
        self._total_quarantined = stats['total_quarantined']
        self._num_students = stats['num_students']
        self._num_teachers = stats['num_teachers']
        self._name = stats['name']

        w = tk.Label(self, text=f"Statistics for: {self._name}", bg="gold", fg="black")
        w.pack(fill=X)
        w = tk.Label(self, text=f"Total people: {self._total_people}", bg="deep sky blue", fg="white")
        w.pack(fill=X)
        w = tk.Label(self, text=f"Number of students: {self._num_students}", bg="light sky blue", fg="white")
        w.pack(fill=X)
        w = tk.Label(self, text=f"Number of teachers: {self._num_teachers}", bg="light sky blue", fg="white")
        w.pack(fill=X)
        w = tk.Label(self, text=f"Total quarantined: {self._total_quarantined}", bg="red", fg="white")
        w.pack(fill=X)
        w = tk.Label(self, text=f"Number of quarantined students: {self._num_quarantined_stu}", bg="IndianRed1", fg="white")
        w.pack(fill=X)
        w = tk.Label(self, text=f"Number of quarantined teachers: {self._num_quarantined_teach}", bg="IndianRed1", fg="white")
        w.pack(fill=X)

        w = ttk.Button(self, text="Close", command=self._close_cb)
        w.pack(fill=X)


