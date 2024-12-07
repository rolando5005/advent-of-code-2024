import multiprocessing
from time import sleep
from webbrowser import get

from envireach_logging import Logger
from datetime import datetime, timedelta
from copy import deepcopy

EXAMPLE_INPUT = [
    "....#.....\n",
    ".........#\n",
    "..........\n",
    "..#.......\n",
    ".......#..\n",
    "..........\n",
    ".#..^.....\n",
    "........#.\n",
    "#.........\n",
    "......#..."
]

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

def check_obstacle(map: list[list[str]], guard: Guard) -> tuple[bool, bool, bool]:
    try:
        if guard.direction == "up":
            return map[guard.pos_y - 1][guard.pos_x] in ["#", "O"], False
        elif guard.direction == "down":
            return map[guard.pos_y + 1][guard.pos_x] in ["#", "O"], False
        elif guard.direction == "left":
            return map[guard.pos_y][guard.pos_x - 1] in ["#", "O"], False
        elif guard.direction == "right":
            return map[guard.pos_y][guard.pos_x + 1] in ["#", "O"], False
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

def check_placed_obstacle(map: list[list[str]], guard: Guard) -> bool:
    if guard.direction == "up":
        return map[guard.pos_y - 1][guard.pos_x] == "O"
    elif guard.direction == "down":
        return map[guard.pos_y + 1][guard.pos_x] == "O"
    elif guard.direction == "left":
        return map[guard.pos_y][guard.pos_x - 1] == "O"
    elif guard.direction == "right":
        return map[guard.pos_y][guard.pos_x + 1] == "O"

def get_placed_obstacle(guard: Guard) -> tuple[int, int]:
    if guard.direction == "up":
        return guard.pos_x, guard.pos_y - 1
    elif guard.direction == "down":
        return guard.pos_x, guard.pos_y + 1
    elif guard.direction == "left":
        return guard.pos_x - 1, guard.pos_y
    elif guard.direction == "right":
        return guard.pos_x + 1, guard.pos_y

def check_for_loop(map: list[list[str]], guard: Guard) -> bool:
    logger = Logger()
    reached_border = False
    location_placed_obstacle = None
    location_seen_obstacles = []
    time = datetime.now() + timedelta(seconds=5)
    while not reached_border:
        
        facing_obstacle, reached_border = check_obstacle(map, guard)
        if facing_obstacle == True:
            location_seen_obstacle = get_placed_obstacle(guard)
            
            if location_placed_obstacle is None and check_placed_obstacle(map, guard):
                location_placed_obstacle = get_placed_obstacle(guard)
            
            if location_seen_obstacle in location_seen_obstacles and location_placed_obstacle is not None:
                logger.info("Found loop at {}, {}".format(location_seen_obstacle[0], location_seen_obstacle[1]))
                return True
            else:
                location_seen_obstacles.append(location_seen_obstacle)
            
            # if location_placed_obstacle is None and check_placed_obstacle(map, guard):
            #     location_placed_obstacle = get_placed_obstacle(guard)
            # elif location_placed_obstacle == get_placed_obstacle(guard):
            #     pos_x, pos_y = get_placed_obstacle(guard)
            #     logger.info("Found loop at {}, {}".format(pos_x, pos_y))
            #     return True
                
            rotate_guard(guard)
        map, guard, reached_border = advance_guard(map, guard)
        
        if time < datetime.now():
            time = datetime.now() + timedelta(seconds=20)
            pos_x, pos_y = get_placed_obstacle(guard)
            logger.info("timeout reached at {}, {}".format(pos_x, pos_y))
            return False
    return False

def visualize_map(map: list[list[str]]) -> None:
    for line in map:
        logger.info("".join(line))
    logger.info("")

def process_position(args):
    pos_x, pos_y, map, guard = args
    used_map = deepcopy(map)
    used_map[pos_y][pos_x] = "O"
    if check_for_loop(used_map, guard):
        return pos_x, pos_y, True
    return pos_x, pos_y, False

class SolverPartB:
    
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

        self._result = 0
        
        map = load_map(self._input)
        x, y, map = get_guard_position(map)

        positions = [(pos_x, pos_y, map, Guard(x, y, "up")) for pos_y, map_y in enumerate(map) for pos_x, value in enumerate(map_y) if value == "."]

        with multiprocessing.Pool() as pool:
            results = pool.map(process_position, positions)

        locations = []
        for pos_x, pos_y, found_loop in results:
            location = (pos_x, pos_y)
            if location in locations:
                self._logger("Found duplicate location")
                continue
            
            locations.append(location)
            if found_loop:
                self._result += 1
        
    @property
    def result(self):
        return self._result

def format_time(time: timedelta) -> str:
    total_seconds = int(time.total_seconds())
    milliseconds = int(time.microseconds / 1000)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}:{milliseconds:03}"

if __name__ == "__main__":
    logger = Logger()
    
    puzzle = SolverPartB()
    puzzle.read_input()
    time = datetime.now()
    puzzle.solve()
    time = datetime.now() - time
    logger.info("AoC Day 06 Part B:")
    logger.info("Execution time: {}".format(format_time(time)))
    logger.info("Answer: {}".format(puzzle.result))
    

# 1457 not correct
# 1518 not correct
# 2031 not correct
# 45.. too high