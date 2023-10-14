from pacman.game.common import GameState
from pacman.elements.common import Element, BoardElement
from pacman.space import Direction

class GameSolver:    
    @staticmethod
    def apply(state: GameState, action: str, max_fear: int):
        direction = Direction.from_string(action)
        current_pos = state.pacman.get_position()
        target_pos = current_pos + direction.vector

        board_element = state.board.get(
            target_pos
        )

        if not board_element or board_element.element in (Element.WALL, Element.GHOST):
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