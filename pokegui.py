"""
Dynamic GUI for the Pokemon Management System
Author: Nolan Crooks, Tushya Iyer

Assignment 4 - Python Object Oriented Programming ACIT2515
Date: 4/8/2020
"""

import tkinter as tk
import tkinter.font as font
from tkinter import ttk, messagebox, StringVar
import requests
import json
from ttkthemes import ThemedTk
from pokemodule.pokedex import Pokedex
from pokepopups.add_pokemon_popup import AddPokemonPopup
from pokepopups.add_egg_popup import AddEggPopup
from pokepopups.pokestats_popup import PokeStatsPopup
from pokepopups.edit_pokemon_popup import EditPokemonPopup
from pokepopups.edit_egg_popup import EditEggPopup
from pokepopups.new_hatches_popup import PokeHatchPopup


class MainAppController(ThemedTk):
    """ Main Application for GUI """

    _BASE_URL = "http://127.0.0.1:5000"

    def __init__(self):
        """ Initialize Main Application """
        ThemedTk.__init__(self, theme='ubuntu', themebg=True)
        self.geometry('580x650')
        self.resizable(False, False)
        self.config(background='indian red')
        self._widget_bg = 'gray14'
        self._text_bg = 'light sky blue'
        self._text_fg = 'RoyalBlue1'
        self._text_font = font.Font(size=12, weight='bold')
        self._button_bg = 'light goldenrod'
        self._button_fg = 'black'
        self._button_select = 'hand2'

        tk.Label(self, text='Choose Player', bg=self._widget_bg, fg='white').grid(row=0,column=3, pady=(30,0))
        # Top frame, row 1
        self._top_frame = tk.Frame(master=self, bg=self._widget_bg)
        self._top_frame.grid(row=1, column=2, padx=(40,0))

        # Left frame, column 1
        self._left_frame = tk.Frame(master=self, bg=self._widget_bg)
        self._left_frame.grid(row=2, column=2, padx=(40,0))

        # Right frame (info text, column 2)
        self._right_frame = tk.Frame(master=self, bg=self._widget_bg)
        self._right_frame.grid(row=2, column=3)

        # Under text frame
        self._under_frame = tk.Frame(master=self, bg=self._widget_bg)
        self._under_frame.grid(row=3, column=3)

        # Bottom frame
        self._bottom_frame = tk.Frame(master=self, bg=self._widget_bg)
        self._bottom_frame.grid(row=4, column=3)

        tk.Label(self._left_frame, text="Current Party:", bg=self._widget_bg, fg='white').grid(row=1, column=1, columnspan=3)
        self._party_list= tk.Listbox(self._left_frame, width=20, height=6, bg=self._text_bg, fg=self._text_fg, font=self._text_font)
        self._party_list.grid(row=2, column=1, columnspan=3)

        tk.Label(self._left_frame, text="PC Pokemon:", bg=self._widget_bg, fg='white').grid(row=4, column=1, columnspan=3)
        self._pc_list= tk.Listbox(self._left_frame, width=20, bg=self._text_bg, fg=self._text_fg, font=self._text_font)
        self._pc_list.grid(row=5, column=1, columnspan=3)

        # A couple buttons - using TTK
        tk.Button(self._left_frame, text="Move Member", command=self._move_member, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select).grid(row=6, column=1)
        tk.Button(self._left_frame, text="Create Member", command=self._create_member, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select).grid(row=6, column=3)
        tk.Button(self._left_frame, text="Player Stats", command=self._get_stats, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select).grid(row=7, column=1)
        tk.Button(self._left_frame, text="Release", command=self._release_member, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select).grid(row=7, column=3)
        tk.Button(self._left_frame, text="Quit", command=self._quit_callback, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select).grid(row=8, column=1, columnspan=3)

        # Right frame widgets
        tk.Label(self._right_frame, text='Member Info', bg=self._widget_bg, fg='white').grid(row=1, column=1, columnspan=3)
        self._info_text = tk.Text(master=self._right_frame, height=18.5, width=30, bg=self._text_bg, fg=self._text_fg, font=self._text_font)
        self._info_text.grid(row=2, column=2)
        self._disable_text_insert(self._info_text)

        # Under text frame widgets
        self._edit_btn = tk.Button(self._under_frame, text="Edit member", command=self._edit_member, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select)
        self._edit_btn.grid(row=2, column=1)
        self._walk_btn = tk.Button(self._under_frame, text="Walk", command=self._walk, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select)
        self._walk_btn.grid(row=2, column=2)

        # Create dropdown to choose manager
        managers = requests.get(f'{self._BASE_URL}/managers/all').json()
        self._managers = {m['player_name']:m for m in managers}

        self._dropdown_var = StringVar(self)
        self._dropdown_var.set(managers[0]['player_name'])

        tk.Button(self._top_frame, text="New Player", command=self._create_player, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select).grid(row=1, column=2)
        self._dropdown = tk.OptionMenu(self, self._dropdown_var, *self._managers, command=self._update_all)
        self._dropdown.config(background=self._button_bg, foreground=self._button_fg, activebackground='yellow', cursor=self._button_select)
        self._dropdown.grid(row=1, column=3)

        # Call this on select
        self._pc_list.bind("<<ListboxSelect>>", self._update_textbox)
        self._party_list.bind("<<ListboxSelect>>", self._update_textbox)

        # Now update all widgets
        self._update_all(None)

    def _update_all(self, event):
        """ Updates both lists and textbox for when manager changes """
        self._update_lists()
        self._update_dropdown()
        self._update_textbox(event)
        self._update_right_buttons()

    def _move_member(self):
        """ Moved selected member to party, or remove from party depending on their status"""
        member_id = self._get_member_id_from_list()
        if not member_id:
            messagebox.showerror(title='Select member', message='Please select a member to move.')
            return
        manager_id = self._get_manager_id()

        r = requests.put(f"{self._BASE_URL}/{manager_id}/{member_id}/move")

        if r.status_code == 400:
            messagebox.showerror(title='Error', message='Could not move member to party.')
            return
        if r.status_code == 401:
            messagebox.showerror(title='Party Full', message='Your party is full! Please remove a member from your party if you would like to add this member to your party.')
            return
        self._update_lists()

    def _release_member(self):
        """ Release selected member into the wild """

        member_id = self._get_member_id_from_list()
        if not member_id:
            messagebox.showerror(title='Select member', message='Please select a member to release.')
            return

        self._id_to_remove = member_id
        self._popup_win = tk.Toplevel()
        self._error_msg = ''
        self._popup_win.config(bg='indian red')
        tk.Label(self._popup_win, text=f'Are you sure you would like to release member {self._id_to_remove}?', bg=self._widget_bg, fg='white').grid(row=0)

        confirm = tk.Button(self._popup_win, text='I am sure', command=self._confirm_removal, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select)
        confirm.grid(row=1)

    def _confirm_removal(self):
        """ Confirms removal of member """
        manager_id = self._get_manager_id()

        if type(self._id_to_remove) is not str:
            self._error_msg = ttk.Label(self._popup_win, text='Member ID must be string.')
            self._error_msg.grid(row=2, column=1)
            return

        r = requests.delete(f"{self._BASE_URL}/{manager_id}/member/{self._id_to_remove}")
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

    def _create_player(self):
        """ CREATES NEW PLAYER!!! """
        self._popup_win = tk.Toplevel(bg='indian red')
        self._popup_win.geometry('250x90')
        self._popup_win.resizable(False, False)
        self._error_msg = ''

        self._popup_frame = tk.Frame(self._popup_win, bg='indian red')
        self._popup_frame.grid(row=1, column=1, padx=(10,0))

        tk.Label(self._popup_frame, text='Player Name', bg=self._widget_bg, fg='white').grid(row=0, column=1, padx=(10,0), pady=(10,0))
        self._new_player_name = tk.Entry(self._popup_frame, bg=self._text_bg, fg='black')
        self._new_player_name.grid(row=0, column=2, padx=(10,0), pady=(10,0))

        confirm = tk.Button(self._popup_frame, text='Create New Player', command=self._confirm_player, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select)
        confirm.grid(row=1, column=1,columnspan=2)

    def _confirm_player(self):
        """ Creates popup confirm if the new player is created or not """
        data = {'player_name': self._new_player_name.get()}
        r = requests.post(f'{self._BASE_URL}/create_manager', json=data)
        if r.status_code == 200:
            messagebox.showinfo(title='Success',
                                message=f'Player {self._new_player_name.get()} created. Choose your new player from the drop down menu "Choose Player"')
            self._update_dropdown()
            self._close_popup()
        elif r.status_code == 400 or r.status_code == 401:
            self._error_msg = tk.Label(self._popup_win,
                                        text=f'Please enter a name for your new player.', font=('Arial',10), bg='indian red', fg='white')
            self._error_msg.grid(row=3, column=1, columnspan=2)

    def _create_member(self):
        """ Creates popup to choose which type of member to create """
        self._popup_win = tk.Toplevel(bg='indian red')
        self._popup_win.geometry('150x100')
        self._popup_win.resizable(False, False)
        self._error_msg = ''
        options = ['Pokemon', 'Egg']

        tk.Label(self._popup_win, text='Choose type to create', bg=self._widget_bg, fg='white').grid(row=0, column=1)

        self._type_dropdown_var = StringVar(self)
        self._type_dropdown_var.set(options[0])
        self._type_to_create = tk.OptionMenu(self._popup_win, self._type_dropdown_var, *options)
        self._type_to_create.config(background=self._button_bg, foreground=self._button_fg, activebackground='yellow', cursor=self._button_select)
        self._type_to_create.grid(row=1, column=1)

        confirm = tk.Button(self._popup_win, text='Create', command=self._choose_popup, bg=self._button_bg, fg=self._button_fg, cursor=self._button_select)
        confirm.grid(row=2, column=1)

    def _choose_popup(self):
        """ Determines which popup to generate depending on the type dropdown value """
        self._close_popup()
        if self._type_dropdown_var.get() == 'Pokemon':
            self._add_pokemon()
        if self._type_dropdown_var.get() == 'Egg':
            self._add_egg()

    def _add_pokemon(self):
        """ Add Pokemon Popup """
        self._popup_win = tk.Toplevel()
        self._popup_win.resizable(False, False)
        self._popup = AddPokemonPopup(self._popup_win, self._get_manager_id(), self._close_popup)

    def _add_egg(self):
        """ Add Egg Popup """
        self._popup_win = tk.Toplevel()
        self._popup_win.resizable(False, False)
        self._popup = AddEggPopup(self._popup_win, self._get_manager_id(), self._close_popup)

    def _edit_member(self):
        """ Creates a popup to edit the selected member. """
        member_id = self._get_member_id_from_list()
        if not member_id:
            messagebox.showerror(title='Select member', message='Please select a member to edit.')
            return
        manager_id = self._get_manager_id()
        self._popup_win = tk.Toplevel()
        self._popup_win.resizable(False, False)

        if member_id[0] == 'p':
            self._popup = EditPokemonPopup(self._popup_win, manager_id, member_id, self._close_popup)
        if member_id[0] == 'e':
            self._popup = EditEggPopup(self._popup_win, manager_id, member_id, self._close_popup)

    def _get_stats(self):
        """ Pokestats Popup """
        r = requests.get(f"{self._BASE_URL}/{self._get_manager_id()}/stats")
        stats = r.json()

        self._popup_win = tk.Toplevel()
        self._popup_win.resizable(False, False)
        self._popup = PokeStatsPopup(stats, self._popup_win, self._close_popup)

    def _update_textbox(self, evt):
        """ Updates the info text box on the right, based on the current ID selected """
        self._update_right_buttons()
        member_id = self._get_member_id_from_list()
        if not member_id:
            self._info_text.insert(tk.END, "No Member selected!")
            return

        # Make some GET requests
        manager_id = self._get_manager_id()

        r = requests.get(f"{self._BASE_URL}/{manager_id}/member/{member_id}")

        # Clear the text box
        self._enable_text_insert(self._info_text)
        self._info_text.delete(1.0, tk.END)

        # Check the request status code
        if r.status_code != 200:
            self._info_text.insert(tk.END, "Error running the request!")
            return

        data = json.loads(r.text)
        self._generate_info(data)
        self._disable_text_insert(self._info_text)

    def _generate_info(self, data):
        """ Creates and inserts the info into the info text widget """
        if data['member_type'] == 'Pokemon':
            self._species = Pokedex[data['pokedex_num']][0]
            self._sprite = tk.PhotoImage(file=Pokedex[data['pokedex_num']][2])
            ordered_keys = [
                'nickname',
                'source',
                'date_acquired',
                'current_hp',
                'level',
                'attack',
                'defense',
                'speed',
                'moves',
                'height',
                'weight',
                'item',
                'ability'
            ]
        else:
            self._species = 'Egg'
            self._sprite = tk.PhotoImage(file='img/egg.png')
            ordered_keys = [
                'source',
                'date_acquired',
                'steps_remaining',
            ]

        self._info_text.image_create(tk.END, image=self._sprite)
        self._info_text.insert(tk.END, f'{self._species}\n')

        self._info_text.tag_configure('left', justify='left')
        for key in ordered_keys:
            if key == 'moves':
                moves_list = json.loads(data['moves'])
                moves_list = [move[0] for move in moves_list]
                self._info_text.insert(tk.END,
                                       f"{' '.join([c.strip() for c in key.split('_')]).capitalize()}:\n")
                self._info_text.insert(tk.END, f"   {moves_list[0]} | {moves_list[1]} | {moves_list[2]} | {moves_list[3]}\n")
            else:
                self._info_text.insert(tk.END, f"{' '.join([c.strip() for c in key.split('_')]).capitalize()}\t\t{data[key]}\n")
        self._info_text.tag_add('left', '1.0', 'end')

    def _close_popup(self):
        """ Close Generic Popup """
        self._popup_win.destroy()
        self._update_lists()

    def _quit_callback(self):
        """ Quit """
        self.quit()

    def _get_manager_id(self):
        """ Converts name in drop down menu to an Id """
        player = self._managers[self._dropdown_var.get()]

        if player:
            return player['id']
        else:
            messagebox.showerror(title="Player ID", message=f"No Player Selected")

    def _get_member_id_from_list(self):
        """ Gets the Id of the selected member in either the pc or party list """
        selected_values = self._party_list.curselection()
        print(1)
        if selected_values:
            selected_index = selected_values[0]
            member_id = self._party_list.get(selected_index)[0:5]

        else:
            selected_values = self._pc_list.curselection()

            if selected_values:
                selected_index = selected_values[0]
                member_id = self._pc_list.get(selected_index)[0:5]
            else:
                return None
        
        print(member_id)
        return member_id

    def _update_lists(self):
        """ Update the Lists"""
        manager_id = self._get_manager_id()

        r = requests.get(f"{self._BASE_URL}/{manager_id}/member/all")
        self._pc_list.delete(0, tk.END)
        self._party_list.delete(0, tk.END)
        for m in r.json():
            if m['in_party']:
                self._party_list.insert(tk.END, m['id'] + ' - ' + m['nickname'])
            else:
                self._pc_list.insert(tk.END, m['id'] + ' - ' + m['nickname'])

    def _update_right_buttons(self):
        """ Dynamically show certain buttons for when either a Pokemon or Egg is selected """
        member_id = self._get_member_id_from_list()
        try:

            self._dmg_btn.grid_forget()
            self._lvl_btn.grid_forget()
            self._heal_btn.grid_forget()
        except AttributeError:
            print('Attribute error handled. Dont even stress')

        if member_id:
            if member_id[0] == 'p':
                self._bottom_frame.config(background='indian red')
                self._lvl_btn = tk.Button(self._bottom_frame, text="Add XP", command=self._add_xp, bg=self._button_bg,
                                        fg=self._button_fg, cursor=self._button_select)
                self._lvl_btn.grid(row=4, column=0)
                self._dmg_btn = tk.Button(self._bottom_frame, text="Damage", command=self._damage, bg=self._button_bg,
                                        fg=self._button_fg, cursor=self._button_select)
                self._dmg_btn.grid(row=4, column=2)
                self._heal_btn = tk.Button(self._bottom_frame, text="Heal", command=self._heal, bg=self._button_bg,
                                        fg=self._button_fg, cursor=self._button_select)
                self._heal_btn.grid(row=4, column=3)


    def _heal(self):
        """ Heals the selected Pokemon and revives it if it was KO'd """
        member_id = self._get_member_id_from_list()
        if not member_id:
            messagebox.showerror(title='Select member', message='Please select a member to heal.')
            return
        manager_id = self._get_manager_id()

        # Check the pokemons KO status before healing
        poke_r = requests.get(f"{self._BASE_URL}/{manager_id}/member/{member_id}")
        ko_before = poke_r.json()['is_KO']

        # Heal the pokemon
        r = requests.put(f"{self._BASE_URL}/{manager_id}/member/{member_id}/heal")
        if r.status_code == 400:
            messagebox.showerror(title='Error', message='Member not found')

        # Update the textbox
        self._update_textbox(evt='')

        # Check to see if the pokemon was revived
        poke_r = requests.get(f"{self._BASE_URL}/{manager_id}/member/{member_id}")
        ko_after = poke_r.json()['is_KO']
        if ko_before != ko_after:
            messagebox.showinfo(title=f"{poke_r.json()['nickname']} was revived!", message=f'Nurse Joy healed your Pokemon back to health!')

    def _damage(self):
        """ Damages the selected Pokemon and KOs it if its hp reaches 0 """
        member_id = self._get_member_id_from_list()
        if not member_id:
            messagebox.showerror(title='Select member', message='Please select a member to damage.')
            return
        manager_id = self._get_manager_id()

        # Deal damage to the pokemon
        r = requests.put(f"{self._BASE_URL}/{manager_id}/member/{member_id}/damage")
        if r.status_code == 400:
            messagebox.showerror(title='Error', message='Member not found')

        # Update the textbox
        self._update_textbox(evt='')

        # Check to see if the pokemon was knocked out
        r = requests.get(f"{self._BASE_URL}/{manager_id}/member/{member_id}")
        if r.json()['is_KO']:
            messagebox.showinfo(title='KO!', message=f"{r.json()['nickname']} was knocked out!")

    def _add_xp(self):
        """ Adds xp to the selected Pokemon """
        member_id = self._get_member_id_from_list()
        if not member_id:
            messagebox.showerror(title='Select member', message='Please select a member to add xp.')
            return
        manager_id = self._get_manager_id()

        # Get the pokemon's level before adding XP
        poke_r = requests.get(f"{self._BASE_URL}/{manager_id}/member/{member_id}")
        lvl_before = poke_r.json()['level']

        # Add XP to the pokemon
        r = requests.put(f"{self._BASE_URL}/{manager_id}/member/{member_id}/add_xp")
        if r.status_code == 400:
            messagebox.showerror(title='Error', message='Member not found')

        # Update the textbox
        self._update_textbox(evt='')

        # Check to see if the pokemon leveled up
        poke_r = requests.get(f"{self._BASE_URL}/{manager_id}/member/{member_id}")
        lvl_after = poke_r.json()['level']
        if lvl_after != lvl_before:
            messagebox.showinfo(title='Level up!', message=f"{poke_r.json()['nickname']} leveled up to level {lvl_after}!")

    def _walk(self):
        player_id = self._get_manager_id()

        r = requests.get(f'{self._BASE_URL}/{player_id}/member/all/Pokemon')
        before_pokemon_ids = set([p['id'] for p in r.json()])

        requests.put(f"{self._BASE_URL}/{player_id}/walk")
        
        r = requests.get(f'{self._BASE_URL}/{player_id}/member/all/Pokemon')
        after_pokemon_ids = set([p['id'] for p in r.json()])

        print(before_pokemon_ids)
        print(after_pokemon_ids)

        self._update_lists()
        if not self._get_member_id_from_list():
            self._party_list.select_set(0)
            self._party_list.event_generate("<<ListboxSelect>>")

        new_pokemon = self._determine_new_pokemon(before_pokemon_ids, after_pokemon_ids)

        if new_pokemon:
            self._popup_win = tk.Toplevel()
            self._popup_win.resizable(False, False)
            self._popup = PokeHatchPopup(new_pokemon, self._popup_win, self._close_popup)
        

    def _determine_new_pokemon(self, p_before, p_after):
        new_pokemon_ids = list(p_before.symmetric_difference(p_after))

        if len(new_pokemon_ids) == 0:
            print("no new")
            return None
        
        player_id = self._get_manager_id()

        new_pokemon = []

        for id in new_pokemon_ids:
            r = requests.get(f'{self._BASE_URL}/{player_id}/member/{id}')
            new_pokemon.append(r.json())    
        return new_pokemon

    def _update_dropdown(self):
        """ Updates the Player dropdown menu """
        managers = requests.get(f'{self._BASE_URL}/managers/all').json()
        self._managers = {m['player_name']:m for m in managers}
        self._dropdown.destroy()
        self._dropdown = tk.OptionMenu(self, self._dropdown_var, *self._managers, command=self._update_all)
        self._dropdown.config(background=self._button_bg, foreground=self._button_fg, activebackground='yellow', cursor=self._button_select)
        self._dropdown.grid(row=1, column=3)

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
    root.mainloop()

