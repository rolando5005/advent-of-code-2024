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
        self._height = len(data) - 1
        self._width = len(data[0]) - 1
    
    def get_antenna_pairs(self) -> list[tuple[int, int]]:
        
        def check_for_line_of_sight(antenna_1: tuple[int, int], antenna_2: tuple[int, int]) -> bool:
            x1, y1 = antenna_1
            x2, y2 = antenna_2
            
            dx = x2 - x1
            dy = y2 - y1
            steps = max(abs(dx), abs(dy))
            x_step = dx / steps
            y_step = dy / steps

            line_of_sight = True
            for i in range(1, steps):
                x = x1 + round(i * x_step)
                y = y1 + round(i * y_step)
                if self._map[y][x] != '.':
                    block_line_of_sight = self._map[y][x]
                    line_of_sight = False
                    break
            
            # if line_of_sight == False:
            #     self._logger.info("No line of sight between {} and {} due to {}".format(antenna_1, antenna_2, block_line_of_sight))
            # self._logger.info("Line of sight: {}".format(line_of_sight))
            return line_of_sight
        
        def find_antenna_pairs(antenna_frequency: str) -> list[tuple[int, int]]:
            pairs = []
            for y in range(self._height):
                for x in range(self._width):
                    if self._map[y][x] == antenna_frequency:
                        for y2 in range(self._height):
                            for x2 in range(self._width):
                                if self._map[y2][x2] == antenna_frequency and (x, y) != (x2, y2):
                                    if check_for_line_of_sight((x, y), (x2, y2)):
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
                if map[y][x] == ".":  # Empty
                    map[y][x] = "#"
            except IndexError:
                pass
        return ["".join(row) for row in map]

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
    
    # Calculate the direction vector
    dir_x = x2 - x1
    dir_y = y2 - y1
    
    # Normalize the direction vector
    length = (dir_x ** 2 + dir_y ** 2) ** 0.5
    norm_dir_x = dir_x / length
    norm_dir_y = dir_y / length
    
    # Calculate the anti-nodes
    anti_nodes = []
    index = 2
    out_of_map_1 = False
    out_of_map_2 = False
    while index == 2:
        scaled_dir_x = norm_dir_x * length * index
        scaled_dir_y = norm_dir_y * length * index
        
        new_x_1 = x1 + int(scaled_dir_x)
        new_y_1 = y1 + int(scaled_dir_y)
        
        anti_nodes.append((new_x_1, new_y_1))
        
        break
        
        if out_of_map_1 == False and 0 <= new_x_1 <= map_width and 0 <= new_y_1 <= map_hight:
            anti_nodes.append((new_x_1, new_y_1))
        else:
            out_of_map_1 = True
            
        if out_of_map_2 == False == 0 <= new_x_2 <= map_width and 0 <= new_y_2 <= map_hight:
            anti_nodes.append((new_x_2, new_y_2))
        else:
            out_of_map_2 = True
        
        if out_of_map_1 and out_of_map_2:
            break
        index += 1
    
    return anti_nodes

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
        
        def filter_result(result: list[tuple[int, int]]) -> list[tuple[int, int]]:
            filtered_result = []
            for anti_node in result:
                if not anti_node in filtered_result and 0 <= anti_node[0] <= antenna_map.width and 0 <= anti_node[1] <= antenna_map.height:
                    filtered_result.append(anti_node)
                else:
                    if not 0 <= anti_node[0] <= antenna_map.width or not 0 <= anti_node[1] <= antenna_map.height:
                        self._logger.info("Filtered out of bounds Anti-node: {}".format(anti_node))
                    elif anti_node in filtered_result:
                        self._logger.info("Filtered duplicate Anti-node: {}".format(anti_node))
            return filtered_result
        
        self._result = 0
        antenna_map = AntennaMap(self._input)
        antenna_pairs = antenna_map.get_antenna_pairs()
        input = [(antenna_1, antenna_2, antenna_map.width, antenna_map.height) for antenna_1, antenna_2 in antenna_pairs]
        
        with multiprocessing.Pool(1) as pool:
            results = pool.map(get_anti_nodes, input)
            result = [item for sublist in results for item in sublist]
            
        self._logger.info("Found Anti-nodes: {}".format((result)))
        
        result = filter_result(result)
        # self._logger.info("Filtered Anti-nodes: {}".format(result))
        map = antenna_map.get_map(result)
        self._logger.info("Map with Anti-nodes:")
        for row in map:
            self._logger.info(row)
        
        self._result = len(result)
        
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

# 209 too low
# 278 too high