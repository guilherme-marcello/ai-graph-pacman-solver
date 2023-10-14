from pacman.elements.common import Element, BoardElement, NonStaticElement
from pacman.space import Vector

class Pacman(NonStaticElement):
    def __init__(self, element: BoardElement, steps: int = 0, visited: dict = None) -> None:
        super().__init__(element)
        self.steps = steps
        self.visited_positions = visited if visited else dict()
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
    def from_board(cls, board):
        return super().from_board(
            Element.PACMAN,
            board
        )
    