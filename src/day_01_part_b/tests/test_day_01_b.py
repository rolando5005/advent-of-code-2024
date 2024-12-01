from day_01_part_b.day_01_part_b import Day01PartB

EXAMPLE_INPUT = [
    "3   4",
    "4   3",
    "2   5",
    "1   3",
    "3   9",
    "3   3"
]

def test_day_01_part_b():
    puzzle = Day01PartB()
    puzzle.read_input(EXAMPLE_INPUT)
    puzzle.solve()
    assert puzzle.result == 31
