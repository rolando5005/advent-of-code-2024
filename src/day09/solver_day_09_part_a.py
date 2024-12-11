from envireach_logging import Logger
from datetime import datetime, timedelta

EXAMPLE_INPUT = [
    "2333133121414131402",
]

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
        
        def get_disk_map() -> list:
            disk_map = []
            index = 0
            size_disk_map = len(self._input[0])
            for disk_position in range(0, size_disk_map, 2):
                file = int(self._input[0][disk_position])
                for i in range(file):
                    disk_map.append(str(index))
                
                if disk_position + 1 < size_disk_map:
                    free_space = int(self._input[0][disk_position + 1])
                    if free_space > 0:
                        for i in range(free_space):
                            disk_map.append(".")
                
                index += 1
            return disk_map
        
        def move_numbers_to_left(disk_map: list) -> list:
            right_side_index = len(disk_map) - 1
            left_side_index = 0
            
            while left_side_index < right_side_index:
                if disk_map[left_side_index] == ".":
                    while True:
                        digit = disk_map[right_side_index]
                        if digit != ".":
                            disk_map[left_side_index] = digit
                            disk_map[right_side_index] = "."
                            break
                        right_side_index -= 1

                left_side_index += 1
            return disk_map

        
        def get_checksum(disk_map: list) -> int:
            checksum = 0
            for index, digit in enumerate(disk_map):
                if digit == ".":
                    continue
                checksum += int(digit) * (index)
            return checksum
        
        disk_map = get_disk_map()
        disk_map = move_numbers_to_left(disk_map)
        self._result = get_checksum(disk_map)     

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
    logger.info("AoC Day 09 Part A:")
    logger.info("Execution time: {}".format(format_time(time)))
    logger.info("Answer: {}".format(puzzle.result))

# 166 too low
# 209 too low
# 263 not correct
# 278 too high