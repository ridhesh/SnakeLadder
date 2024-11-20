class Player:
    def __init__(self, name, color=None):
        self.name = name
        self.position = 0
        self.color = color if color else "blue"  # Default color for players
