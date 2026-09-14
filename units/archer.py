from units.unit import Unit

class Archer(Unit):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(
            name="Archer",
            health=70,
            attack_power=15,
            move_range=3,  # Mobile unit
            x=x,
            y=y
        )