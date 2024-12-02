from solver_part_a import SolverPartA
from solver_part_b import SolverPartB

EXAMPLE_INPUT = [
    "7 6 4 2 1",
    "1 2 7 8 9",
    "9 7 6 2 1",
    "1 3 2 4 5",
    "8 6 4 4 1",
    "1 3 6 7 9"
]

def test_solver_day_01_part_a():
    puzzle = SolverPartA()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 2

# def test_solver_day_01_part_b():
#     puzzle = SolverPartB()
#     puzzle.read_input(EXAMPLE_INPUT)
#     puzzle.solve()
#     assert puzzle.result == None
