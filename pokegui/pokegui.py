import tkinter as tk
import tkinter.font
from tkinter import ttk, messagebox
import requests
import re
from ttkthemes import ThemedTk, THEMES


class MainAppController(ThemedTk):
    """ Main Application for GUI """

    _BASE_URL = "http://127.0.0.1:5000/"

    def __init__(self):
        """ Initialize Main Application """
        ThemedTk.__init__(self, themebg=True)

        # Left frame, column 1
        left_frame = tk.Frame(master=self)
        left_frame.grid(row=1, column=1)

        # Right frame (info text, column 2)
        right_frame = tk.Frame(master=self)
        right_frame.grid(row=1, column=2)

        # Listbox for people
        tk.Label(left_frame, text="People list:").grid(row=1, column=1, columnspan=3)
        self._people_list = tk.Listbox(left_frame, width=20)
        self._people_list.grid(row=2, column=1, columnspan=3)
        # Call this on select
        self._people_list.bind("<<ListboxSelect>>", self._update_textbox)

        # A couple buttons - using TTK
        ttk.Button(left_frame, text="Add Student", command=self._add_student).grid(row=3, column=1)
        ttk.Button(left_frame, text="Add Teacher", command=self._add_teacher).grid(row=3, column=3)
        ttk.Button(left_frame, text="Quit", command=self._quit_callback).grid(row=4, column=1)
        ttk.Button(left_frame, text="Remove Person", command=self._remove_person).grid(row=4, column=3)
        ttk.Button(left_frame, text="School Stats", command=self._get_stats).grid(row=5, column=1)

        # Right frame widgets
        self._info_text = tk.Text(master=right_frame, height=10, width=40, font=("TkTextFont", 10))
        self._info_text.grid(row=1, column=1, columnspan=2, )
        self._info_text.tag_configure("bold", font=("TkTextFont", 10, "bold"))
        ttk.Button(right_frame, text="Quarantine", command=self._quarantine_cb).grid(row=2, column=1)
        ttk.Button(right_frame, text="Release", command=self._release_cb).grid(row=2, column=2)

        # Now update the list
        self._update_people_list()

    def _get_stats(self):
        r = requests.get("http://127.0.0.1:5000/school/stats")
        stats = r.json()

        self._popup_win = tk.Toplevel()
        self._popup = StatsPopup(stats, self._popup_win, self._close_student_cb)

    def _remove_person(self):
        self._popup_win = tk.Toplevel()
        self._error_msg = ''

        ttk.Label(self._popup_win, text='Student ID to remove ').grid(row=0)

        self._id_to_remove = ttk.Entry(self._popup_win)
        confirm = ttk.Button(self._popup_win, text='Remove', command=self._confirm_removal)

        self._id_to_remove.grid(row=0, column=1)
        confirm.grid(row=1, column=1)

    def _confirm_removal(self):
        if type(self._id_to_remove.get()) is not str:
            self._error_msg = ttk.Label(self._popup_win, text='Student ID must be string.')
            self._error_msg.grid(row=2, column=1)
            return
        if not re.match(r"^A\d+$", self._id_to_remove.get()):
            self._error_msg = ttk.Label(self._popup_win, text='Student ID must be in format: A00000000')
            self._error_msg.grid(row=2, column=1)
            return

        response = requests.delete(f"http://127.0.0.1:5000/school/person/{self._id_to_remove.get()}")
        if response.status_code == 200:
            messagebox.showinfo(title='Success',
                                message=f'Student with ID: {self._id_to_remove.get()} has been successfully deleted.')
            self._close_popup()
        elif response.status_code == 400:
            self._error_msg = ttk.Label(self._popup_win,
                                        text=f'Student with ID: {self._id_to_remove.get()} does not exist.')
            self._error_msg.grid(row=2, column=1)

    def _update_textbox(self, evt):
        """ Updates the info text box on the right, based on the current ID selected """

        # This is a list, so we take just the first item (could be multi select...)
        selected_values = self._people_list.curselection()
        selected_index = selected_values[0]
        student_id = self._people_list.get(selected_index)

        # Make a GET request
        r = requests.get("http://127.0.0.1:5000/school/person/" + student_id)

        # Clear the text box
        self._info_text.delete(1.0, tk.END)

        # Check the request status code
        if r.status_code != 200:
            self._info_text.insert(tk.END, "Error running the request!")

        # For every item (key, value) in the JSON response, display them:
        for k, v in r.json().items():
            self._info_text.insert(tk.END, f"{k.capitalize()}\t\t", "bold")
            self._info_text.insert(tk.END, f"{v}\n")

    def _quarantine_cb(self):
        selected_values = self._people_list.curselection()
        selected_index = selected_values[0]
        student_id = self._people_list.get(selected_index)

        response = requests.put(f'http://127.0.0.1:5000/school/person/{student_id}/quarantine')

        self._update_textbox(student_id)
        self._update_people_list()

    def _release_cb(self):
        selected_values = self._people_list.curselection()
        selected_index = selected_values[0]
        student_id = self._people_list.get(selected_index)

        response = requests.put(f'http://127.0.0.1:5000/school/person/{student_id}/release')

        self._update_textbox(student_id)
        self._update_people_list()

    def _add_student(self):
        """ Add Student Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddStudentPopup(self._popup_win, self._close_student_cb)

    def _close_student_cb(self):
        """ Close Add Student Popup """
        self._popup_win.destroy()
        self._update_people_list()

    def _add_teacher(self):
        """ Add Teacher Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddTeacherPopup(self._popup_win, self._close_teacher_cb)

    def _close_teacher_cb(self):
        """ Close Add Teacher Popup """
        self._popup_win.destroy()
        self._update_people_list()

    def _close_popup(self):
        """ Close Generic Popup """
        self._popup_win.destroy()
        self._update_people_list()

    def _quit_callback(self):
        """ Quit """
        self.quit()

    def _update_people_list(self):
        """ Update the List of People """
        r = requests.get("http://127.0.0.1:5000/school")
        self._people_list.delete(0, tk.END)
        for s in r.json()["people"]:
            self._people_list.insert(tk.END, s['student_id'])
            if s['type'] == "teacher":
                self._people_list.itemconfig(tk.END, {'fg': 'blue'})
            if s['quarantine']:
                self._people_list.itemconfig(tk.END, {'bg': 'red'})


if __name__ == "__main__":
    root = MainAppController()
    root.set_theme("ubuntu")
    root.mainloop()

