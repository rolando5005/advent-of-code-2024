from envireach_logging import Logger
from datetime import datetime

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
        
        def get_rule_set() -> list[set[int, int]]:
            rule_set = []
            for line in self._input:
                if "|" not in line or line == "\n":
                    continue
                line = line.replace("\n", "").split("|")
                rule_set.append((int(line[0]), int(line[1])))
            return rule_set
        
        rule_set = get_rule_set()
        
        def check_page_order(page_numbers: list[int]) -> bool:
            for rule in rule_set:
                if not rule[0] in page_numbers:
                    continue
                if not rule[1] in page_numbers:
                    continue
                
                index_x = page_numbers.index(rule[0])
                index_y = page_numbers.index(rule[1])
                if index_x > index_y:
                    return False

            return True
        
        def order_pages(pages: list[int]) -> list[int]:
            for rule in rule_set:
                if not rule[0] in pages:
                    continue
                if not rule[1] in pages:
                    continue
                
                index_x = pages.index(rule[0])
                index_y = pages.index(rule[1])
                if index_x > index_y:
                    pages.pop(index_y)
                    pages.insert(index_x, rule[1])
            return pages

        def get_to_be_updated_pages() -> list[list[int]]:
            to_be_updated_pages = []
            for line in self._input:
                if "|" in line or line == "\n":
                    continue
                
                line = line.replace("\n", "").split(",")
                to_be_updated_pages.append([int(page_number) for page_number in line])
            return to_be_updated_pages
                
        def find_middle_item(lst: list) -> any:
            n = len(lst)
            if n == 0:
                return None  # or raise an exception if the list is empty
            mid_index = n // 2

            return lst[mid_index]
        
        self._result = 0
        ordered_pages = []
        for pages in get_to_be_updated_pages():
            if not check_page_order(pages):
                while not check_page_order(pages):
                    pages = order_pages(pages)
                ordered_pages.append(order_pages(pages))
        
        for re_ordered_pages in ordered_pages:
            self._result += find_middle_item(re_ordered_pages)
        
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
    logger.info("AoC Day 05 Part B:")
    logger.info("Execution time: {} ms".format(time.microseconds/1000))
    logger.info("Answer: {}".format(puzzle.result))