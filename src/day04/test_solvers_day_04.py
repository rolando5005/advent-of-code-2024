from solver_day_04_part_a import SolverPartA
from solver_day_04_part_b import SolverPartB

EXAMPLE_INPUT = [
    "MMMSXXMASM\n",
    "MSAMXMSMSA\n",
    "AMXSXMAAMM\n",
    "MSAMASMSMX\n",
    "XMASAMXAMM\n",
    "XXAMMXXAMA\n",
    "SMSMSASXSS\n",
    "SAXAMASAAA\n",
    "MAMMMXMMMM\n",
    "MXMXAXMASX"
]

def test_solver_day_04_part_a():
    puzzle = SolverPartA()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 18

def test_solver_day_04_part_b():
    puzzle = SolverPartB()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 9
