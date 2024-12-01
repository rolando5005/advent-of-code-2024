from day_01_part_a import Day01PartA

EXAMPLE_INPUT = [
    "3   4",
    "4   3",
    "2   5",
    "1   3",
    "3   9",
    "3   3"
]

def test_day_01_part_A():
    puzzle = Day01PartA()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 11
