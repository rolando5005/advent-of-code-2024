from envireach_logging import Logger
from datetime import datetime

class Day01PartB:
    
    def __init__(self):
        self._input = None
        self._result = None
    
    def read_input(self, input=None):
        if input is not None:
            self._input = input
        else:
            with open("input" , "r") as f:
                self._input = f.readlines()

    def solve(self):
        self._result = 0
        left_list = []
        right_list = []
        for line in self._input:
            left, right = line.split("   ")
            left_list.append(int(left))
            right_list.append(int(right))
        
        left_list = sorted(left_list)
        right_list = sorted(right_list)
        previous_number = None
        
        for i in range(len(left_list)):
            self._result += abs(left_list[i] - right_list[i])

    @property
    def result(self):
        return self._result

if __name__ == "__main__":
    puzzle = Day01PartB()
    logger = Logger()
    
    puzzle.read_input()
    time = datetime.now()
    puzzle.solve()
    time = datetime.now() - time
    logger.info("Execution time: {} ms".format(time.microseconds/1000))
    logger.info("Answer: {}".format(puzzle.result))