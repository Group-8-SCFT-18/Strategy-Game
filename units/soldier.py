from units.unit import Unit

class Soldier(Unit):
    def __init__(self, name: str = "Soldier", position: tuple[int, int] = (0, 0)):
        super().__init__(
            name=name,
            health=100,
            attack_power=20,
            defense=5,
            movement_range=2,
            attack_range=1,
            position=position,
        )

    def attack(self, enemy: Unit) -> int:
        return enemy.take_damage(self.attack_power)