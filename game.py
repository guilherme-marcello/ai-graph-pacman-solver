class Vector:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def manhattan_distance(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __repr__(self) -> str:
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

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: object):
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y


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
            key_value.get("P"),
            key_value.get("M")
        )

    def __str__(self) -> str:
        return f"T={self.T}\nM={self.M}\nP={self.P}"


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

class Direction:
    NORTH = Vector(-1, 0)
    SOUTH = Vector(1, 0)
    WEST = Vector(0, -1)
    EAST = Vector(0, 1)

    string_parser = {
        "N": NORTH,
        "S": SOUTH,
        "W": WEST,
        "E": EAST
    }

    def __init__(self, vector):
        self.vector = vector

    @classmethod
    def from_string(cls, direction: str):
        return cls(
            cls.string_parser.get(direction)
        )

    def to_string(self):
        for direction, value in Direction.string_parser.items():
            if value == self.vector:
                return direction
        return None

    @classmethod
    def get_options(cls):
        return [cls.NORTH, cls.WEST, cls.EAST, cls.SOUTH]

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
    def from_board(cls, target_element: Element, board: Board):
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


class Pacman(NonStaticElement):
    def __init__(self, element: BoardElement, steps: int = 0, visited: dict = dict()) -> None:
        super().__init__(element)
        self.steps = steps
        self.visited_positions = visited
        if not self.visited_positions.get(self.element.get_position()):
            self.visited_positions[self.element.get_position()] = 2

    def get_cost(self, vector: Vector) -> int:
        cost = self.visited_positions.get(vector)
        return cost if cost else 1

    def get_steps(self) -> int:
        return self.steps
    
    def increase_steps(self):
        self.steps += 1
    
    def mark_as_visited(self, vector: Vector):
        n_visits = self.visited_positions.get(vector)
        n_visits = n_visits + 1 if n_visits else 2
        self.visited_positions[vector] = n_visits

    def copy(self):
        pacman = Pacman(
            element=self.element.copy(),
            steps=self.steps,
            visited=self.visited_positions.copy()
        )
        return pacman
    
    def __eq__(self, other: object) -> bool:
        if not super().__eq__(other):
            return False
        other: Pacman = other
        return self.steps == other.steps and self.visited_positions == other.visited_positions
    
    @classmethod
    def from_board(cls, board: Board):
        return super().from_board(
            Element.PACMAN,
            board
        )
    

    
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
    def from_board(cls, board: Board):
        return super().from_board(
            Element.GHOST,
            board
        )
    
    def __eq__(self, other: object) -> bool:
        if not super().__eq__(other):
            return False
        other: Ghost = other
        return self.fear == other.fear
    
class SuperGum:
    @staticmethod
    def find_all(board: Board) -> list:
        gums = list()
        for line in board:
            line: list
            for element in line:
                element: BoardElement
                if element.get_element() == Element.SUPER_GUM:
                    gums.append(
                        element
                    )
        return gums

    


class GameState:
    def __init__(self, pacman: Pacman, ghost: Ghost, supergums: list, board: Board) -> None:
        self.pacman = pacman
        self.ghost = ghost
        self.supergums = supergums
        self.board = board

    def __iter__(self):
        yield self.pacman
        yield self.ghost
        yield self.supergums
        yield self.board


    @classmethod
    def from_board(cls, board: Board, initial_fear: int):
        ghost = Ghost.from_board(board)
        ghost.set_fear(initial_fear)
        return cls(
            Pacman.from_board(board),
            ghost,
            SuperGum.find_all(board),
            board
        )
    
    def copy(self):
        current_ghost_fear = self.ghost.get_fear()
        new = GameState.from_board(
            self.board.copy(), 
            current_ghost_fear
        )
    
        new_pacman: Pacman = self.pacman.copy()
        new.board.put(
            new_pacman.element,
            new_pacman.get_position()
        )
        new.pacman = new_pacman
        return new
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameState):
            return False
        other: GameState = other
        
        if (self.pacman != other.pacman):
            return False
        
        if (self.ghost != other.ghost):
            return False
        
        if not all(x in self.supergums for x in other.supergums):
            return False
        
        return True
    
    def __str__(self) -> str:
        string = f"Fear - {self.pacman.get_steps() + self.ghost.get_fear()}\n"

        string += f"Pacman - {self.pacman.get_position()} - steps = {self.pacman.get_steps()} - visited = {self.pacman.visited_positions}\n"
        string += f"Ghost - {self.ghost.get_position()} - current fear {self.ghost.get_fear()}\n"
        string += f"{self.supergums}\n"
        return string
    
class Game:
    def __init__(self, conditions: GameConditions, board: Board) -> None:
        self.conditions = conditions
        self.board = board
        self.state = GameState.from_board(board)

    def get_state(self) -> GameState:
        return self.state
    
    @staticmethod
    def apply(state: GameState, action: str, max_fear: int):
        direction = Direction.from_string(action)
        current_pos = state.pacman.get_position()
        target_pos = current_pos + direction.vector

        board_element = state.board.get(
            target_pos
        )

        if not board_element or board_element.element == Element.WALL:
            return state
        
        state.ghost.decrease_fear()
        state.pacman.mark_as_visited(target_pos)
        state.pacman.increase_steps()

        if (board_element.element == Element.SUPER_GUM):
            state.supergums.remove(board_element)
            state.ghost.set_fear(max_fear)

        state.board.put(BoardElement(Element.EMPTY, current_pos), current_pos)
        state.board.put(state.pacman.element, target_pos)
        state.pacman.set_position(target_pos)

        return state

    @classmethod
    def from_input(cls, text_input: str):
        params = text_input.split("\n")
        return cls(
            GameConditions.from_list(params[:3]),
            Board.from_input(params[3:])
        )
    
    def __str__(self) -> str:
        return f"{self.conditions}\n{self.board}\n{self.state}"
    

class GameSolver:
    @staticmethod
    def find_valid_directions(state: GameState) -> list:
        pacman = state.pacman
        current_pos = pacman.get_position()
        valid_directions = []
        for direction in Direction.get_options():
            board_element = state.board.get(
                current_pos + direction
            )
            if board_element and board_element.element not in (Element.WALL, Element.GHOST):
                valid_directions.append(
                    Direction.to_string(Direction(direction))
                )
        return valid_directions
