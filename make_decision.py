# -*- coding: utf-8 -*-
"""
Author: Evan Jones.

Created on Fri Aug 20 08:43:30 2021

"""
import sys
import pandas as pd
from itertools import combinations
from random import shuffle
import tkinter
from tkinter import ttk

# Begin by creating an Agent class that will track how many times an Agent has won or lost:
class Agent():
    def __init__(self, name):
        self.name = name
        self.win_counter = 0
        self.loss_counter = 0
        self.draw_counter = 0
        self.play_counter = 0

    def __str__(self):
        return (f"{self.name} has:\n"
                f"\twon: {self.win_counter} times\n"
                f"\tlost: {self.loss_counter} times\n"
                f"\tdrew: {self.draw_counter} times\n"
                f"out of {self.play_counter} games.")

    def increment_win(self):
        self.win_counter += 1
        self.play_counter += 1

    def increment_loss(self):
        self.loss_counter += 1
        self.play_counter += 1

    def increment_draw(self):
        self.draw_counter += 1
        self.play_counter += 1


def match_iterator(projects):
    combos = list(combinations(projects, 2))
    for pair in combos:
        pair = list(pair)
        shuffle(pair)
    shuffle(combos)
    return iter(combos)


class RoundRobinApp():
    def __init__(self, projects):
        master = tkinter.Tk()
        # An iterator of matches
        self.matches = match_iterator(projects)
        self.A, self.B = next(self.matches)

        # Create a label with, spans 2 columns, in top left column & row.
        self.label = ttk.Label(master, text="Pick the one you prefer:")
        self.label.grid(row=0, column=0, columnspan=3)  # grid as opposed to pack

        # two buttons, that call the functions below to change the label's text.
        self.buttonA = ttk.Button(master, text=self.A.name, command=self.Awin)
        self.buttonA.grid(row=1, column=0)
        self.buttonB = ttk.Button(master, text=self.B.name, command=self.Bwin)
        self.buttonB.grid(row=1, column=2)

        self.buttonDraw = ttk.Button(master, text="Draw", command=self.draw_match)
        self.buttonDraw.grid(row=1, column=1)

        master.mainloop()

    def update_buttons(self):
        try:
            self.A, self.B = next(self.matches)
        except StopIteration:
            self.label.config(text="All finished! Please close this window to view your ranking.")
            self.buttonA.grid_forget()
            self.buttonB.grid_forget()
            self.buttonDraw.grid_forget()

        self.buttonA.config(text=self.A.name)
        self.buttonB.config(text=self.B.name)

    def Awin(self):
        self.A.increment_win()
        self.B.increment_loss()
        self.update_buttons()

    def Bwin(self):
        self.B.increment_win()
        self.A.increment_loss()
        self.update_buttons()

    def draw_match(self):
        self.A.increment_draw()
        self.B.increment_draw()
        self.update_buttons()


def main():
    if len(sys.argv) < 2:
        decision_names = ["First", "Second", "Third"]

    elif sys.argv[1] == "file":
        try:
            decision_names = pd.read_csv(sys.argv[2])
        except IndexError:
            raise IndexError("You have probably chosen file, but not passed a filename.")

    else:
        print("I hope you remembered to wrap each project name in quotes \" \"")
        decision_names = sys.argv[1:]

    decision_list = [Agent(name) for name in decision_names]

    # Run the app
    RoundRobinApp(decision_list)

    results = pd.DataFrame([{"name": decision.name,
                             "wins": decision.win_counter,
                             "draws": decision.draw_counter,
                             "losses": decision.loss_counter,
                             "plays": decision.play_counter}
                            for decision in decision_list])

    # Calculate the score, and print the ranking (in order)
    results["score"] = results["wins"] - results["losses"]
    results.sort_values("score", ascending=False, inplace=True)
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
