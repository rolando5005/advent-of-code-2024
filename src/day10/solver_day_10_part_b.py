from collections import deque

from envireach_logging import Logger
from datetime import datetime, timedelta

EXAMPLE_INPUT = [
    "0123",
    "1234",
    "8765",
    "9876"
]

LARGER_EXAMPLE_INPUT = [
    "89010123",
    "78121874",
    "87430965",
    "96549874",
    "45678903",
    "32019012",
    "01329801",
    "10456732"
]

class HikingMap:
    
    def __init__(self, input: list[str]) -> None:
        self._hiking_map = []
        for line in input:
            self._hiking_map.append([int(char) for char in line.strip()])
        
    def get_trailheads(self) -> list[tuple[int, int]]:
        trailheads = []
        for i in range(len(self._hiking_map)):
            for j in range(len(self._hiking_map[i])):
                if self._hiking_map[i][j] == 0:
                    trailheads.append((i, j))
        return trailheads

    def find_trails(self, trailhead: tuple[int, int]) -> int:
        rows, cols = len(self._hiking_map), len(self._hiking_map[0])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        queue = deque([(trailhead, [(trailhead)])])
        trails = 0

        while queue:
            (x, y), path = queue.popleft()
            current_height = self._hiking_map[x][y]

            if current_height == 9:
                trails += 1
                continue

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in path:
                    next_height = self._hiking_map[nx][ny]
                    if next_height == current_height + 1:
                        queue.append(((nx, ny), path + [(nx, ny)]))

        return trails

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
        self._result = 0
        
        hiking_map = HikingMap(self._input)
        trailheads = hiking_map.get_trailheads()
        
        for trailhead in trailheads:
            self._result += hiking_map.find_trails(trailhead)

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
    logger.info("AoC Day 09 Part B:")
    logger.info("Execution time: {}".format(format_time(time)))
    logger.info("Answer: {}".format(puzzle.result))