from units.unit import Unit

class Tank(Unit):
    def __init__(
        self,
        name: str = "Tank",
        position: tuple[int, int] = (0, 0),
        x: int | None = None,
        y: int | None = None,
    ):
        if x is not None or y is not None:
            position = (x or 0, y or 0)
        super().__init__(
            name=name,
            health=160,
            attack_power=30,
            defense=10,
            movement_range=1,
            attack_range=1,
            position=position,
        )

    def attack(self, enemy: Unit) -> int:
        return enemy.take_damage(self.attack_power)