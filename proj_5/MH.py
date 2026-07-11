"""Project 5: The Monty Hall Problem
Kim Huynh, 2026-04-29, CS 211
"""

# credits: slides from class, https://brilliant.org/wiki/monty-hall-problem/

"""
MH.py

This module contains the implementation of the Monty Hall problem simulation. 
The Monty Hall problem is a probability puzzle based on a game show scenario. 
The simulation allows users to experiment with the problem, analyze the results, 
and visualize the probabilities of winning by switching or staying with the initial choice.
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class MH:
    """
    A class to simulate the Monty Hall problem and analyze the probabilities of winning 
    by switching or staying with the initially chosen door.

    Attributes:
        n_doors (int): The number of doors in the simulation (default is 3).
        n_trials (int): The total number of trials conducted.
        n_sw (int): The number of times the player switched doors.
        sw_w_n (int): The number of times the player switched doors and won.
        sw_w (list): The frequency of winning when switching doors over trials.
        st_w_n (int): The number of times the player stayed with the initial choice and won.
        st_w (list): The frequency of winning when staying with the initial choice over trials.
    """

    def __init__(self) -> None:
        """
        Initializes the MH class with default values for the Monty Hall problem simulation.
        """
        self.n_doors = 3
        self.n_trials = 0
        self.n_sw = 0
        self.sw_w_n = 0
        self.sw_w = []
        self.st_w_n = 0
        self.st_w = []

    def __str__(self) -> str:
        """
        Returns:
            str: A formatted string showing the current state of the simulation.
        """
        return (
            "MH problem\n"
            f"n_doors = {self.n_doors}\n"
            f"n_trials = {self.n_trials}\n"
            f"n_sw = {self.n_sw}\n"
            f"sw_w_n = {self.sw_w_n}\n"
            f"sw_w [{len(self.sw_w)}] = {self.sw_w}...\n"
            f"st_w_n = {self.st_w_n}\n"
            f"st_w [{len(self.st_w)}] = {self.st_w}..."
        )

    def update(self, switched, chosen, correct, sw_d, verbose=False):
        """
        Updates the simulation statistics after a single trial.

        Args:
            switched (int): The door chosen after switching.
            chosen (int): The initially chosen door.
            correct (int): The correct door with the prize.
            sw_d (bool): Whether the player decided to switch doors.
            verbose (bool, optional): If True, prints detailed information about the trial. Defaults to False.
        """
        self.n_trials += 1

        if verbose:
            print(f"correct = {correct}")
            print(f"chosen = {chosen}")
            print(f"switched_door = {switched}")
            print(f"n_trials = {self.n_trials}")

        if sw_d:
            self.n_sw += 1
            final_choice = switched

            if verbose:
                print("switching doors")
                print(f"no of times switching doors: {self.n_sw}")

            if final_choice == correct:
                self.sw_w_n += 1

                if verbose:
                    print("final choice is correct")
                    print(f"no of switch and win: {self.sw_w_n}")

        else:
            final_choice = chosen

            if verbose:
                print("not switching doors")

            if final_choice == correct:
                self.st_w_n += 1

                if verbose:
                    print("final choice is correct")
                    print(f"no of stay and win: {self.st_w_n}")

        if self.n_sw > 0:
            switch_freq = self.sw_w_n / self.n_sw
        else:
            switch_freq = 0.0

        n_stay = self.n_trials - self.n_sw

        if n_stay > 0:
            stay_freq = self.st_w_n / n_stay
        else:
            stay_freq = 0.0

        self.sw_w.append(switch_freq)
        self.st_w.append(stay_freq)

        if verbose:
            print(f"final choice: {final_choice}")
            print(f"freqs of switch and win: {self.sw_w}")
            print(f"freqs of stay and win: {self.st_w}")

    def trial(self, verbose=False):
        """
        Conducts a single trial of the Monty Hall problem.

        Args:
            verbose (bool, optional): If True, prints detailed information about the trial. Defaults to False.
        """
        correct = random.randint(1, self.n_doors)
        chosen = random.randint(1, self.n_doors)

        possible_goats = []

        for door in range(1, self.n_doors + 1):
            if door != correct and door != chosen:
                possible_goats.append(door)

        opened = random.choice(possible_goats)

        possible_switches = []

        for door in range(1, self.n_doors + 1):
            if door != chosen and door != opened:
                possible_switches.append(door)

        switched = random.choice(possible_switches)

        sw_d = random.choice([True, False])

        self.update(switched, chosen, correct, sw_d, verbose)

    def experiment(self, nt=10):
        """
        Conducts multiple trials of the Monty Hall problem.

        Args:
            nt (int, optional): Number of trials to conduct. Defaults to 10.
        """
        for _ in range(nt):
            self.trial()

    def animate(self):
        """
        Animates the probabilities of winning by switching or staying over multiple trials.

        Uses matplotlib's FuncAnimation to create a dynamic visualization of the probabilities.
        """
        fig, ax = plt.subplots()

        x = np.arange(1, self.n_trials + 1)

        ax.set_xlim(1, self.n_trials)
        ax.set_ylim(0, 1)
        ax.set_xlabel("n")
        ax.set_ylabel("prob")
        ax.set_title("Monty Hall Simulation")
        ax.grid(True)

        switch_line, = ax.plot([], [], label="switch")
        stay_line, = ax.plot([], [], label="no switch")

        ax.legend()

        def update_frame(frame):
            switch_line.set_data(x[:frame], self.sw_w[:frame])
            stay_line.set_data(x[:frame], self.st_w[:frame])
            return switch_line, stay_line

        ani = FuncAnimation(
            fig,
            update_frame,
            frames=len(x) + 1,
            interval=20,
            blit=True,
            repeat=False
        )

        plt.show()
        return ani

    def plot(self):
        """
        Plots the probabilities of winning by switching or staying over multiple trials.

        Uses matplotlib to create a static line plot of the probabilities.
        """
        x = np.arange(1, self.n_trials + 1)

        plt.figure()
        plt.plot(x, self.sw_w, label="switch")
        plt.plot(x, self.st_w, label="no switch")

        plt.xlabel("n")
        plt.ylabel("prob")
        plt.title("Monty Hall Simulation")
        plt.legend()
        plt.grid(True)

        plt.savefig("mh_1000.png")
        plt.show()

if __name__ == "__main__":
    random.seed(42)
    mh = MH()
    print(mh)                   # initial state (no trials yet)

    mh.trial(verbose=True)
    print(mh)                   # after 1 trial

    mh.trial(verbose=True)
    print(mh)                   # after 2 trials

    mh.trial(verbose=True)
    print(mh)                   # after 3 trials

    mh.experiment(5000)         # run many trials for convergence
    print(mh)                   # final state summary

    mh.plot()                   # static visualization
    mh.animate()                # animated visualization