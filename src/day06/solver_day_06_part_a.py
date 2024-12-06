from envireach_logging import Logger
from datetime import datetime

class Guard:
    
    def __init__(self, pos_x: int, pos_y: int, direction: str="up") -> None:
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._direction = direction
    
    @property
    def pos_x(self):
        return self._pos_x
    
    @property
    def pos_y(self):
        return self._pos_y
    
    @property
    def direction(self):
        return self._direction

class SolverPartA:
    
    def __init__(self) -> None:
        self._input = None
        self._result = None
        self._logger = Logger()
    
    def read_input(self, input=None) -> None:
        if input is not None:
            self._input = input
        else:
            with open("input" , "r") as f:
                self._input = f.readlines()

    def solve(self) -> None:
        
        def load_map(input: list[str]) -> list[list[str]]:
            map = []
            for line in input:
                map.append(list(line.replace("\n", "")))
            return map
        
        def get_guard_position(map: list[list[str]]) -> tuple[int, int]:
            for y in range(len(map)):
                for x in range(len(map[y])):
                    if map[y][x] == "^":
                        map[y][x] = "X"
                        return (x, y, map)
            return None, None, map
        
        def check_obstacle(map: list[list[str]], guard: Guard) -> tuple[bool, bool]:
            try:
                if guard.direction == "up":
                    return map[guard.pos_y - 1][guard.pos_x] == "#", False
                elif guard.direction == "down":
                    return map[guard.pos_y + 1][guard.pos_x] == "#", False
                elif guard.direction == "left":
                    return map[guard.pos_y][guard.pos_x - 1] == "#", False
                elif guard.direction == "right":
                    return map[guard.pos_y][guard.pos_x + 1] == "#", False
            except IndexError:
                return False, True
        
        def advance_guard(map: list[list[str]], guard: Guard) -> tuple[list[list[str]], Guard, bool]:
            
            def is_border(map: list[list[str]], x: int, y: int) -> bool:
                return x == 0 or x == len(map[y]) - 1 or y == 0 or y == len(map) - 1
            
            try:
                border = False
                if guard.direction == "up":
                    guard._pos_y -= 1
                elif guard.direction == "down":
                    guard._pos_y += 1
                elif guard.direction == "left":
                    guard._pos_x -= 1
                elif guard.direction == "right":
                    guard._pos_x += 1
                
                if is_border(map, guard.pos_x, guard.pos_y):
                    border = True
                
                map[guard.pos_y][guard.pos_x] = "X"
                return map, guard, border
            except IndexError:
                return map, guard, True
        
        def rotate_guard(guard: Guard) -> None:
            if guard.direction == "up":
                guard._direction = "right"
            elif guard.direction == "right":
                guard._direction = "down"
            elif guard.direction == "down":
                guard._direction = "left"
            elif guard.direction == "left":
                guard._direction = "up"
        
        def count_visited(map: list[list[str]]) -> int:
            visited = 0
            for y in range(len(map)):
                for x in range(len(map[y])):
                    if map[y][x] == "X":
                        visited += 1
            return visited
        
        def visualize_map(map: list[list[str]]) -> None:
            for line in map:
                self._logger.info("".join(line))
            self._logger.info("")
        
        map = load_map(self._input)
        x, y, map = get_guard_position(map)
        guard = Guard(x, y, "up")
        
        reached_border = False
        
        while not reached_border:
            facing_obstacle, reached_border = check_obstacle(map, guard)
            if facing_obstacle:
                rotate_guard(guard)
            map, guard, reached_border = advance_guard(map, guard)
        
        # visualize_map(map)
        self._logger.info("Guard position: ({}, {})".format(guard.pos_x, guard.pos_y))
        self._result = count_visited(map)
        
    @property
    def result(self):
        return self._result

if __name__ == "__main__":
    logger = Logger()
    
    puzzle = SolverPartA()
    puzzle.read_input()
    time = datetime.now()
    puzzle.solve()
    time = datetime.now() - time
    logger.info("AoC Day 06 Part A:")
    logger.info("Execution time: {} ms".format(time.microseconds/1000))
    logger.info("Answer: {}".format(puzzle.result))
