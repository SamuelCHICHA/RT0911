from Point import Point

class Light(Point):
    # Etat des feux (croisements)
    RED = 0
    GREEN = 1
    COLORS = {
        RED: "red",
        GREEN: "green"
    }
    
    def __init__(self, position : Point):
        super().__init__(position.x, position.y)
        self.state = 0
        
    def __repr__(self):
        feu_repr =  self.__class__.COLORS[self.state] if self.state in self.__class__.COLORS.keys() else "/"
        # to do: change
        return f"({super().__repr__()} state = {feu_repr})"
