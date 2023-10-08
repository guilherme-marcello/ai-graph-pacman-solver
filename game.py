class Vector:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{(self.x, self.y)}"
    
    def __iter__(self):
        yield self.x
        yield self.y

    def __add__(self, other):
        if isinstance(other, Vector):
            new_x = self.x + other.x
            new_y = self.y + other.y
            return Vector(new_x, new_y)
        else:
            raise TypeError("Unsupported operand type. You can only add Vector objects.")

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
        self.nrows = len(lines)
        self.ncols = len(lines[0])

    def __iter__(self):
        return iter(self.lines)
    
    def __next__(self):
        return next(self.lines)
    
    def _out_of_board(self, x, y) -> bool:
        if x < 0 or y < 0:
            return True
        if x >= self.ncols or y >= self.nrows:
            return True
        return False
    
    def get(self, vector: Vector) -> BoardElement:
        x, y = vector
        return self.lines[y][x] if not self._out_of_board(x, y) else None
    
    def put(self, element: BoardElement, vector: Vector) -> bool:
        x, y = vector
        if not self._out_of_board(x, y):
            self.lines[y][x] = element
            return True
        return False
    
    def set_empty(self, vector: Vector) -> bool:
        x, y = vector
        if not self._out_of_board(x, y):
            self.lines[y][x] = BoardElement(Element.EMPTY, Vector(x, y))
            return True
        return False 
        

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
                position = Vector(row_index, elem_index)
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

class Direction:
    NORTH = Vector(0, -1)
    SOUTH = Vector(0, 1)
    WEST = Vector(-1, 0)
    EAST = Vector(1, 0)

    string_parser = {
        "N" : NORTH,
        "S" : SOUTH,
        "W" : WEST,
        "E" : EAST
    }

    @staticmethod
    def from_string(direction: str):
        return Direction.string_parser.get(direction)

class NonStaticElement:
    def __init__(self, element: BoardElement, board: Board) -> None:
        self.element = element
        self.board = board
    
    def move(self, delta: Vector):
        target_element = self.board.get(
            self.element.position + delta
        )

        if not target_element or target_element == Element.WALL:
            return
        
        self.board.set_empty(
            self.element.position
        )
        self.element.position += delta
        self.board.put(
            self.element, self.element.position
        )
        
    
    @classmethod
    def from_board(cls, target_element: Element, board: Board):
        for line in board:
            line: list
            for element in line:
                element: BoardElement
                if element.get_element() == target_element:
                    board_element = element
        return cls(
            board_element,
            board
        )
    
    def __str__(self) -> str:
        return f"{str(self.element)}{self.element.get_position()}"
    
    def __repr__(self) -> str:
        return self.__str__()


class Pacman(NonStaticElement):
    def __init__(self, element: BoardElement, board: Board) -> None:
        super().__init__(element, board)
    
    @classmethod
    def from_board(cls, board: Board):
        return super().from_board(
            Element.PACMAN,
            board
        )
    

    
class Ghost(NonStaticElement):
    def __init__(self, element: BoardElement, board: Board) -> None:
        super().__init__(element, board)
    
    @classmethod
    def from_board(cls, board: Board):
        return super().from_board(
            Element.GHOST,
            board
        )
    
class SuperGum(NonStaticElement):
    def __init__(self, element: BoardElement, board: Board) -> None:
        super().__init__(element, board)

    @staticmethod
    def find_all(board: Board) -> list:
        gums = list()
        for line in board:
            line: list
            for element in line:
                element: BoardElement
                if element.get_element() == Element.SUPER_GUM:
                    gums.append(
                        NonStaticElement(element, board)
                    )
        return gums

    


class GameState:
    def __init__(self, pacman: Pacman, ghost: Ghost, supergums: list) -> None:
        self.pacman = pacman
        self.ghost = ghost
        self.supergums = supergums

    @classmethod
    def from_board(cls, board: Board):
        return cls(
            Pacman.from_board(board),
            Ghost.from_board(board),
            SuperGum.find_all(board)
        )
    
    def __str__(self) -> str:
        return f"{self.pacman}\n{self.ghost}\n{self.supergums}"

class Game:
    def __init__(self, conditions: GameConditions, board: Board) -> None:
        self.conditions = conditions
        self.board = board
        self.state = GameState.from_board(board)


    @classmethod
    def from_input(cls, text_input: str):
        params = text_input.split("\n")
        return cls(
            GameConditions.from_list(params[:3]),
            Board.from_input(params[3:])
        )
    
    def __str__(self) -> str:
        return f"{self.conditions}\n{self.board}\n{self.state}"
