from envireach_logging import Logger
from datetime import datetime

class SolverPartB:
    
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
        
        def is_safe(lst) -> bool:
            increasing = all(lst[i] <= lst[i + 1] and 1 <= abs(lst[i] - lst[i + 1]) <= 3 for i in range(len(lst) - 1))
            decreasing = all(lst[i] >= lst[i + 1] and 1 <= abs(lst[i] - lst[i + 1]) <= 3 for i in range(len(lst) - 1))
            
            if increasing or decreasing:
                return True
            else:
                # check if removing a single element makes the list safe
                for i in range(len(lst)):
                    new_lst = lst[:i] + lst[i+1:]
                    increasing = all(new_lst[j] <= new_lst[j + 1] and 1 <= abs(new_lst[j] - new_lst[j + 1]) <= 3 for j in range(len(new_lst) - 1))
                    decreasing = all(new_lst[j] >= new_lst[j + 1] and 1 <= abs(new_lst[j] - new_lst[j + 1]) <= 3 for j in range(len(new_lst) - 1))
                    if increasing or decreasing:
                        return True
                return False
                        
        
        self._result = 0
        for line in self._input:
            line = list(map(int, line.split(" ")))  # Convert each element to an integer
            
            if is_safe(line):
                self._result += 1
            
    @property
    def result(self):
        return self._result

if __name__ == "__main__":
    logger = Logger()
    
    puzzle = SolverPartB()
    puzzle.read_input()
    time = datetime.now()
    puzzle.solve()
    time = datetime.now() - time
    logger.info("AoC Day 02 Part B:")
    logger.info("Execution time: {} ms".format(time.microseconds/1000))
    logger.info("Answer: {}".format(puzzle.result))