from units.unit import Unit

class Tank(Unit):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(
            name="Tank",
            health=180,
            attack_power=35,
            move_range=1,  # Moves slowly
            x=x,
            y=y
        )