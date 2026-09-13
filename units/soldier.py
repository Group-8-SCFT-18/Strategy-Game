from units.unit import Unit

class Soldier(Unit):
    def __init__(self, name: str = "Soldier", position: tuple[int, int] = (0, 0)):
        super().__init__(
            name=name,
            health=100,
            attack_power=20,
            movement_range=2,
            position=position  # Pass position to the base class
        )