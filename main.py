import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from board import Board
from dice import Dice
from player import Player
import json

class SnakesAndLaddersGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snakes and Ladders")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        
        self.players = []
        self.current_player_index = 0
        self.movements = []

        self.setup_main_menu()
        self.window.mainloop()

    def setup_main_menu(self):
        self.clear_window()
        tk.Label(self.window, text="Snakes and Ladders", font=("Arial", 24)).pack(pady=20)
        tk.Button(self.window, text="Start New Game", command=self.new_game, font=("Arial", 16)).pack(pady=10)
        tk.Button(self.window, text="Load Game", command=self.load_game, font=("Arial", 16)).pack(pady=10)
        tk.Button(self.window, text="Quit", command=self.window.quit, font=("Arial", 16)).pack(pady=10)

    def new_game(self):
        self.board = Board(size=100)
        self.num_players = self.get_num_players()
        self.players = [Player(f"Player {i + 1}") for i in range(self.num_players)]
        self.current_player_index = 0
        self.movements = []
        self.start_game()

    def get_num_players(self):
        while True:
            try:
                num = simpledialog.askstring("Input", "Enter number of players (2 or more):")
                if num is None:  # User pressed cancel
                    return
                num = int(num)  # Convert the input to an integer
                if num >= 2:
                    return num
                else:
                    messagebox.showerror("Error", "At least 2 players required.")
            except (ValueError, TypeError):
                messagebox.showerror("Error", "Invalid input. Please enter a number.")

    def start_game(self):
        self.clear_window()
        self.canvas = tk.Canvas(self.window, width=600, height=400, bg='white')
        self.canvas.pack()
        self.roll_button = tk.Button(self.window, text="Roll Dice", command=self.take_turn, font=("Arial", 16))
        self.roll_button.pack(pady=20)

        self.render_board()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def render_board(self):
        self.canvas.delete("all")
        rows, cols = 10, 10
        cell_size = 40
        
        for i in range(rows):
            for j in range(cols):
                x1 = j * cell_size
                y1 = (rows - i - 1) * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
        
        for snake_start, snake_end in self.board.snakes.items():
            pos = snake_start - 1
            x = (pos % cols) * cell_size + cell_size // 2
            y = (rows - (pos // cols) - 1) * cell_size + cell_size // 2
            self.canvas.create_line(x, y, x, y + 20, fill='red', width=2)
        
        for ladder_start, ladder_end in self.board.ladders.items():
            pos = ladder_start - 1
            x = (pos % cols) * cell_size + cell_size // 2
            y = (rows - (pos // cols) - 1) * cell_size + cell_size // 2
            self.canvas.create_line(x, y, x, y - 20, fill='green', width=2)

        for player in self.players:
            position = player.position
            player_x = (position - 1) % cols * cell_size + cell_size // 2
            player_y = (rows - (position - 1) // cols - 1) * cell_size + cell_size // 2
            self.canvas.create_oval(player_x - 10, player_y - 10, player_x + 10, player_y + 10, fill=player.color)

    def take_turn(self):
        if self.players[self.current_player_index].position == 100:
            messagebox.showinfo("Game Over", f"{self.players[self.current_player_index].name} already won!")
            return

        current_player = self.players[self.current_player_index]
        dice_roll = Dice().roll()
        self.movements.append(f"{current_player.name} rolled a {dice_roll}")
        self.update_player_position(current_player, dice_roll)
        
        if current_player.position == 100:
            messagebox.showinfo("Game Over", f"{current_player.name} wins!")

        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.render_board()

    def update_player_position(self, player, steps):
        new_position = player.position + steps

        if new_position in self.board.snakes:
            player.position = self.board.snakes[new_position]
            self.movements.append(f"{player.name} landed on a snake and moved to {player.position}.")
        elif new_position in self.board.ladders:
            player.position = self.board.ladders[new_position]
            self.movements.append(f"{player.name} climbed a ladder to {player.position}.")
        elif new_position > self.board.size:
            player.position = self.board.size - (new_position - self.board.size)
            self.movements.append(f"{player.name} overshot and moved to {player.position}.")
        else:
            player.position = new_position

    def load_game(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                game_data = json.load(file)
                self.current_player_index = game_data['current_player_index']
                self.players = [Player(name, position) for name, position in game_data['players']]
                self.movements = game_data['movements']
                self.render_board()
                messagebox.showinfo("Load Game", "Game loaded successfully!")

    def save_game(self):
        game_data = {
            'current_player_index': self.current_player_index,
            'players': [(player.name, player.position) for player in self.players],
            'movements': self.movements
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(game_data, file)
            messagebox.showinfo("Save Game", "Game saved successfully!")

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.quit()

if __name__ == "__main__":
    SnakesAndLaddersGame()
