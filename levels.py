class Level:
    def __init__(self, number):
        self.number = number
        self.minerals_required = 50 + (self.number - 1) * 10  # Aumentar minerales requeridos por nivel
        self.enemy_speed = 1 + self.number * 0.5  # Aumentar velocidad de enemigos por nivel