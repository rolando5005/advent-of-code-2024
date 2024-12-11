import multiprocessing
from turtle import right

from envireach_logging import Logger
from datetime import datetime, timedelta


EXAMPLE_INPUT = [
    "2333133121414131402",
]

class SolverPartB:
    
    def __init__(self) -> None:
        self._input = None
        self._result = None
        self._logger = Logger()
    
    def read_input(self, input=EXAMPLE_INPUT) -> None:
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
        
        def visualize_disk_map(disk_map: list, index:int=0, step:int=1, offset:int=0) -> None:
            # only show the first 20 elements
            msg = ""
            if step > 0:
                start = 0
                end = 60
            else:
                start = 60
                end = 0
            try:
                for i in range(start, end, step):
                    msg += str(disk_map[i + index - offset])
            except IndexError:
                pass
            
            self._logger.info(msg)
        
        def move_numbers_to_left(disk_map: list) -> list:
            right_side_index = len(disk_map) - 1
            left_side_index = 0
            
            time = datetime.now() + timedelta(seconds=1)
            timeout = datetime.now() + timedelta(seconds=60)
            while disk_map[left_side_index] != ".":
                left_side_index += 1
                
            visualize_disk_map(disk_map)
            
            while left_side_index < len(disk_map) - 1:
                if datetime.now() > timeout:
                    break
                
                if datetime.now() > time:
                    self._logger.info("left_side_index: {}".format(left_side_index))
                    visualize_disk_map(disk_map, left_side_index)
                    self._logger.info("right_side_index: {}".format(right_side_index))
                    visualize_disk_map(disk_map, left_side_index, step=-1, offset=-10)
                    time = datetime.now() + timedelta(seconds=1)
                
                digit = disk_map[right_side_index]
                
                if digit == ".":
                    right_side_index -= 1
                    continue
                
                digit_file_size = 1
                while disk_map[right_side_index - digit_file_size] == digit:
                    digit_file_size += 1
                
                empty_block_index = left_side_index
                
                while empty_block_index < right_side_index:
                    if disk_map[empty_block_index] != ".":
                        empty_block_index += 1
                        continue
                
                    empty_space_size = 1
                    while disk_map[empty_block_index + empty_space_size] == ".":
                        empty_space_size += 1

                    if digit_file_size > empty_space_size:
                        # file to big to move to the empty block
                        empty_block_index += digit_file_size
                        continue
                    
                    # able to move the digit to the empty block
                    for i in range(digit_file_size):
                        disk_map[empty_block_index + i] = digit
                        disk_map[right_side_index - i] = "."
                    break
                
                left_side_index = 0
                # while disk_map[left_side_index] != "." and left_side_index < len(disk_map) - 1:
                #     left_side_index += 1
                # while disk_map[right_side_index] != "." and right_side_index > 0:
                #     right_side_index -= 1
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
        # self._logger.info("".join(disk_map))
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
    
    puzzle = SolverPartB()
    puzzle.read_input()
    time = datetime.now()
    puzzle.solve()
    time = datetime.now() - time
    logger.info("AoC Day 09 Part B:")
    logger.info("Execution time: {}".format(format_time(time)))
    logger.info("Answer: {}".format(puzzle.result))

# 6617586836709 too high
