import tkinter as tk
from tkinter import ttk
import random
from PIL import ImageTk, Image
from Bots import Bots


class FiveOOneGame(tk.Tk):
    # TODO: difficulty level button must be pressed first now, should be initialised on 1
    # TODO : Initial picture
    # TODO : add bull option
    def __init__(self):
        super().__init__()

        self.title("501 Game")
        self.geometry("1200x1000")

        # Variables to store selected player, aimed at number, section, average throw, number of throws, score left, and difficulty level
        self.selected_player = tk.StringVar()

        self.aimed_at_number = tk.IntVar(value=1)
        self.aimed_at_section = tk.StringVar(value="TRIPLE")
        self.score_left = 501

        self.average_throw = tk.StringVar(value="0")
        self.num_throws = tk.StringVar(value="0")
        self.difficulty_level = tk.StringVar(value="1")
        self.players = {
            "Marnick": "graphics/profilepics/Marnick{0}.png".format(self.difficulty_level.get()),
            "Warre": "graphics/profilepics/{0}.png".format(self.difficulty_level.get()),
            "Jelle": "graphics/profilepics/{0}.png".format(self.difficulty_level.get())
        }

        # Create widgets
        ttk.Label(self, text="Select Player:").grid(row=0, column=0, padx=5, pady=5)
        self.player_combobox = ttk.Combobox(self, textvariable=self.selected_player, values=list(self.players.keys()))
        self.player_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.player_combobox.bind("<<ComboboxSelected>>", self.update_player_image)

        ttk.Label(self, text="").grid(row=0, column=3, rowspan=9,padx=5, pady=5)
        self.player_image_label = ttk.Label(self)
        self.player_image_label.grid(row=0, column=3,rowspan=9,padx=5, pady=5)

        ttk.Label(self, text="Aim at Number:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Scale(self, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.aimed_at_number, length=400,
                  command=self.update_aimed_number).grid(row=1, column=1, padx=5, pady=5)
        self.aimed_number_label = ttk.Label(self, textvariable=self.aimed_at_number)
        self.aimed_number_label.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(self, text="Aim at Section:").grid(row=2, column=0, padx=5, pady=5)
        section_frame = ttk.Frame(self)
        section_frame.grid(row=2, column=1, padx=5, pady=5)
        section_frame.columnconfigure(0, weight=1)
        self.single_button = ttk.Button(section_frame, text="SINGLE", command=lambda: self.set_section("UPPER SINGLE"))
        self.single_button.grid(row=0, column=0, sticky="ew", padx=2)
        self.double_button = ttk.Button(section_frame, text="DOUBLE", command=lambda: self.set_section("DOUBLE"))
        self.double_button.grid(row=0, column=1, sticky="ew", padx=2)
        self.triple_button = ttk.Button(section_frame, text="TRIPLE", command=lambda: self.set_section("TRIPLE"))
        self.triple_button.grid(row=0, column=2, sticky="ew", padx=2)
        self.triple_button.state(['pressed'])

        ttk.Label(self, text="Difficulty Level:").grid(row=3, column=0, padx=5, pady=5)
        difficulty_frame = ttk.Frame(self)
        difficulty_frame.grid(row=3, column=1, padx=5, pady=5)
        difficulty_frame.columnconfigure(0, weight=1)
        self.difficulty_1_button = ttk.Button(difficulty_frame, text="1", command=lambda: self.set_difficulty("1"))
        self.difficulty_1_button.grid(row=0, column=0, sticky="ew", padx=2)
        self.difficulty_2_button = ttk.Button(difficulty_frame, text="2", command=lambda: self.set_difficulty("0.75"))
        self.difficulty_2_button.grid(row=0, column=1, sticky="ew", padx=2)
        self.difficulty_3_button = ttk.Button(difficulty_frame, text="3", command=lambda: self.set_difficulty("0.5"))
        self.difficulty_3_button.grid(row=0, column=2, sticky="ew", padx=2)
        self.difficulty_4_button = ttk.Button(difficulty_frame, text="4", command=lambda: self.set_difficulty("0.25"))
        self.difficulty_4_button.grid(row=0, column=3, sticky="ew", padx=2)
        self.difficulty_5_button = ttk.Button(difficulty_frame, text="5", command=lambda: self.set_difficulty("0.10"))
        self.difficulty_5_button.grid(row=0, column=4, sticky="ew", padx=2)
        self.difficulty_6_button = ttk.Button(difficulty_frame, text="INSANE",
                                              command=lambda: self.set_difficulty("0.01"))
        self.difficulty_6_button.grid(row=0, column=5, sticky="ew", padx=2)

        ttk.Button(self, text="Throw", command=self.throw_dart).grid(row=5, columnspan=3, padx=5, pady=5)

        # Label to display the score left
        self.score_label = ttk.Label(self, text="Score Left: 501")
        self.score_label.grid(row=6, columnspan=3, padx=5, pady=5)

        # Label to display throw result
        self.throw_result_label = ttk.Label(self, text="")
        self.throw_result_label.grid(row=7, columnspan=3, padx=5, pady=5)

        ttk.Label(self, text="Average Throw:").grid(row=8, column=0, padx=5, pady=5)
        ttk.Label(self, textvariable=self.average_throw).grid(row=8, column=1, padx=5, pady=5)
        ttk.Label(self, text="Number of Throws:").grid(row=9, column=0, padx=5, pady=5)
        ttk.Label(self, textvariable=self.num_throws).grid(row=9, column=1, padx=5, pady=5)

        # Button to start over
        ttk.Button(self, text="Start Over", command=self.start_over).grid(row=10, columnspan=3, padx=5, pady=5)

        self.bot = Bots(self.selected_player.get(), self.difficulty_level.get())
        self.update_player_image()

    def update_aimed_number(self, value):
        # Round the value to the nearest integer
        self.aimed_at_number.set(round(float(value)))

    def set_section(self, section):
        # Update aimed at section
        self.aimed_at_section.set(section)

        # Highlight the selected button
        if section == "UPPER SINGLE":
            self.single_button.state(['pressed'])
            self.double_button.state(['!pressed'])
            self.triple_button.state(['!pressed'])
        elif section == "DOUBLE":
            self.single_button.state(['!pressed'])
            self.double_button.state(['pressed'])
            self.triple_button.state(['!pressed'])
        elif section == "TRIPLE":
            self.single_button.state(['!pressed'])
            self.double_button.state(['!pressed'])
            self.triple_button.state(['pressed'])

    def set_difficulty(self, difficulty):
        # Update difficulty level
        self.difficulty_level.set(difficulty)

        # Highlight the selected button
        for button in [self.difficulty_1_button, self.difficulty_2_button, self.difficulty_3_button,
                       self.difficulty_4_button, self.difficulty_5_button, self.difficulty_6_button]:
            button.state(['!pressed'])
        if difficulty == "1":
            self.difficulty_1_button.state(['pressed'])
            button = "1"
        elif difficulty == "0.75":
            self.difficulty_2_button.state(['pressed'])
            button = "2"
        elif difficulty == "0.5":
            self.difficulty_3_button.state(['pressed'])
            button = "3"
        elif difficulty == "0.25":
            self.difficulty_4_button.state(['pressed'])
            button = "4"
        elif difficulty == "0.10":
            self.difficulty_5_button.state(['pressed'])
            button = "5"
        elif difficulty == "0.01":
            self.difficulty_6_button.state(['pressed'])
            button = "6"

        self.bot = Bots(self.selected_player.get(), float(self.difficulty_level.get()))
        print("New difficulty " + str(self.difficulty_level.get()))

        self.players = {
            "Marnick": "graphics/profilepics/Marnick{0}.png".format(str(button)),
            "Warre": "graphics/profilepics/Warre{0}.png".format(str(button)),
            "Jelle": "graphics/profilepics/Jelle{0}.png".format(str(button))
        }
        self.update_player_image()

    def start_over(self):
        # Reset all values
        self.score_left = 501
        self.average_throw.set("0")
        self.num_throws.set("0")
        self.score_label.config(text="Score Left: 501")
        self.throw_result_label.config(text="")

    def update_player_image(self, event=None):
        # Update player image based on selected player
        player_name = self.selected_player.get()
        print(player_name)
        print(self.players)
        if player_name in self.players:
            image_path = self.players[player_name]
            try:
                print("lol")
                img = Image.open(image_path)
                img = img.resize((400, 400))
                player_image = ImageTk.PhotoImage(img)
                self.player_image_label.configure(image=player_image)
                self.player_image_label.image = player_image
            except FileNotFoundError:
                self.player_image_label.configure(image=None)

    def throw_dart(self):
        # Simulate throwing darts
        score, section = self.bot.throw(aimed_at_number=self.aimed_at_number.get(),
                                        aimed_at_section=self.aimed_at_section.get(),
                                        player=self.selected_player.get())
        # TODO AND DOUBLE
        if self.score_left == score:
            result_text = f"{self.selected_player.get()} threw {section} for {score} points and won the game."
            self.score_left -= score
        elif score + 1 >= self.score_left:
            result_text = f"{self.selected_player.get()} threw {section} for {score} points and busted."
        else:
            # Update the score left
            self.score_left -= score
            # Display the result of the throw
            result_text = f"{self.selected_player.get()} threw {section} for {score} points."
            # Update the score label
        self.score_label.config(text=f"Score Left: {self.score_left}")

        self.throw_result_label.config(text=result_text)

        # Update the number of throws
        self.num_throws.set(str(int(self.num_throws.get()) + 1))

        # Calculate average throw

        new_average = (501 - self.score_left) / int(self.num_throws.get())
        self.average_throw.set(f"{new_average:.2f}")


if __name__ == "__main__":
    app = FiveOOneGame()
    app.mainloop()
