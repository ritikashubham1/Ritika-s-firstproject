import tkinter as tk
import random

# ---------------- GAME SETTINGS ---------------- #
BOARD_SIZE = 10
CELL_SIZE = 50
OFFSET = CELL_SIZE // 2

# Snakes and Ladders
snakes = {
    16: 6,
    48: 30,
    64: 60,
    79: 19,
    93: 68,
    95: 24,
    98: 78
}

ladders = {
    1: 38,
    4: 14,
    9: 31,
    21: 42,
    28: 84,
    51: 67,
    72: 91,
    80: 99
}


class SnakeAndLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Snakes and Ladders 🪜")
        self.root.resizable(False, False)

        self.player_pos = 1
        self.positions = {}

        # Title
        tk.Label(
            root,
            text="🐍 SNAKES AND LADDERS 🪜",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Canvas
        self.canvas = tk.Canvas(
            root,
            width=BOARD_SIZE * CELL_SIZE,
            height=BOARD_SIZE * CELL_SIZE,
            bg="white"
        )
        self.canvas.pack()

        # Status Label
        self.status_label = tk.Label(
            root,
            text="🎲 Click Roll Dice to Start!",
            font=("Arial", 12, "bold")
        )
        self.status_label.pack(pady=10)

        # Dice Button
        self.roll_button = tk.Button(
            root,
            text="🎲 Roll Dice",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            command=self.play_turn
        )
        self.roll_button.pack(pady=5)

        # Build Board
        self.generate_coordinates()
        self.draw_board()
        self.draw_snakes_and_ladders()
        self.create_player()

    def generate_coordinates(self):
        """Generate coordinates for each square."""
        number = 1

        for row in range(9, -1, -1):
            if (9 - row) % 2 == 0:
                cols = range(10)
            else:
                cols = range(9, -1, -1)

            for col in cols:
                x = col * CELL_SIZE + OFFSET
                y = row * CELL_SIZE + OFFSET
                self.positions[number] = (x, y)
                number += 1

    def draw_board(self):
        """Draw board squares."""
        for number, (cx, cy) in self.positions.items():
            x1 = cx - OFFSET
            y1 = cy - OFFSET
            x2 = cx + OFFSET
            y2 = cy + OFFSET

            color = "#FFFACD" if number % 2 == 0 else "#E6F7FF"

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="black"
            )

            self.canvas.create_text(
                x1 + 5,
                y1 + 5,
                text=str(number),
                anchor="nw",
                font=("Arial", 8)
            )

    def draw_snakes_and_ladders(self):
        """Draw snakes and ladders."""

        # Ladders
        for start, end in ladders.items():
            x1, y1 = self.positions[start]
            x2, y2 = self.positions[end]

            self.canvas.create_line(
                x1, y1,
                x2, y2,
                fill="green",
                width=5,
                dash=(5, 3),
                arrow=tk.LAST
            )

        # Snakes
        for start, end in snakes.items():
            x1, y1 = self.positions[start]
            x2, y2 = self.positions[end]

            self.canvas.create_line(
                x1, y1,
                x2, y2,
                fill="red",
                width=5,
                arrow=tk.LAST,
                smooth=True
            )

    def create_player(self):
        """Create player token."""
        x, y = self.positions[1]

        self.player = self.canvas.create_oval(
            x - 15,
            y - 15,
            x + 15,
            y + 15,
            fill="blue",
            outline="black",
            width=2
        )

    def animate_step(self, current, target):
        """Animate player movement."""

        if current == target:
            self.player_pos = target
            self.check_special_square()
            return

        next_pos = current + 1 if current < target else current - 1

        x, y = self.positions[next_pos]

        self.canvas.coords(
            self.player,
            x - 15,
            y - 15,
            x + 15,
            y + 15
        )

        self.root.after(
            250,
            self.animate_step,
            next_pos,
            target
        )

    def check_special_square(self):
        """Check snakes, ladders and win."""

        if self.player_pos == 100:
            self.status_label.config(
                text="🏆 Congratulations! You Won!",
                fg="green"
            )

            self.roll_button.config(state="disabled")
            return

        if self.player_pos in snakes:
            target = snakes[self.player_pos]

            self.status_label.config(
                text=f"🐍 Snake! {self.player_pos} → {target}",
                fg="red"
            )

            self.root.after(
                1000,
                self.animate_step,
                self.player_pos,
                target
            )

        elif self.player_pos in ladders:
            target = ladders[self.player_pos]

            self.status_label.config(
                text=f"🪜 Ladder! {self.player_pos} → {target}",
                fg="green"
            )

            self.root.after(
                1000,
                self.animate_step,
                self.player_pos,
                target
            )

        else:
            self.status_label.config(
                text=f"📍 You are on square {self.player_pos}",
                fg="black"
            )

            self.roll_button.config(state="normal")

    def play_turn(self):
        """Roll dice and move player."""

        self.roll_button.config(state="disabled")

        dice = random.randint(1, 6)

        self.status_label.config(
            text=f"🎲 You rolled {dice}",
            fg="blue"
        )

        target = self.player_pos + dice

        if target > 100:
            self.status_label.config(
                text=f"🎲 You rolled {dice}. Need exact number to reach 100!",
                fg="orange"
            )

            self.roll_button.config(state="normal")
            return

        self.root.after(
            500,
            self.animate_step,
            self.player_pos,
            target
        )


# ---------------- MAIN PROGRAM ---------------- #

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeAndLadderGame(root)
    root.mainloop()