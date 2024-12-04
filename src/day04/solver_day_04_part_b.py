from envireach_logging import Logger
from datetime import datetime

PATTERNS = [
    [
        "M.M",
        ".A.",
        "S.S"
    ],
    [
        "S.M",
        ".A.",
        "S.M"
    ],
    [
        "S.S",
        ".A.",
        "M.M"
    ],
    [
        "M.S",
        ".A.",
        "M.S"
    ]
]

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
        self._result = 0
        for pattern in PATTERNS:
            rows = len(self._input)
            cols = len(self._input[0].strip())
            pattern_rows = len(pattern)
            pattern_cols = len(pattern[0].strip())
            
            for i in range(rows - pattern_rows + 1):
                for j in range(cols - pattern_cols + 1):
                    match = True
                    for k in range(pattern_rows):
                        for l in range(pattern_cols):
                            if pattern[k][l] != '.' and pattern[k][l] != self._input[i + k][j + l]:
                                match = False
                                break
                        if not match:
                            break
                    if match:
                        self._result += 1
        
    @property
    def result(self):
        return self._result
    @property
    def result(self):
        return self._result
            
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
    logger.info("AoC Day 04 Part B:")
    logger.info("Execution time: {} ms".format(time.microseconds/1000))
    logger.info("Answer: {}".format(puzzle.result))