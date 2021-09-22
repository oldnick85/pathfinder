import pathfinder
from typing import Set, List

from pathfinder.common import Position, PositionDistance
from pathfinder.search import PathSearchContext

class TestPosition(Position):
    def __init__(self, name : str) -> None:
        Position.__init__(self)
        self.__name = name
        return

    def __str__(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return self.__name

class TestPositionStart(TestPosition):
    def __init__(self, name : str) -> None:
        TestPosition.__init__(self, name)
        return

    def set(self, branch1 : PositionDistance, branch2 : PositionDistance, branch3 : PositionDistance, branch4 : PositionDistance) -> None:
        self.__adj : Set[PositionDistance] = {branch1, branch2, branch3, branch4}
        return

    def get_adjacent(self) -> Set[PositionDistance]:
        return self.__adj

class TestPositionEnd(TestPosition):
    def __init__(self, name : str) -> None:
        TestPosition.__init__(self, name)
        return

    def set(self, branch1 : PositionDistance, branch2 : PositionDistance, branch3 : PositionDistance) -> None:
        self.__adj = {branch1, branch2, branch3}
        return

    def get_adjacent(self) -> Set[PositionDistance]:
        return self.__adj

class TestPositionBranch(TestPosition):
    def __init__(self, name : str) -> None:
        TestPosition.__init__(self, name)
        return

    def set(self, p1 : PositionDistance, p2 : PositionDistance) -> None:
        self.__adj = {p1, p2}
        return

    def get_adjacent(self) -> Set[PositionDistance]:
        return self.__adj

class TestSimple:
    def __init__(self) -> None:
        return

    def test(self) -> None:
        ps_start = TestPositionStart("START")
        ps_end = TestPositionEnd("END")
        ps_b1_1 = TestPositionBranch("B_1_1")
        ps_b1_2 = TestPositionBranch("B_1_2")
        ps_b2_1 = TestPositionBranch("B_2_1")
        ps_b2_2 = TestPositionBranch("B_2_2")
        ps_b3_1 = TestPositionBranch("B_3_1")
        ps_b3_2 = TestPositionBranch("B_3_2")
        ps_b4_1 = TestPositionBranch("B_4_1")
        ps_b4_2 = TestPositionBranch("B_4_2")
        ps_start.set(PositionDistance(ps_b1_1, 1.0), PositionDistance(ps_b2_1, 1.0), PositionDistance(ps_b3_1, 1.0), PositionDistance(ps_b4_1, 1.0))
        ps_end.set(PositionDistance(ps_b1_2, 1.0), PositionDistance(ps_b2_2, 1.0), PositionDistance(ps_b3_2, 1.0))
        ps_b1_1.set(PositionDistance(ps_start, 1.0), PositionDistance(ps_b1_2, 0.5))
        ps_b1_2.set(PositionDistance(ps_b1_1, 0.5), PositionDistance(ps_end, 1.0))
        ps_b2_1.set(PositionDistance(ps_start, 1.0), PositionDistance(ps_b2_2, 0.6))
        ps_b2_2.set(PositionDistance(ps_b2_1, 0.6), PositionDistance(ps_end, 1.0))
        ps_b3_1.set(PositionDistance(ps_start, 1.0), PositionDistance(ps_b3_2, 0.7))
        ps_b3_2.set(PositionDistance(ps_b3_1, 0.7), PositionDistance(ps_end, 1.0))
        ps_b4_1.set(PositionDistance(ps_start, 1.0), PositionDistance(ps_b4_2, 0.2))
        ps_b4_2.set(PositionDistance(ps_b4_1, 0.2), PositionDistance(ps_end, 1.0))
        path_ctx = PathSearchContext()
        path = path_ctx.find_path(ps_start, ps_end)
        print(path.steps)
        print(path.length)
        return

def main():
    print(f"TESTING PATHFINDER {pathfinder.__version__} START")
    test = TestSimple()
    test.test()
    print(f"TESTING PATHFINDER {pathfinder.__version__} END")
    return


if __name__ == "__main__":
    main()
