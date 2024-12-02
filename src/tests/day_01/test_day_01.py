from day01.solver_part_a import SolverPartA
from day01.solver_part_b import solverPartB

EXAMPLE_INPUT = [
    "3   4",
    "4   3",
    "2   5",
    "1   3",
    "3   9",
    "3   3"
]

def test_puzzle_day_01_part_1():
    puzzle = SolverPartA()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 11

def test_puzzle_day_01_part_2():
    puzzle = solverPartB()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 31
