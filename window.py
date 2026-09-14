import tkinter as tk

from ai.ai_player import AIPlayer
from game.game import Game
from game.map import Map
from game.player import Player
from units.soldier import Soldier


class StrategyWindow:
    CELL_SIZE = 56

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Strategy Game")
        self.game = Game(Map(width=8, height=8))
        self.human = Player("Human")
        self.computer = AIPlayer("Computer")
        self.game.add_player(self.human)
        self.game.add_player(self.computer)

        self.selected_index = 0
        self.status = tk.StringVar(value="Your turn")
        self.canvas = tk.Canvas(
            root,
            width=self.game.game_map.width * self.CELL_SIZE,
            height=self.game.game_map.height * self.CELL_SIZE,
            background="#18212b",
            highlightthickness=0,
        )
        self.canvas.pack(padx=12, pady=12)
        tk.Label(root, textvariable=self.status).pack(pady=(0, 10))

        self._add_starting_units()
        root.bind("<Left>", lambda event: self._move_selected(-1, 0))
        root.bind("<Right>", lambda event: self._move_selected(1, 0))
        root.bind("<Up>", lambda event: self._move_selected(0, -1))
        root.bind("<Down>", lambda event: self._move_selected(0, 1))
        root.bind("<Tab>", self._select_next)
        root.bind("<Return>", self._run_ai_turn)
        self.draw()

    def _add_starting_units(self):
        self.game.add_unit(self.human, Soldier(position=(1, 1)))
        self.game.add_unit(self.computer, Soldier(position=(6, 6)))

    @property
    def selected_unit(self):
        if not self.human.units:
            return None
        return self.human.units[self.selected_index % len(self.human.units)]

    def _move_selected(self, x_delta, y_delta):
        unit = self.selected_unit
        if unit is None or self.game.current_player is not self.human:
            return
        destination = (unit.x + x_delta, unit.y + y_delta)
        try:
            resource = self.game.move_unit(self.human, unit, destination)
        except ValueError as error:
            self.status.set(str(error))
        else:
            self.status.set(
                f"Collected {resource.resource_type}" if resource else "Unit moved"
            )
        self.draw()

    def _select_next(self, event=None):
        if self.human.units:
            self.selected_index = (self.selected_index + 1) % len(self.human.units)
        self.draw()
        return "break"

    def _run_ai_turn(self, event=None):
        if self.game.current_player is not self.human:
            return "break"
        self.game.end_turn()
        action = self.computer.take_turn(self.game)
        self.game.end_turn()
        self.status.set(f"Computer: {action}. Your turn")
        self.draw()
        return "break"

    def draw(self):
        self.canvas.delete("all")
        for x in range(self.game.game_map.width):
            for y in range(self.game.game_map.height):
                left = x * self.CELL_SIZE
                top = y * self.CELL_SIZE
                self.canvas.create_rectangle(
                    left,
                    top,
                    left + self.CELL_SIZE,
                    top + self.CELL_SIZE,
                    outline="#314252",
                    fill="#1f2d38" if (x + y) % 2 else "#223541",
                )

        for player, color in ((self.human, "#4ecdc4"), (self.computer, "#ff6b6b")):
            for unit in player.units:
                x, y = unit.position
                padding = 8
                self.canvas.create_oval(
                    x * self.CELL_SIZE + padding,
                    y * self.CELL_SIZE + padding,
                    (x + 1) * self.CELL_SIZE - padding,
                    (y + 1) * self.CELL_SIZE - padding,
                    fill=color,
                    outline="#f8f9fa" if unit is self.selected_unit else color,
                    width=3 if unit is self.selected_unit else 1,
                )
                self.canvas.create_text(
                    (x + 0.5) * self.CELL_SIZE,
                    (y + 0.5) * self.CELL_SIZE,
                    text=unit.name[0],
                    fill="#102027",
                    font=("TkDefaultFont", 16, "bold"),
                )


def main():
    root = tk.Tk()
    StrategyWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()