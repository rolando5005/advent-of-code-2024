from solver_day_09_part_a import SolverPartA
from solver_day_09_part_b import SolverPartB

EXAMPLE_INPUT = [
    "2333133121414131402",
]

def test_solver_day_09_part_a():
    puzzle = SolverPartA()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 1928

def test_solver_day_09_part_b():
    puzzle = SolverPartB()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 2858
