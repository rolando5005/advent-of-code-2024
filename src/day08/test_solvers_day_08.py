from solver_day_08_part_a import SolverPartA
from solver_day_08_part_b import SolverPartB

EXAMPLE_INPUT = [
    "............\n",
    "........0...\n",
    ".....0......\n",
    ".......0....\n",
    "....0.......\n",
    "......A.....\n",
    "............\n",
    "............\n",
    "........A...\n",
    ".........A..\n",
    "............\n",
    "............"
]

def test_solver_day_08_part_a():
    puzzle = SolverPartA()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 14

def test_solver_day_08_part_b():
    puzzle = SolverPartB()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 34
