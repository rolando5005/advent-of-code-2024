import multiprocessing

from envireach_logging import Logger
from datetime import datetime, timedelta
from copy import deepcopy


class Guard:
    
    def __init__(self, pos_x: int, pos_y: int, direction: str="up") -> None:
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._direction = direction
        self._start_position = (pos_x, pos_y)
    
    @property
    def pos_x(self) -> int:
        return self._pos_x
    
    @property
    def pos_y(self) -> int:
        return self._pos_y
    
    @property
    def direction(self) -> str:
        return self._direction
    
    @property
    def start_position(self) -> tuple[int, int]:
        return self._start_position

class GuardMap: 
    
    def __init__(self, map: list[list[str]], guard: Guard) -> None:
        self._map = map
        self._guard = guard
        self._obstacle_locations = []
        self._logger = Logger()

    def is_guard_facing_obstacle(self) -> bool:
        try:
            if self._guard.direction == "up":
                return self._map[self._guard.pos_y - 1][self._guard.pos_x] in ["#", "O"]
            elif self._guard.direction == "down":
                return self._map[self._guard.pos_y + 1][self._guard.pos_x] in ["#", "O"]
            elif self._guard.direction == "left":
                return self._map[self._guard.pos_y][self._guard.pos_x - 1] in ["#", "O"]
            elif self._guard.direction == "right":
                return self._map[self._guard.pos_y][self._guard.pos_x + 1] in ["#", "O"]
        except IndexError:
            return False
    
    def guard_reached_each_map_border(self) -> bool:
        return self._guard.pos_x == 0 or self._guard.pos_x == len(self._map[0]) - 1 or self._guard.pos_y == 0 or self._guard.pos_y == len(self._map) - 1
    
    def guard_advance(self) -> None:
        self._map[self._guard.pos_y][self._guard.pos_x] = "X"
        if self._guard.direction == "up":
            self._guard._pos_y -= 1
        elif self._guard.direction == "down":
            self._guard._pos_y += 1
        elif self._guard.direction == "left":
            self._guard._pos_x -= 1
        elif self._guard.direction == "right":
            self._guard._pos_x += 1
    
    def guard_rotate(self) -> None:
        if self._guard.direction == "up":
            self._obstacle_locations.append((self._guard.pos_x, self._guard.pos_y + 1))
            self._guard._direction = "right"
        elif self._guard.direction == "right":
            self._obstacle_locations.append((self._guard.pos_x + 1, self._guard.pos_y))
            self._guard._direction = "down"
        elif self._guard.direction == "down":
            self._obstacle_locations.append((self._guard.pos_x, self._guard.pos_y - 1))
            self._guard._direction = "left"
        elif self._guard.direction == "left":
            self._obstacle_locations.append((self._guard.pos_x - 1, self._guard.pos_y))
            self._guard._direction = "up"
    
    def check_if_seen_obstacle_before(self) -> bool:
        if self._guard.direction == "up":
            obstacle_location = (self._guard.pos_x, self._guard.pos_y + 1)
        elif self._guard.direction == "right":
            obstacle_location = (self._guard.pos_x + 1, self._guard.pos_y)
        elif self._guard.direction == "down":    
            obstacle_location = (self._guard.pos_x, self._guard.pos_y - 1)
        elif self._guard.direction == "left":
            obstacle_location = (self._guard.pos_x - 1, self._guard.pos_y)
        
        return self._obstacle_locations.count(obstacle_location) > 9
    
    def check_for_loop(self) -> bool:
        while not self.guard_reached_each_map_border():
            while self.is_guard_facing_obstacle():
                if self.check_if_seen_obstacle_before():
                    return True
                self.guard_rotate()
                
            self.guard_advance()
        return False

    def get_positions_to_place_obstacle(self) -> list[tuple[int, int]]:
        self._logger.info("Starting to traverse the map")
        while not self.guard_reached_each_map_border():
            if self.is_guard_facing_obstacle():
                self.guard_rotate()
            self.guard_advance()
        
        self._logger.info("Traversing the map is done")
        self._logger.info("Starting to find positions to place the obstacle")
        positions = []
        for y in range(len(self._map)):
            for x in range(len(self._map[y])):
                if self._map[y][x] == ".":
                    if y > 0 and self._map[y - 1][x] == "X":
                        positions.append((x, y))
                    elif y < len(self._map) - 1 and self._map[y + 1][x] == "X":
                        positions.append((x, y))
                    elif x > 0 and self._map[y][x - 1] == "X":
                        positions.append((x, y))
                    elif x < len(self._map[y]) - 1 and self._map[y][x + 1] == "X":
                        positions.append((x, y))
                    elif self._map[y][x] == "X":
                        positions.append((x, y))
                elif self._map[y][x] == "X":
                    positions.append((x, y))
        self._logger.info("Finding positions to place the obstacle is done")
        self._logger.info("Positions to place the obstacle: {}".format(len(positions)))
        return positions

    def visual_map(self, map: list[list[str]]=None) -> None:
        if map is None:
            map = self._map
        
        for line in map:
            self._logger.info("".join(line))
        self._logger.info("")

def process_guard_map(args) -> bool:
    obstacle_pos, guard_start_pos, map  = args
    map_with_obstacle = deepcopy(map)
    map_with_obstacle[obstacle_pos[1]][obstacle_pos[0]] = "O"
    guard_map = GuardMap(map_with_obstacle, Guard(*guard_start_pos))
    return guard_map.check_for_loop(), map_with_obstacle

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
                        return (x, y)
            return None, None
        
        self._result = 0
        map = load_map(self._input)
        x, y = get_guard_position(map)
        guard_map = GuardMap(deepcopy(map), Guard(x, y))
        positions = [(pos, (x, y), map) for pos in guard_map.get_positions_to_place_obstacle()]
        
        self._logger.info("Checking for loops...")
        with multiprocessing.Pool() as pool:
            results = pool.map(process_guard_map, positions)
        
        for found_loop, traveled_map in results:
            if found_loop:
                # guard_map.visual_map(traveled_map)
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
# 1485 not correct
# 1517 not correct
# 1518 not correct
# 1575 correct
# 1659 not correct
# 2031 not correct
# 2154 ...
# 4220 not correct
# 45.. too high