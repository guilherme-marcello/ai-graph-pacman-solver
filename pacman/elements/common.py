from pacman.space import Vector

class Element:
    WALL = "="
    PACMAN = "@"
    GHOST = "F"
    SUPER_GUM = "*"
    EMPTY = "."
    NONE = ""

    @staticmethod
    def from_string(element: str):
        if element == Element.WALL:
            return Element.WALL
        if element == Element.PACMAN:
            return Element.PACMAN
        if element == Element.SUPER_GUM:
            return Element.SUPER_GUM
        if element == Element.GHOST:
            return Element.GHOST
        if element == Element.EMPTY:
            return Element.EMPTY
        if element == Element.NONE:
            return Element.NONE

        return None

class BoardElement:
    def __init__(self, element: Element, position: Vector) -> None:
        self.element = element
        self.position = position

    def get_position(self) -> Vector:
        return self.position
    
    def get_element(self) -> Element:
        return self.element

    def __str__(self) -> str:
        return str(self.element)
    
    def copy(self):
        x, y = self.position
        return BoardElement(
            self.element,
            Vector(x, y)
        )
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BoardElement):
            return False
        return self.element == other.element and self.position == other.position
    
    def __repr__(self) -> str:
        return f"{self.element}{self.position}"
    
class NonStaticElement:
    def __init__(self, element: BoardElement) -> None:
        self.element = element

    def get_position(self) -> Vector:
        return self.element.get_position()
    
    def set_position(self, vector: Vector):
        self.element.position = vector

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NonStaticElement):
            return False
        return self.element == other.element

    @classmethod
    def from_board(cls, target_element: Element, board):
        for line in board:
            line: list
            for element in line:
                element: BoardElement
                if element.get_element() == target_element:
                    board_element = element
        return cls(
            board_element
        )
    
    def __str__(self) -> str:
        return f"{str(self.element)}{self.element.get_position()}"
    
    def __repr__(self) -> str:
        return self.__str__()