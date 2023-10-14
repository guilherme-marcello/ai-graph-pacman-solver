from pacman.elements import Element, BoardElement

class SuperGum:
    @staticmethod
    def find_all(board) -> list:
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