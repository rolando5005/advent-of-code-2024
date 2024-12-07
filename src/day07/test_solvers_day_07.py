from solver_day_07_part_a import SolverPartA
from solver_day_07_part_b import SolverPartB

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

def test_solver_day_07_part_a():
    puzzle = SolverPartA()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 3749

def test_solver_day_07_part_b():
    puzzle = SolverPartB()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 11387
