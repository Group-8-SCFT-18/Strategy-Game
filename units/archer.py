from units.unit import Unit

class Archer(Unit):
    def __init__(self, position: tuple[int, int] = (0, 0), x: int | None = None, y: int | None = None):
        if x is not None or y is not None:
            position = (x or 0, y or 0)
        super().__init__(
            name="Archer",
            health=75,
            attack_power=18,
            defense=2,
            movement_range=2,
            attack_range=3,
            position=position,
        )

    def attack(self, enemy: Unit) -> int:
        return enemy.take_damage(self.attack_power)