from pacman.space import Vector
from pacman.elements.common import Element, BoardElement

class Board:
    def __init__(self, lines: list) -> None:
        self.lines = lines
        self.dim = len(lines[0])

    def __iter__(self):
        return iter(self.lines)
    
    def __next__(self):
        return next(self.lines)
    
    def _out_of_board(self, x, y) -> bool:
        if x < 0 or y < 0:
            return True
        if x >= self.dim or y >= self.dim:
            return True
        return False
    
    def get(self, vector: Vector) -> BoardElement:
        x, y = vector
        return self.lines[x][y] if not self._out_of_board(x, y) else None
    
    def put(self, element: BoardElement, vector: Vector) -> bool:
        x, y = vector
        if not self._out_of_board(x, y):
            self.lines[x][y] = element
            return True
        return False
    

    def find_closest(self, vector: Vector, element: Element):
        closest_distance = self.dim
        closest_position = None
        for row in range(self.dim):
            for col in range(self.dim):
                board_element: BoardElement = self.get(Vector(row, col))
                if board_element.get_element() == element:
                    distance = vector.manhattan_distance(board_element.get_position())
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_position = board_element.get_position()
        
        return closest_position, closest_distance
    
    def set_empty(self, vector: Vector) -> bool:
        x, y = vector
        if not self._out_of_board(x, y):
            self.lines[x][y] = BoardElement(Element.EMPTY, Vector(x, y))
            return True
        return False 
        
    def copy(self):
        return Board(
            [line.copy() for line in self.lines]
        )

    @classmethod
    def from_input(cls, input: list):
        _output = []
        for row_index in range(0, len(input)):
            row: str = input[row_index]
            if not len(row):
                continue
            elements: list = row.split(" ")
            for elem_index in range(0, len(elements)):
                element = Element.from_string(
                    element=elements[elem_index]
                )
                position = Vector(row_index, elem_index)
                elements[elem_index] = BoardElement(element, position)
            _output.append(elements)

        return cls(
            _output
        )
    
    def __str__(self) -> str:
        string = ""
        for line_index in range(len(self.lines)):
            line = self.lines[line_index]
            for element in line:
                string += f"{element} "
            if line_index != len(self.lines):
                string += "\n"

        return string