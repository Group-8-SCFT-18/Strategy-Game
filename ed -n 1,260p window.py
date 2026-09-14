[1mdiff --git a/window.py b/window.py[m
[1mindex 42053ed..a0d996d 100644[m
[1m--- a/window.py[m
[1m+++ b/window.py[m
[36m@@ -1,221 +1,165 @@[m
[31m-"""Pygame window for the turn-based strategy game."""[m
[31m-[m
[31m-import pygame[m
[32m+[m[32mimport tkinter as tk[m
 [m
[32m+[m[32mfrom ai.ai_player import AIPlayer[m
[32m+[m[32mfrom game.game import Game[m
[32m+[m[32mfrom game.map import Map[m
[32m+[m[32mfrom game.player import Player[m
 from game.resource import ResourceNode[m
[31m-from main import create_game[m
[31m-[m
[31m-[m
[31m-BOARD_SIZE = 64[m
[31m-PANEL_WIDTH = 260[m
[31m-MARGIN = 24[m
[31m-WINDOW_WIDTH = MARGIN * 2 + BOARD_SIZE * 8 + PANEL_WIDTH[m
[31m-WINDOW_HEIGHT = MARGIN * 2 + BOARD_SIZE * 8[m
[31m-[m
[31m-BACKGROUND = (24, 29, 36)[m
[31m-PANEL = (34, 41, 51)[m
[31m-GRID_LIGHT = (211, 215, 204)[m
[31m-GRID_DARK = (167, 178, 164)[m
[31m-TEXT = (239, 241, 235)[m
[31m-MUTED_TEXT = (173, 183, 177)[m
[31m-PLAYER_COLORS = ((49, 104, 190), (190, 67, 61))[m
[31m-RESOURCE_COLORS = {[m
[31m-    "gold": (225, 179, 55),[m
[31m-    "food": (83, 161, 91),[m
[31m-    "wood": (151, 99, 53),[m
[31m-}[m
[31m-[m
[31m-[m
[31m-def create_window_game():[m
[31m-    """Create the standard game and place collectible resources on its map."""[m
[31m-    game = create_game()[m
[31m-    resources = ([m
[31m-        ResourceNode((3, 2), "gold", 20),[m
[31m-        ResourceNode((4, 4), "food", 20),[m
[31m-        ResourceNode((2, 5), "wood", 20),[m
[31m-        ResourceNode((5, 3), "gold", 20),[m
[31m-    )[m
[31m-    for resource in resources:[m
[31m-        game.game_map.add_resource(resource)[m
[31m-    return game[m
[31m-[m
[31m-[m
[31m-def run(game=None):[m
[31m-    """Run the graphical game until the window is closed."""[m
[31m-    pygame.init()[m
[31m-    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))[m
[31m-    pygame.display.set_caption("Grid Strategy Game")[m
[31m-    clock = pygame.time.Clock()[m
[31m-    fonts = {[m
[31m-        "title": pygame.font.SysFont("dejavusans", 24, bold=True),[m
[31m-        "body": pygame.font.SysFont("dejavusans", 18),[m
[31m-        "small": pygame.font.SysFont("dejavusans", 15),[m
[31m-    }[m
[31m-    game = game or create_window_game()[m
[31m-    selected_index = 0[m
[31m-    status = "Use the arrow keys to move."[m
[31m-    running = True[m
[31m-[m
[31m-    while running:[m
[31m-        active_units = game.current_player.units[m
[31m-        if active_units:[m
[31m-            selected_index %= len(active_units)[m
[31m-            selected_unit = active_units[selected_index][m
[31m-        else:[m
[31m-            selected_unit = None[m
[31m-[m
[31m-        for event in pygame.event.get():[m
[31m-            if event.type == pygame.QUIT:[m
[31m-                running = False[m
[31m-            elif event.type == pygame.KEYDOWN:[m
[31m-                if event.key == pygame.K_ESCAPE:[m
[31m-                    running = False[m
[31m-                elif event.key == pygame.K_TAB and active_units:[m
[31m-                    selected_index = (selected_index + 1) % len(active_units)[m
[31m-                    status = f"Selected {active_units[selected_index].name}."[m
[31m-                elif event.key in (pygame.K_RETURN, pygame.K_e):[m
[31m-                    try:[m
[31m-                        game.end_turn()[m
[31m-                        selected_index = 0[m
[31m-                        status = f"{game.current_player.name}'s turn."[m
[31m-                    except ValueError as error:[m
[31m-                        status = str(error)[m
[31m-                elif event.key in ([m
[31m-                    pygame.K_UP,[m
[31m-                    pygame.K_DOWN,[m
[31m-                    pygame.K_LEFT,[m
[31m-                    pygame.K_RIGHT,[m
[31m-                ):[m
[31m-                    if selected_unit is None:[m
[31m-                        status = "This player has no units."[m
[31m-                    else:[m
[31m-                        offsets = {[m
[31m-                            pygame.K_UP: (0, -1),[m
[31m-                            pygame.K_DOWN: (0, 1),[m
[31m-                            pygame.K_LEFT: (-1, 0),[m
[31m-                            pygame.K_RIGHT: (1, 0),[m
[31m-                        }[m
[31m-                        try:[m
[31m-                            status = move_selected(game, selected_unit, offsets[event.key])[m
[31m-                        except ValueError as error:[m
[31m-                            status = str(error)[m
[31m-[m
[31m-        draw_game(screen, game, selected_unit, status, fonts)[m
[31m-        pygame.display.flip()[m
[31m-        clock.tick(60)[m
[31m-[m
[31m-    pygame.quit()[m
[31m-[m
[31m-[m
[31m-def move_selected(game, unit, offset):[m
[31m-    """Move a selected unit one tile and describe any collected resource."""[m
[31m-    x_coordinate, y_coordinate = unit.position[m
[31m-    delta_x, delta_y = offset[m
[31m-    destination = (x_coordinate + delta_x, y_coordinate + delta_y)[m
[31m-    resource = game.move_unit(game.current_player, unit, destination)[m
[31m-    if resource is None:[m
[31m-        return f"{unit.name} moved to {destination}."[m
[31m-    return ([m
[31m-        f"Collected {resource.amount} {resource.resource_type} "[m
[31m-        f"at {destination}."[m
[31m-    )[m
[31m-[m
[31m-[m
[31m-def draw_game(screen, game, selected_unit, status, fonts):[m
[31m-    """Draw the board, units, resources, and current player panel."""[m
[31m-    screen.fill(BACKGROUND)[m
[31m-    draw_board(screen, game, selected_unit, fonts["body"])[m
[31m-[m
[31m-    panel_x = MARGIN + BOARD_SIZE * game.game_map.width + MARGIN[m
[31m-    pygame.draw.rect([m
[31m-        screen,[m
[31m-        PANEL,[m
[31m-        (panel_x, MARGIN, PANEL_WIDTH, BOARD_SIZE * game.game_map.height),[m
[31m-        border_radius=8,[m
[31m-    )[m
[31m-    draw_text(screen, fonts["title"], "Strategy Game", panel_x + 18, MARGIN + 18)[m
[31m-    draw_text([m
[31m-        screen,[m
[31m-        fonts["body"],[m
[31m-        f"Turn {game.turn_number}: {game.current_player.name}",[m
[31m-        panel_x + 18,[m
[31m-        MARGIN + 58,[m
[31m-    )[m
[31m-[m
[31m-    y_position = MARGIN + 105[m
[31m-    for index, player in enumerate(game.players):[m
[31m-        draw_text(screen, fonts["body"], player.name, panel_x + 18, y_position,[m
[31m-                  PLAYER_COLORS[index])[m
[31m-        y_position += 28[m
[31m-        resources = player.resources.as_dict()[m
[31m-        draw_text([m
[31m-            screen,[m
[31m-            fonts["small"],[m
[31m-            f"Gold {resources['gold']}  Food {resources['food']}",[m
[31m-            panel_x + 18,[m
[31m-            y_position,[m
[31m-            MUTED_TEXT,[m
[32m+[m[32mfrom units.soldier import Soldier[m
[32m+[m
[32m+[m
[32m+[m[32mclass StrategyWindow:[m
[32m+[m[32m    CELL_SIZE = 56[m
[32m+[m
[32m+[m[32m    def __init__(self, root: tk.Tk):[m
[32m+[m[32m        self.root = root[m
[32m+[m[32m        self.root.title("Strategy Game")[m
[32m+[m[32m        self.game = Game(Map(width=8, height=8))[m
[32m+[m[32m        self.human = Player("Human")[m
[32m+[m[32m        self.computer = AIPlayer("Computer")[m
[32m+[m[32m        self.game.add_player(self.human)[m
[32m+[m[32m        self.game.add_player(self.computer)[m
[32m+[m
[32m+[m[32m        self.selected_index = 0[m
[32m+[m[32m        self.status = tk.StringVar(value="Your turn")[m
[32m+[m[32m        self.canvas = tk.Canvas([m
[32m+[m[32m            root,[m
[32m+[m[32m            width=self.game.game_map.width * self.CELL_SIZE,[m
[32m+[m[32m            height=self.game.game_map.height * self.CELL_SIZE,[m
[32m+[m[32m            background="#18212b",[m
[32m+[m[32m            highlightthickness=0,[m
         )[m
[31m-        y_position += 22[m
[31m-        draw_text([m
[31m-            screen,[m
[31m-            fonts["small"],[m
[31m-            f"Wood {resources['wood']}",[m
[31m-            panel_x + 18,[m
[31m-            y_position,[m
[31m-            MUTED_TEXT,[m
[31m-        )[m
[31m-        y_position += 38[m
[31m-[m
[31m-    draw_text(screen, fonts["small"], "Controls", panel_x + 18, y_position)[m
[31m-    y_position += 25[m
[31m-    for control in ("Arrows  Move unit", "Tab  Select unit", "E / Enter  End turn", "Esc  Quit"):[m
[31m-        draw_text(screen, fonts["small"], control, panel_x + 18, y_position, MUTED_TEXT)[m
[31m-        y_position += 21[m
[31m-[m
[31m-    draw_text(screen, fonts["small"], status, panel_x + 18, WINDOW_HEIGHT - 60, TEXT)[m
[31m-[m
[31m-[m
[31m-def draw_board(screen, game, selected_unit, font):[m
[31m-    """Draw map cells and their contents."""[m
[31m-    for y_coordinate in range(game.game_map.height):[m
[31m-        for x_coordinate in range(game.game_map.width):[m
[31m-            cell = pygame.Rect([m
[31m-                MARGIN + x_coordinate * BOARD_SIZE,[m
[31m-                MARGIN + y_coordinate * BOARD_SIZE,[m
[31m-                BOARD_SIZE,[m
[31m-                BOARD_SIZE,[m
[32m+[m[32m        self.canvas.pack(padx=12, pady=12)[m
[32m+[m[32m        tk.Label(root, textvariable=self.status).pack(pady=(0, 10))[m
[32m+[m
[32m+[m[32m        self._add_starting_units()[m
[32m+[m[32m        root.bind("<Left>", lambda event: self._move_selected(-1, 0))[m
[32m+[m[32m        root.bind("<Right>", lambda event: self._move_selected(1, 0))[m
[32m+[m[32m        root.bind("<Up>", lambda event: self._move_selected(0, -1))[m
[32m+[m[32m        root.bind("<Down>", lambda event: self._move_selected(0, 1))[m
[32m+[m[32m        root.bind("<Tab>", self._select_next)[m
[32m+[m[32m        root.bind("a", self._attack_selected)[m
[32m+[m[32m        root.bind("A", self._attack_selected)[m
[32m+[m[32m        root.bind("<Return>", self._run_ai_turn)[m
[32m+[m[32m        self.draw()[m
[32m+[m
[32m+[m[32m    def _add_starting_units(self):[m
[32m+[m[32m        self.game.add_unit(self.human, Soldier(position=(1, 1)))[m
[32m+[m[32m        self.game.add_unit(self.computer, Soldier(position=(6, 6)))[m
[32m+[m[32m        self.game.game_map.add_resource(ResourceNode((2, 1), "gold", amount=20))[m
[32m+[m[32m        self.game.game_map.add_resource(ResourceNode((5, 6), "food", amount=20))[m
[32m+[m
[32m+[m[32m    @property[m
[32m+[m[32m    def selected_unit(self):[m
[32m+[m[32m        if not self.human.units:[m
[32m+[m[32m            return None[m
[32m+[m[32m        return self.human.units[self.selected_index % len(self.human.units)][m
[32m+[m
[32m+[m[32m    def _move_selected(self, x_delta, y_delta):[m
[32m+[m[32m        unit = self.selected_unit[m
[32m+[m[32m        if unit is None or self.game.current_player is not self.human:[m
[32m+[m[32m            return[m
[32m+[m[32m        destination = (unit.x + x_delta, unit.y + y_delta)[m
[32m+[m[32m        try:[m
[32m+[m[32m            resource = self.game.move_unit(self.human, unit, destination)[m
[32m+[m[32m        except ValueError as error:[m
[32m+[m[32m            self.status.set(str(error))[m
[32m+[m[32m        else:[m
[32m+[m[32m            self.status.set([m
[32m+[m[32m                f"Collected {resource.resource_type}" if resource else "Unit moved"[m
             )[m
[31m-            color = GRID_LIGHT if (x_coordinate + y_coordinate) % 2 == 0 else GRID_DARK[m
[31m-            pygame.draw.rect(screen, color, cell)[m
[31m-            position = (x_coordinate, y_coordinate)[m
[31m-            resource = game.game_map.get_resource_at(position)[m
[31m-            if resource is not None:[m
[31m-                pygame.draw.circle(screen, RESOURCE_COLORS[resource.resource_type], cell.center, 17)[m
[31m-                draw_centered_text(screen, font, resource.resource_type[0].upper(), cell.center)[m
[31m-[m
[31m-            unit = game.game_map.get_unit_at(position)[m
[31m-            if unit is not None:[m
[31m-                player_index = next([m
[31m-                    index for index, player in enumerate(game.players) if unit in player.units[m
[32m+[m[32m        self.draw()[m
[32m+[m
[32m+[m[32m    def _select_next(self, event=None):[m
[32m+[m[32m        if self.human.units:[m
[32m+[m[32m            self.selected_index = (self.selected_index + 1) % len(self.human.units)[m
[32m+[m[32m        self.draw()[m
[32m+[m[32m        return "break"[m
[32m+[m
[32m+[m[32m    def _attack_selected(self, event=None):[m
[32m+[m[32m        unit = self.selected_unit[m
[32m+[m[32m        if unit is None or self.game.current_player is not self.human:[m
[32m+[m[32m            return "break"[m
[32m+[m
[32m+[m[32m        targets = [[m
[32m+[m[32m            enemy[m
[32m+[m[32m            for enemy_player in self.game.players[m
[32m+[m[32m            if enemy_player is not self.human[m
[32m+[m[32m            for enemy in enemy_player.units[m
[32m+[m[32m            if enemy.is_alive[m
[32m+[m[32m            and unit.get_distance_to(enemy.position) <= unit.attack_range[m
[32m+[m[32m        ][m
[32m+[m[32m        if not targets:[m
[32m+[m[32m            self.status.set("No enemy in attack range")[m
[32m+[m[32m        else:[m
[32m+[m[32m            target = min(targets, key=lambda enemy: unit.get_distance_to(enemy.position))[m
[32m+[m[32m            damage = self.game.attack(self.human, unit, target)[m
[32m+[m[32m            self.status.set(f"Attacked {target.name} for {damage} damage")[m
[32m+[m[32m        self.draw()[m
[32m+[m[32m        return "break"[m
[32m+[m
[32m+[m[32m    def _run_ai_turn(self, event=None):[m
[32m+[m[32m        if self.game.current_player is not self.human:[m
[32m+[m[32m            return "break"[m
[32m+[m[32m        self.game.end_turn()[m
[32m+[m[32m        action = self.computer.take_turn(self.game)[m
[32m+[m[32m        self.game.end_turn()[m
[32m+[m[32m        self.status.set(f"Computer: {action}. Your turn")[m
[32m+[m[32m        self.draw()[m
[32m+[m[32m        return "break"[m
[32m+[m
[32m+[m[32m    def draw(self):[m
[32m+[m[32m        self.canvas.delete("all")[m
[32m+[m[32m        for x in range(self.game.game_map.width):[m
[32m+[m[32m            for y in range(self.game.game_map.height):[m
[32m+[m[32m                left = x * self.CELL_SIZE[m
[32m+[m[32m                top = y * self.CELL_SIZE[m
[32m+[m[32m                self.canvas.create_rectangle([m
[32m+[m[32m                    left,[m
[32m+[m[32m                    top,[m
[32m+[m[32m                    left + self.CELL_SIZE,[m
[32m+[m[32m                    top + self.CELL_SIZE,[m
[32m+[m[32m                    outline="#314252",[m
[32m+[m[32m                    fill="#1f2d38" if (x + y) % 2 else "#223541",[m
                 )[m
[31m-                unit_color = PLAYER_COLORS[player_index][m
[31m-                pygame.draw.circle(screen, unit_color, cell.center, 23)[m
[31m-                draw_centered_text(screen, font, unit.name[0].upper(), cell.center)[m
[31m-                if unit is selected_unit:[m
[31m-                    pygame.draw.circle(screen, (255, 244, 181), cell.center, 28, 3)[m
 [m
[32m+[m[32m        for resource in self.game.game_map.resources:[m
[32m+[m[32m            x, y = resource.position[m
[32m+[m[32m            self.canvas.create_text([m
[32m+[m[32m                (x + 0.5) * self.CELL_SIZE,[m
[32m+[m[32m                (y + 0.78) * self.CELL_SIZE,[m
[32m+[m[32m                text=resource.resource_type[0].upper(),[m
[32m+[m[32m                fill="#f4d35e",[m
[32m+[m[32m                font=("TkDefaultFont", 11, "bold"),[m
[32m+[m[32m            )[m
 [m
[31m-def draw_text(screen, font, text, x_position, y_position, color=TEXT):[m
[31m-    """Draw left-aligned text."""[m
[31m-    screen.blit(font.render(text, True, color), (x_position, y_position))[m
[32m+[m[32m        for player, color in ((self.human, "#4ecdc4"), (self.computer, "#ff6b6b")):[m
[32m+[m[32m            for unit in player.units:[m
[32m+[m[32m                x, y = unit.position[m
[32m+[m[32m                padding = 8[m
[32m+[m[32m                self.canvas.create_oval([m
[32m+[m[32m                    x * self.CELL_SIZE + padding,[m
[32m+[m[32m                    y * self.CELL_SIZE + padding,[m
[32m+[m[32m                    (x + 1) * self.CELL_SIZE - padding,[m
[32m+[m[32m                    (y + 1) * self.CELL_SIZE - padding,[m
[32m+[m[32m                    fill=color,[m
[32m+[m[32m                    outline="#f8f9fa" if unit is self.selected_unit else color,[m
[32m+[m[32m                    width=3 if unit is self.selected_unit else 1,[m
[32m+[m[32m                )[m
[32m+[m[32m                self.canvas.create_text([m
[32m+[m[32m                    (x + 0.5) * self.CELL_SIZE,[m
[32m+[m[32m                    (y + 0.5) * self.CELL_SIZE,[m
[32m+[m[32m                    text=unit.name[0],[m
[32m+[m[32m                    fill="#102027",[m
[32m+[m[32m                    font=("TkDefaultFont", 16, "bold"),[m
[32m+[m[32m                )[m
 [m
 [m
[31m-def draw_centered_text(screen, font, text, center):[m
[31m-    """Draw text centered at a point."""[m
[31m-    surface = font.render(text, True, TEXT)[m
[31m-    screen.blit(surface, surface.get_rect(center=center))[m
[32m+[m[32mdef main():[m
[32m+[m[32m    root = tk.Tk()[m
[32m+[m[32m    StrategyWindow(root)[m
[32m+[m[32m    root.mainloop()[m
 [m
 [m
 if __name__ == "__main__":[m
[31m-    run()[m
[32m+[m[32m    main()[m
\ No newline at end of file[m
