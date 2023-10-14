from pacman.elements import Pacman, Ghost, SuperGum
from pacman.game import Board

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