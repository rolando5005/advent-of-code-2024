import re

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
        
        self._result = 0
        for line in self._input:
            matches = re.findall(r"mul\(\d+,\d+\)", line)
            
            for match in matches:
                a, b = map(int, match[4:-1].split(","))
                self._result += a*b
        
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
    logger.info("AoC Day 03 Part A:")
    logger.info("Execution time: {} ms".format(time.microseconds/1000))
    logger.info("Answer: {}".format(puzzle.result))