"""HW 5: Monty Python with N doors
Kim Huynh, 2026-04-29, CS 211
"""

# credits: monty hall problem slides from class

import random
import matplotlib.pyplot as plt

class MontyHall:
    def __init__(self, num_doors: int):
        if num_doors < 3:
            raise ValueError("Number of doors must be at least 3.")

        self.num_doors = num_doors

    def play_stay(self) -> bool:
        doors = list(range(self.num_doors))

        car = random.choice(doors)
        player_choice = random.choice(doors)

        return player_choice == car

    def play_switch(self) -> bool:
        doors = list(range(self.num_doors))

        car = random.choice(doors)
        player_choice = random.choice(doors)

        # host opens n - 2 goat doors that are not the player's choice
        possible_doors_to_open = [
            door for door in doors
            if door != player_choice and door != car
        ]

        opened_doors = random.sample(possible_doors_to_open, self.num_doors - 2)

        # remaining unopened door is the switch choice
        remaining_doors = [
            door for door in doors
            if door != player_choice and door not in opened_doors
        ]

        switch_choice = remaining_doors[0]

        return switch_choice == car

    def run_simulation(self, trials: int):
        stay_wins = 0
        switch_wins = 0

        stay_results = []
        switch_results = []

        for trial in range(1, trials + 1):
            if self.play_stay():
                stay_wins += 1

            if self.play_switch():
                switch_wins += 1

            stay_results.append(stay_wins / trial)
            switch_results.append(switch_wins / trial)

        return stay_results, switch_results

    def plot_results(self, trials: int):
        stay_results, switch_results = self.run_simulation(trials)

        plt.figure()
        plt.plot(stay_results, label="Stay")
        plt.plot(switch_results, label="Switch")

        plt.title(f"Monty Hall Simulation with {self.num_doors} Doors")
        plt.xlabel("Number of Trials")
        plt.ylabel("Winning Probability")
        plt.legend()
        plt.grid(True)

        filename = f"plot_{self.num_doors}.jpg"
        plt.savefig(filename)
        plt.close()

        print(f"Saved {filename}")
        print(f"Final stay probability: {stay_results[-1]:.4f}")
        print(f"Final switch probability: {switch_results[-1]:.4f}")
        print()

def main():
    trials = 5000
    door_options = [3, 5, 10, 25, 50, 100]

    for num_doors in door_options:
        game = MontyHall(num_doors)
        game.plot_results(trials)

if __name__ == "__main__":
    main()