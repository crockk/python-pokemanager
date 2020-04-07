import tkinter as tk
import tkinter.font
from tkinter import ttk, messagebox, StringVar
import requests
import re
import json
from ttkthemes import ThemedTk, THEMES
from add_pokemon_popup import AddPokemonPopup
from add_egg_popup import AddEggPopup


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

        tk.Label(left_frame, text="Current Party:").grid(row=1, column=1, columnspan=3)
        self._party_list= tk.Listbox(left_frame, width=20, height=7)
        self._party_list.grid(row=2, column=1, columnspan=3)

        tk.Label(left_frame, text="PC Pokemon:").grid(row=4, column=1, columnspan=3)
        self._pc_list= tk.Listbox(left_frame, width=20)
        self._pc_list.grid(row=5, column=1, columnspan=3)

        # A couple buttons - using TTK
        ttk.Button(left_frame, text="Move Member", command=self._move_member).grid(row=6, column=1)
        ttk.Button(left_frame, text="Create Member", command=self._create_member).grid(row=6, column=3)
        ttk.Button(left_frame, text="Player Stats", command=None).grid(row=7, column=1)
        ttk.Button(left_frame, text="Release", command=self._release_member).grid(row=7, column=3)
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
        """ Updates both lists and textbox for when manager changes """
        self._update_lists()
        self._update_textbox(event)

    def _move_member(self):
        """ Moved selected member to party, or remove from party depending on their status"""
        member_id = self._get_member_id_from_list()
        manager_id = self._get_manager_id()

        r = requests.put(f"http://127.0.0.1:5000/{manager_id}/{member_id}/move")

        self._update_lists()

    def _release_member(self):
        """ Release selected member into the wild """
        self._popup_win = tk.Toplevel()
        self._error_msg = ''
        self._id_to_remove = self._get_member_id_from_list()

        ttk.Label(self._popup_win, text=f'Are you sure you would like to release member {self._id_to_remove}?').grid(row=0)

        confirm = ttk.Button(self._popup_win, text='I am sure', command=self._confirm_removal)
        confirm.grid(row=1)

    def _confirm_removal(self):
        """ Confirms removal of member """
        manager_id = self._get_manager_id()

        if type(self._id_to_remove) is not str:
            self._error_msg = ttk.Label(self._popup_win, text='Member ID must be string.')
            self._error_msg.grid(row=2, column=1)
            return

        r = requests.delete(f"http://127.0.0.1:5000/{manager_id}/member/{self._id_to_remove}")
        if r.status_code == 204:
            messagebox.showinfo(title='Success',
                                message=f'Member with ID: {self._id_to_remove} has been released into the wild.')
            self._close_popup()
        elif r.status_code == 400:
            self._error_msg = ttk.Label(self._popup_win,
                                        text=f'Member with ID: {self._id_to_remove} does not exist.')
            self._error_msg.grid(row=2, column=1)
        elif r.status_code == 401:
            self._error_msg = ttk.Label(self._popup_win,
                                        text=f'Member with ID: {self._id_to_remove} could not be released (It has become too attached to you).')
            self._error_msg.grid(row=2, column=1)

    def _create_member(self):
        """ Creates popup to choose which type of member to create """
        self._popup_win = tk.Toplevel()
        self._popup_win.geometry('150x100')
        self._error_msg = ''
        options = ['Pokemon', 'Egg']

        ttk.Label(self._popup_win, text='Choose type to create').grid(row=0, column=1)

        self._type_dropdown_var = StringVar(self)
        self._type_dropdown_var.set(options[0])
        self._type_to_create = tk.OptionMenu(self._popup_win, self._type_dropdown_var, *options)
        self._type_to_create.grid(row=1, column=1)

        confirm = ttk.Button(self._popup_win, text='Create', command=self._choose_popup)
        confirm.grid(row=2, column=1)

    def _choose_popup(self):
        """ Determines which popup to generate depending on the type dropdown value """
        self._close_popup()
        if self._type_dropdown_var.get() == 'Pokemon':
            self._add_pokemon()
        if self._type_dropdown_var.get() == 'Egg':
            self._add_egg()

    def _add_pokemon(self):
        print('pokemon create')
        """ Add Student Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddPokemonPopup(self._popup_win, self._close_popup)
        pass

    def _add_egg(self):
        print('egg create')
        """ Add Student Popup """
        self._popup_win = tk.Toplevel()
        self._popup = AddEggPopup(self._popup_win, self._close_popup)
        pass

    # def _get_stats(self):
    #     r = requests.get("http://127.0.0.1:5000/school/stats")
    #     stats = r.json()
    #
    #     self._popup_win = tk.Toplevel()
    #     self._popup = StatsPopup(stats, self._popup_win, self._close_student_cb)
    #

    def _update_textbox(self, evt):
        """ Updates the info text box on the right, based on the current ID selected """
        member_id = self._get_member_id_from_list()

        # Make some GET requests
        manager_id = self._get_manager_id()

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

    def _close_popup(self):
        """ Close Generic Popup """
        self._popup_win.destroy()
        self._update_lists()

    def _quit_callback(self):
        """ Quit """
        self.quit()

    def _get_manager_id(self):
        id = self._managers[self._dropdown_var.get()]['id']
        manager_id = requests.get(f"http://127.0.0.1:5000/managers/{id}")
        manager_id = manager_id.json()['id']
        return manager_id

    def _get_member_id_from_list(self):
        selected_values = self._party_list.curselection()
        if not selected_values:
            selected_values = self._pc_list.curselection()
            selected_index = selected_values[0]
            member_id = self._pc_list.get(selected_index)[0:5]
        else:
            selected_index = selected_values[0]
            member_id = self._party_list.get(selected_index)[0:5]
        print(member_id)
        return member_id

    def _update_lists(self):
        """ Update the Lists"""
        manager_id = self._get_manager_id()

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
