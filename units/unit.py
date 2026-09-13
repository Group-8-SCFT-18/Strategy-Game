class Unit:
    def __init__(self, name: str, health: int, attack_power: int, movement_range: int, position: tuple[int, int] = (0, 0)):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.movement_range = movement_range
        self._position = position

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

    def get_distance_to(self, new_position: tuple[int, int]) -> int:
        """Calculates grid steps (Manhattan distance) to a target tuple position."""
        return abs(self.x - new_position[0]) + abs(self.y - new_position[1])

    def __repr__(self):
        return f"{self.name} at {self._position}"