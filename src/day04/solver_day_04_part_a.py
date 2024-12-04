from envireach_logging import Logger
from datetime import datetime

class SolverPartA:
    
    def __init__(self) -> None:
        self._input = None
        self._result = None
    
    def read_input(self, input=None) -> None:
        if input is not None:
            self._input = input
        else:
            with open("input" , "r") as f:
                self._input = f.readlines()

    def solve(self) -> None:
        
        def is_valid(x, y):
            return 0 <= x < rows and 0 <= y < cols

        def search_from(x, y, dx, dy):
            for i in range(word_len):
                nx, ny = x + i * dx, y + i * dy
                if not is_valid(nx, ny) or self._input[nx][ny] != "XMAS"[i]:
                    return False
            return True
        
        self._input = [line.replace("\n", "") for line in self._input]
        rows = len(self._input)
        cols = len(self._input[0])
        word_len = len("XMAS")
        directions = [
            (0, 1),  # right
            (1, 0),  # down
            (1, 1),  # down-right
            (1, -1), # down-left
            (0, -1), # left
            (-1, 0), # up
            (-1, -1),# up-left
            (-1, 1)  # up-right
        ]
        
        self._result = 0
        for x in range(rows):
            for y in range(cols):
                for dx, dy in directions:
                    if search_from(x, y, dx, dy):
                        self._result += 1
        
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
    logger.info("AoC Day 04 Part A:")
    logger.info("Execution time: {} ms".format(time.microseconds/1000))
    logger.info("Answer: {}".format(puzzle.result))
