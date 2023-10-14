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
    
    def __copy__(self):
        return Vector(self.x, self.y)


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