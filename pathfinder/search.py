from typing import List, Optional

from pathfinder.util import CalculatedDistances, PositionsPath
from pathfinder.common import Position, PositionDistance, Path, AdjanceData

class PathSearchContext:
    """
    Класс поиска путей

    Реализует алгоритмы поиска путей и хранит данные об уже найденных путях для повторного использования.
    При изменении связей или дистанций между позициями контекст может потерять актуальность, в связи с чем дальнейшая работа с ним может привести к неверным результатам
    """
    def __init__(self, adjance_data : Optional[AdjanceData] = None) -> None:
        self.__calculated : CalculatedDistances = CalculatedDistances(adjance_data)
        return

    def find_path(self, pos1 : Position, pos2 : Position, max_steps : Optional[int] = None) -> Path:
        """
        Поиск кратчайшего пути между позициями

        pos1 - начальная позиция, от неё будет распространяться поиск, повторный поиск от этой вершины до другой выполнится быстрее
        pos2 - конечная позиция
        max_steps - наибольшее количество вершин, которые может рассмотреть алгоритм (None - без ограничений)
        В результате вернётся либо кратчайший путь либо пустой, если поиск не увенчался успехом
        """
        calc = self.__calculated.get_calculated_from(pos1)
        path = calc.path_to(pos2)
        if (not path.empty()):
            p = Path()
            p.steps = path.steps.copy()
            p.length = path.length
            return p
        step = 0
        while ((max_steps == None) or (step < max_steps)):
            new_pos = calc.advance()
            if (new_pos == None):
                break
            if (new_pos == pos2):
                path = calc.path_to(pos2)
                p = Path()
                p.steps = path.steps.copy()
                p.length = path.length
                return p
            step += 1
        return Path()

    def calculated_distances(self, position : Position) -> List[PositionDistance]:
        return self.__calculated.calculated_to(position)
