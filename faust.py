#!/usr/bin/python

# this is faust
# This script has been provided by an unknown person and reworked/updated by another unknown person so guess what it
# mean for the copyright... there's NONE! Obviously you don't need to ask to use/rewrite/rework it or whatever

# pulls data to get all classes associated w/ everyprogram in a programme at uqam
# from https://etudier.uqam.ca/recherche-horaires
from datetime import datetime
import argparse
from faust_lib import get_schedule

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
annee = tk.StringVar()
annee.set(datetime.now().year)

annee_label = ttk.Label(config_section, text="Annee:")
annee_label.grid(column=0, row=0, sticky=tk.W)
annee_entry = ttk.Entry(config_section, textvariable=annee, width=5)
annee_entry.grid(column=1, row=0, columnspan=3, sticky=tk.W)
annee_entry.focus()

# SESSION
sessions = [
    {"id": 1, "title": "Hiver"},
    {"id": 2, "title": "Ete"},
    {"id": 3, "title": "Automne"}]

selected_session = tk.StringVar()
selected_session.set("1")

session_label = ttk.Label(config_section, text="Session:")
session_label.grid(column=0, row=1, sticky=tk.W)

for j, session in enumerate(sessions):
    r = ttk.Radiobutton(
        config_section,
        text=session["title"],
        value=session["id"],
        variable=selected_session
    )
    r.grid(column=j+1, row=1, sticky=tk.W)

button = ttk.Button(root, text='Click Me', command=lambda: get_schedule(
    annee.get()+selected_session.get()))
button.pack()

try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         '-o', '--output', default=CSV_FILE_NAME, help="Fichier CVS")
#     parser.add_argument('-r', dest='refresh', action='store_true',
#                         help="Pour retelecharger les horaire à jour")
#     args = parser.parse_args()

#     get_schedule(args.output, args.refresh)
