from game.player import Player


class AIPlayer(Player):
    """Rule-based opponent that attacks first and otherwise advances."""

    def take_turn(self, game) -> str:
        enemies = [player for player in game.players if player is not self]
        enemy_units = [unit for player in enemies for unit in player.units if unit.is_alive]
        if not enemy_units:
            return "idle"

        action = "idle"
        for unit in tuple(self.units):
            if not unit.is_alive:
                continue

            target = min(enemy_units, key=lambda enemy: unit.get_distance_to(enemy.position))
            distance = unit.get_distance_to(target.position)
            if distance <= unit.attack_range:
                game.attack(self, unit, target)
                action = "attack"
                if not target.is_alive:
                    enemy_units.remove(target)
                    if not enemy_units:
                        break
                continue

            destination = self._next_step(game, unit, target)
            if destination is not None:
                game.move_unit(self, unit, destination)
                action = "move"

        return action

    @staticmethod
    def _next_step(game, unit, target):
        current_x, current_y = unit.position
        target_x, target_y = target.position
        candidates = []
        if current_x != target_x:
            candidates.append((current_x + (1 if target_x > current_x else -1), current_y))
        if current_y != target_y:
            candidates.append((current_x, current_y + (1 if target_y > current_y else -1)))

        for destination in candidates:
            if (
                game.game_map.is_within_bounds(destination)
                and not game.game_map.is_occupied(destination)
                and unit.get_distance_to(destination) <= unit.movement_range
            ):
                return destination
        return None