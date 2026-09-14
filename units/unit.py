from abc import ABC, abstractmethod


class Unit(ABC):
    def __init__(
        self,
        name: str,
        health: int,
        attack_power: int,
        defense: int,
        movement_range: int = 1,
        attack_range: int = 1,
        position: tuple[int, int] = (0, 0),
    ):
        if health <= 0:
            raise ValueError("health must be positive")
        if attack_power < 0:
            raise ValueError("attack_power cannot be negative")
        if defense < 0:
            raise ValueError("defense cannot be negative")
        if movement_range <= 0:
            raise ValueError("movement_range must be positive")
        if attack_range <= 0:
            raise ValueError("attack_range must be positive")

        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.defense = defense
        self.movement_range = movement_range
        self.attack_range = attack_range
        self._position = position

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @property
    def position(self) -> tuple[int, int]:
        """Returns the current position as an (x, y) tuple for Map compatibility."""
        return self._position

    @property
    def x(self) -> int:
        return self._position[0]

    @property
    def y(self) -> int:
        return self._position[1]

    def set_position(self, position: tuple[int, int]):
        """Updates unit position using a tuple (x, y)."""
        self._position = position

    def take_damage(self, damage: int) -> int:
        actual_damage = max(0, damage - self.defense)
        self.health = max(0, self.health - actual_damage)
        return actual_damage

    @abstractmethod
    def attack(self, enemy: "Unit") -> int:
        """Attack an enemy and return the damage dealt."""
        raise NotImplementedError

    def get_distance_to(self, new_position: tuple[int, int]) -> int:
        """Calculates grid steps (Manhattan distance) to a target tuple position."""
        return abs(self.x - new_position[0]) + abs(self.y - new_position[1])

    def __repr__(self):
        return f"{self.name} at {self._position}"