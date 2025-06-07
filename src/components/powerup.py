class PowerUp:
    def __init__(self, powerup_type, duration):
        self.powerup_type = powerup_type
        self.duration = duration
        self.active = False

    def apply_effect(self, player):
        if self.powerup_type == "health":
            player.health += 20  # Example effect
        elif self.powerup_type == "speed":
            player.speed *= 1.5  # Example effect
        elif self.powerup_type == "damage":
            player.damage *= 2  # Example effect
        self.active = True

    def update(self):
        if self.active:
            self.duration -= 1  # Assuming this is called every frame
            if self.duration <= 0:
                self.deactivate()

    def deactivate(self):
        self.active = False
        # Reset player effects here if necessary
