from solver_day_10_part_a import SolverPartA
from solver_day_10_part_b import SolverPartB

EXAMPLE_INPUT = [
    "0123",
    "1234",
    "8765",
    "9876"
]

LARGER_EXAMPLE_INPUT = [
    "89010123",
    "78121874",
    "87430965",
    "96549874",
    "45678903",
    "32019012",
    "01329801",
    "10456732"
]

def test_solver_day_10_part_a():
    puzzle = SolverPartA()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 1
    
    puzzle.read_input(LARGER_EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 36

def test_solver_day_10_part_b():
    puzzle = SolverPartB()
    puzzle.read_input(LARGER_EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 81