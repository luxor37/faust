#!/usr/bin/python

# this is faust
# This script has been provided by an unknown person and reworked/updated by another unknown person so guess what it
# mean for the copyright... there's NONE! Obviously you don't need to ask to use/rewrite/rework it or whatever

# pulls data to get all classes associated w/ everyprogram in a programme at uqam
# from https://etudier.uqam.ca/recherche-horaires
from datetime import datetime
import argparse
import sys
from faust_lib import Faust

import tkinter as tk
from tkinter import ttk

window_width = 600
window_height = 400


root = tk.Tk()
root.title('Faust')
# root.iconbitmap('./faust.ico')

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
# root.resizable(False, False)

# --- CONTENT ---

message = tk.Label(
    root, text="This is Faust\nThis program pulls data to get all courses associated w/ every program at UQAM")
message.pack(fill='x')

config_section = ttk.Frame(root)
config_section.pack(padx=10, pady=10, fill='x', expand=True, anchor=tk.N)

# ANNEE
programme = tk.StringVar()
programme.set("")

programme_label = ttk.Label(config_section, text="Programme (facultatif):")
programme_label.grid(column=0, row=0, sticky=tk.E)
programme_entry = ttk.Entry(config_section, textvariable=programme, width=5)
programme_entry.grid(column=1, row=0, columnspan=3, sticky=tk.W)
programme_entry.focus()

# ANNEE
annee = tk.StringVar()
annee.set(datetime.now().year)

annee_label = ttk.Label(config_section, text="Annee:")
annee_label.grid(column=0, row=1, sticky=tk.E)
annee_entry = ttk.Entry(config_section, textvariable=annee, width=5)
annee_entry.grid(column=1, row=1, columnspan=3, sticky=tk.W)

# SESSION
sessions = [
    {"id": 1, "title": "Hiver"},
    {"id": 2, "title": "Été"},
    {"id": 3, "title": "Automne"}]

selected_session = tk.StringVar()
selected_session.set("1")

session_label = ttk.Label(config_section, text="Session:")
session_label.grid(column=0, row=2, sticky=tk.E)

for j, session in enumerate(sessions):
    r = ttk.Radiobutton(
        config_section,
        text=session["title"],
        value=session["id"],
        variable=selected_session
    )
    r.grid(column=j+1, row=2, sticky=tk.W)

# POLITE CHECKBOX
polite = tk.StringVar()
polite.set(True)
polite_check = ttk.Checkbutton(config_section, text='Polite? (recommendé, mais plus long)', variable=polite, onvalue=True, offvalue=False)
polite_check.grid(column=1, row=3, columnspan=3, sticky=tk.E)

# LOGS
output_label = ttk.Label(root, text="Logs:")
output_label.pack()
output = tk.Text(root, height=8)
output.pack(fill='x')

#LOGIC AND BUTTON
def launchProgram():
    faust = Faust(annee.get()+selected_session.get(), output, polite.get(), programme.get())
    faust.get_schedule()

button = ttk.Button(root, text='Générer', command=lambda: launchProgram())
button.pack()

try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    if __name__ == '__main__':
        root.mainloop()
