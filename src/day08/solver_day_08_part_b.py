import multiprocessing
import re

from envireach_logging import Logger
from datetime import datetime, timedelta

EXAMPLE_INPUT = [
    "190: 10 19\n",
    "3267: 81 40 27\n",
    "83: 17 5\n",
    "156: 15 6\n",
    "7290: 6 8 6 15\n",
    "161011: 16 10 13\n",
    "192: 17 8 14\n",
    "21037: 9 7 18 13\n",
    "292: 11 6 16 20"
]

def check_equation(args) -> int:
    equation, answer = args
    logger = Logger()

    def helper(index, current_value, operations) -> bool:
        if index == len(equation):
            if current_value == answer:
                # logger.info("Equation: {} = {}".format(operations, answer))
                return True
            return False

        # Try adding the next number
        if helper(index + 1, current_value + equation[index], operations + f" + {equation[index]}"):
            return True

        # Try multiplying the next number
        if helper(index + 1, current_value * equation[index], operations + f" * {equation[index]}"):
            return True

        # Try concatenating the next number
        if index < len(equation):
            concatenated_value = int(str(current_value) + str(equation[index]))
            if helper(index + 1, concatenated_value, operations + f" || {equation[index]}"):
                return True

        return False

    # Start the recursion with the first number in the equation
    if helper(1, equation[0], str(equation[0])):
        return answer
    else:
        return 0

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
        
        potential_calibrations = []
        for line in self._input:
            line = line.strip()
            answer, equation = line.split(":")
            equation = [int(number) for number in re.findall(r"\d+", equation)]
            potential_calibrations.append((equation, int(answer)))
        
        with multiprocessing.Pool() as pool:
            result = pool.map(check_equation, potential_calibrations)
        
        self._result = sum(result)
        
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
    logger.info("AoC Day 07 Part B:")
    logger.info("Execution time: {}".format(format_time(time)))
    logger.info("Answer: {}".format(puzzle.result))
