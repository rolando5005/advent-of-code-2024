from solver_day_06_part_a import SolverPartA
from solver_day_06_part_b import SolverPartB

EXAMPLE_INPUT = [
    "....#.....\n",
    ".........#\n",
    "..........\n",
    "..#.......\n",
    ".......#..\n",
    "..........\n",
    ".#..^.....\n",
    "........#.\n",
    "#.........\n",
    "......#..."
]

def test_solver_day_05_part_a():
    puzzle = SolverPartA()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 41

# def test_solver_day_05_part_b():
#     puzzle = SolverPartB()
#     puzzle.read_input(EXAMPLE_INPUT)
#     puzzle.solve()
#     assert puzzle.result == 123
