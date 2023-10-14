from pacman.elements import Element, BoardElement, NonStaticElement

class Ghost(NonStaticElement):
    def __init__(self, element: BoardElement, fear: int = 0) -> None:
        super().__init__(element)
        self.fear = fear

    def get_fear(self) -> int:
        return self.fear
    
    def set_fear(self, fear: int):
        self.fear = fear
    
    def decrease_fear(self):
        self.fear -= 1
    
    @classmethod
    def from_board(cls, board):
        return super().from_board(
            Element.GHOST,
            board
        )
    
    def __eq__(self, other: object) -> bool:
        if not super().__eq__(other):
            return False
        other: Ghost = other
        return self.fear == other.fear