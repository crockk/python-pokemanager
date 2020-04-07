import tkinter as tk
import tkinter.font
from tkinter import ttk, messagebox, StringVar
import requests
import re
import json
from ttkthemes import ThemedTk, THEMES


class MainAppController(ThemedTk):
    """ Main Application for GUI """

    _BASE_URL = "http://127.0.0.1:5000/"

    def __init__(self):
        """ Initialize Main Application """
        ThemedTk.__init__(self, themebg=True)
        self.geometry('900x550')

        # Top frame, row 1
        top_frame = tk.Frame(master=self)
        top_frame.grid(row=1, column=1)

        # Left frame, column 1
        left_frame = tk.Frame(master=self)
        left_frame.grid(row=2, column=1)

        # Right frame (info text, column 2)
        right_frame = tk.Frame(master=self)
        right_frame.grid(row=2, column=2)

        tk.Label(left_frame, text="Your Party:").grid(row=1, column=1, columnspan=3)
        self._party_list= tk.Listbox(left_frame, width=20, height=7)
        self._party_list.grid(row=2, column=1, columnspan=3)

        tk.Label(left_frame, text="PC Pokemon:").grid(row=4, column=1, columnspan=3)
        self._pc_list= tk.Listbox(left_frame, width=20)
        self._pc_list.grid(row=5, column=1, columnspan=3)

        # A couple buttons - using TTK
        ttk.Button(left_frame, text="Add to party", command=None).grid(row=6, column=1)
        ttk.Button(left_frame, text="Remove from party", command=None).grid(row=6, column=3)
        ttk.Button(left_frame, text="Player Stats", command=None).grid(row=7, column=1)
        ttk.Button(left_frame, text="Release", command=None).grid(row=7, column=3)
        ttk.Button(left_frame, text="Quit", command=self._quit_callback).grid(row=8, column=1, columnspan=3)

        # Right frame widgets
        self._info_text = tk.Text(master=right_frame, height=20, width=70, font=("TkTextFont", 10))
        self._info_text.grid(row=3, column=1, columnspan=2)
        self._info_text.tag_configure("bold", font=("TkTextFont", 10, "bold"))
        self._disable_text_insert(self._info_text)
        ttk.Button(right_frame, text="Edit member", command=None).grid(row=4, column=1, columnspan=3)

        # Create dropdown to choose manager
        managers = requests.get('http://127.0.0.1:5000/managers').json()
        self._managers = {m['player_name']:m for m in managers}

        self._dropdown_var = StringVar(self)
        self._dropdown_var.set(managers[0]['player_name'])

        tk.Label(top_frame, text="Player").grid(row=5, column=1)
        self._dropdown = tk.OptionMenu(self, self._dropdown_var, *self._managers, command=self._update_all)
        self._dropdown.grid(row=1, column=2)

        # Call this on select
        self._pc_list.bind("<<ListboxSelect>>", self._update_textbox)
        self._party_list.bind("<<ListboxSelect>>", self._update_textbox)

        # Now update the list
        self._update_lists()

    def _update_all(self, event):
        self._update_lists()
        self._update_textbox(event)

    # def _get_stats(self):
    #     r = requests.get("http://127.0.0.1:5000/school/stats")
    #     stats = r.json()
    #
    #     self._popup_win = tk.Toplevel()
    #     self._popup = StatsPopup(stats, self._popup_win, self._close_student_cb)
    #
    # def _remove_person(self):
    #     self._popup_win = tk.Toplevel()
    #     self._error_msg = ''
    #
    #     ttk.Label(self._popup_win, text='Student ID to remove ').grid(row=0)
    #
    #     self._id_to_remove = ttk.Entry(self._popup_win)
    #     confirm = ttk.Button(self._popup_win, text='Remove', command=self._confirm_removal)
    #
    #     self._id_to_remove.grid(row=0, column=1)
    #     confirm.grid(row=1, column=1)
    #
    # def _confirm_removal(self):
    #     if type(self._id_to_remove.get()) is not str:
    #         self._error_msg = ttk.Label(self._popup_win, text='Student ID must be string.')
    #         self._error_msg.grid(row=2, column=1)
    #         return
    #     if not re.match(r"^A\d+$", self._id_to_remove.get()):
    #         self._error_msg = ttk.Label(self._popup_win, text='Student ID must be in format: A00000000')
    #         self._error_msg.grid(row=2, column=1)
    #         return
    #
    #     response = requests.delete(f"http://127.0.0.1:5000/school/person/{self._id_to_remove.get()}")
    #     if response.status_code == 200:
    #         messagebox.showinfo(title='Success',
    #                             message=f'Student with ID: {self._id_to_remove.get()} has been successfully deleted.')
    #         self._close_popup()
    #     elif response.status_code == 400:
    #         self._error_msg = ttk.Label(self._popup_win,
    #                                     text=f'Student with ID: {self._id_to_remove.get()} does not exist.')
    #         self._error_msg.grid(row=2, column=1)
    #
    def _update_textbox(self, evt):
        """ Updates the info text box on the right, based on the current ID selected """

        # This is a list, so we take just the first item (could be multi select...)
        selected_values = self._party_list.curselection()
        if not selected_values:
            selected_values = self._pc_list.curselection()
            selected_index = selected_values[0]
            member_id = self._pc_list.get(selected_index)[0:5]
        else:
            selected_index = selected_values[0]
            member_id = self._party_list.get(selected_index)[0:5]
        print(member_id)

        # Make some GET requests
        manager_id = requests.get(f"http://127.0.0.1:5000/managers/{self._dropdown_var.get()[0]}")
        manager_id = manager_id.json()['id']

        r = requests.get(f"http://127.0.0.1:5000/{manager_id}/member/{member_id}")

        # Clear the text box
        self._enable_text_insert(self._info_text)
        self._info_text.delete(1.0, tk.END)

        # Check the request status code
        if r.status_code != 200:
            self._info_text.insert(tk.END, "Error running the request!")

        # For every item (key, value) in the JSON response, display them:
        for k, v in json.loads(r.text).items():
            self._info_text.insert(tk.END, f"{k}\t\t", "bold")
            self._info_text.insert(tk.END, f"{v}\n")

        self._disable_text_insert(self._info_text)
    #
    # def _quarantine_cb(self):
    #     selected_values = self._people_list.curselection()
    #     selected_index = selected_values[0]
    #     student_id = self._people_list.get(selected_index)
    #
    #     response = requests.put(f'http://127.0.0.1:5000/school/person/{student_id}/quarantine')
    #
    #     self._update_textbox(student_id)
    #     self._update_people_list()
    #
    # def _release_cb(self):
    #     selected_values = self._people_list.curselection()
    #     selected_index = selected_values[0]
    #     student_id = self._people_list.get(selected_index)
    #
    #     response = requests.put(f'http://127.0.0.1:5000/school/person/{student_id}/release')
    #
    #     self._update_textbox(student_id)
    #     self._update_people_list()
    #
    # def _add_student(self):
    #     """ Add Student Popup """
    #     self._popup_win = tk.Toplevel()
    #     self._popup = AddStudentPopup(self._popup_win, self._close_student_cb)
    #
    # def _close_student_cb(self):
    #     """ Close Add Student Popup """
    #     self._popup_win.destroy()
    #     self._update_people_list()
    #
    # def _add_teacher(self):
    #     """ Add Teacher Popup """
    #     self._popup_win = tk.Toplevel()
    #     self._popup = AddTeacherPopup(self._popup_win, self._close_teacher_cb)
    #
    # def _close_teacher_cb(self):
    #     """ Close Add Teacher Popup """
    #     self._popup_win.destroy()
    #     self._update_people_list()
    #
    # def _close_popup(self):
    #     """ Close Generic Popup """
    #     self._popup_win.destroy()
    #     self._update_people_list()
    #
    def _quit_callback(self):
        """ Quit """
        self.quit()
    #
    def _update_lists(self):
        """ Update the Lists"""
        id = self._managers[self._dropdown_var.get()]['id']
        manager_id = requests.get(f"http://127.0.0.1:5000/managers/{id}")
        manager_id = manager_id.json()['id']

        r = requests.get(f"http://127.0.0.1:5000/{manager_id}/member/all")
        self._pc_list.delete(0, tk.END)
        self._party_list.delete(0, tk.END)
        for m in r.json():
            if m['in_party']:
                self._party_list.insert(tk.END, m['id'] + ' - ' + m['nickname'])
            else:
                self._pc_list.insert(tk.END, m['id'] + ' - ' + m['nickname'])

    @staticmethod
    def _enable_text_insert(textbox):
        """ Toggles the textbox to allow insertion """
        textbox.config(state=tk.NORMAL)

    @staticmethod
    def _disable_text_insert(textbox):
        """ Toggles the textbox to not allow insertion """
        textbox.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = MainAppController()
    root.set_theme("ubuntu")
    root.mainloop()

