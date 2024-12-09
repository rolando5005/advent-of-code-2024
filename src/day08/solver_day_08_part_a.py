import multiprocessing

from envireach_logging import Logger
from datetime import datetime, timedelta

EXAMPLE_INPUT = [
    "............\n",
    "........0...\n",
    ".....0......\n",
    ".......0....\n",
    "....0.......\n",
    "......A.....\n",
    "............\n",
    "............\n",
    "........A...\n",
    ".........A..\n",
    "............\n",
    "............"
]

class AntennaMap:
    
    def __init__(self, data: list[str]) -> None:
        self._logger = Logger()
        data = [list(row.strip()) for row in data]
        self._map = data
        self._height = len(data)
        self._width = len(data[0])
    
    def get_antenna_pairs(self) -> list[tuple[int, int]]:
        
        def find_antenna_pairs(antenna_frequency: str) -> list[tuple[int, int]]:
            pairs = []
            for y in range(self._height):
                for x in range(self._width):
                    if self._map[y][x] == antenna_frequency:
                        for y2 in range(self._height):
                            for x2 in range(self._width):
                                if self._map[y2][x2] == antenna_frequency and (x, y) != (x2, y2):
                                    pairs.append(((x, y), (x2, y2)))
                                        
            return pairs
        
        pairs = []
        antenna_frequencies = []
        for y in range(self._height):
            for x in range(self._width):
                if self._map[y][x] != "." and not self._map[y][x] in antenna_frequencies:
                    antenna_frequencies.append(self._map[y][x])
                    pairs.extend(find_antenna_pairs(self._map[y][x]))
        return pairs

    def get_map(self, anti_nodes: list[tuple[int, int]]) -> list[str]:
        map = [list(row) for row in self._map]
        for x, y in anti_nodes:
            try:
                if x >= 0 and y >= 0:
                    map[y][x] = "#"
            except IndexError:
                pass
        return ["".join(row) for row in map]

    def get_row(self, index: int) -> str:
        return "".join(self._map[index])

    @property
    def width(self) -> int:
        return self._width
    
    @property
    def height(self) -> int:
        return self._height

def get_anti_nodes(args) -> list[tuple[int, int]]:
    antenna_1, antenna_2, map_hight, map_width = args
    x1, y1 = antenna_1
    x2, y2 = antenna_2
    
    if x1 == 6 and y1 == 5 and x2 == 8 and y2 == 8:
        pass
    
    dx = x2 - x1
    dy = y2 - y1

    return [(x1 - dx, y1 - dy)]

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
        
        self._result = 0
        antenna_map = AntennaMap(self._input)
        antenna_pairs = antenna_map.get_antenna_pairs()
        input = [(antenna_1, antenna_2, antenna_map.width, antenna_map.height) for antenna_1, antenna_2 in antenna_pairs]
        
        with multiprocessing.Pool() as pool:
            results = pool.map(get_anti_nodes, input)
            result = [item for sublist in results for item in sublist]
            
        self._logger.info("Found Anti-nodes: {}".format((len(result))))
        self._logger.info("Anti-nodes: {}".format(result))
        map = antenna_map.get_map(result)

        self._logger.info("Map with Anti-nodes:")
        for index, row in enumerate(map):
            self._logger.info("{} | {}".format(row, antenna_map.get_row(index)))
            for spot in row:
                if spot == "#":
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
    
    puzzle = SolverPartA()
    puzzle.read_input()
    time = datetime.now()
    puzzle.solve()
    time = datetime.now() - time
    logger.info("AoC Day 08 Part A:")
    logger.info("Execution time: {}".format(format_time(time)))
    logger.info("Answer: {}".format(puzzle.result))

# 166 too low
# 209 too low
# 263 not correct
# 278 too high