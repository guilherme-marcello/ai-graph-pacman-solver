class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

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
    def __init__(self, element: Element, position: Position) -> None:
        self.element = element
        self.position = position

    def __str__(self) -> str:
        return str(self.element)

class GameConditions:
    def __init__(self, fear_goal: int, supergum_power: int, initial_fear: int) -> None:
        self.T = fear_goal
        self.P = supergum_power
        self.M = initial_fear

    @classmethod
    def from_list(cls, input: list):
        key_value = dict()
        for kv in input:
            key, value = kv.split("=")
            key_value[key] = int(value)
        return cls(
            key_value.get("T"),
            key_value.get("M"),
            key_value.get("P")
        )

    def __str__(self) -> str:
        return f"T={self.T}\nM={self.M}\nP={self.P}"


class Board:
    def __init__(self, lines: list) -> None:
        self.lines = lines

    @classmethod
    def from_input(cls, input: list):
        _output = []
        for row_index in range(0, len(input)):
            row: str = input[row_index]
            elements: list = row.split(" ")
            for elem_index in range(0, len(elements)):
                element = Element.from_string(
                    element=elements[elem_index]
                )
                position = Position(row_index, elem_index)
                elements[elem_index] = BoardElement(element, position)
            _output.append(elements)

        return cls(
            _output
        )
    
    def __str__(self) -> str:
        string = ""
        for line in self.lines:
            for element in line:
                string += f"{element} "
            string += "\n"

        return string

class Game:
    def __init__(self, conditions: GameConditions, board: Board) -> None:
        self.conditions = conditions
        self.board = board

    @classmethod
    def from_input(cls, text_input: str):
        params = text_input.split("\n")
        return cls(
            GameConditions.from_list(params[:3]),
            Board.from_input(params[3:])
        )
    
    def __str__(self) -> str:
        return f"{self.conditions}\n{self.board}"
