from typing import List, Optional, Set
from pathfinder.common import Position, PositionDistance, Path, AdjanceData

class PositionsPath(Path):
    """
    Путь между позициями
    """
    def __init__(self) -> None:
        Path.__init__(self)
        return

    def __str__(self) -> str:
        s = "PATH"
        for p in self.steps:
            s += f"-{p}"
        return s

    def empty(self) -> bool:
        return (len(self.steps) == 0)

    def add_adjacent(self, adjanced : PositionDistance) -> None:
        """
        Добавить новый шаг к пути
        """
        self.steps.insert(0, adjanced.get_position())
        self.length += adjanced.get_distance()
        return

class CalculatedForPosition:
    """
    Класс расстояний, найденных относительно некоторой позиции
    """
    def __init__(self, pos : Position, adjance_data : Optional[AdjanceData] = None) -> None:
        self.__from_position : Position = pos                                           # позиция, относительно которой ищутся расстояния
        self.__adjance_data = adjance_data                                              # объект данных о соседних позициях (если не задан, то соседние позиции запрашиваются у самой позиции)
        self.__calculated : Set[PositionDistance] = set([PositionDistance(pos, 0.0)])   # точки с найденными до них минимальными расстояниями
        self.__border : Set[PositionDistance] = self.__get_adjacent(pos).copy()         # граница множества найденных точек (расстояния не являются минимальными)
        return

    def __get_adjacent(self, pos : Position) -> Set[PositionDistance]:
        """
        Получить соседние позиции для данной позиции

        вызывает функцию объекта данных о соседних позициях или функцию самой позиции
        """
        if (self.__adjance_data != None):
            return self.__adjance_data.get_adjacent(pos)
        return pos.get_adjacent()

    def path_to(self, pos : Position) -> PositionsPath:
        """
        Построить путь до указанной позиции

        строит путь на основе рассчитанных данных о расстояниях
        """
        path = PositionsPath()
        pd : Optional[PositionDistance] = self.__find_calculated(pos)
        if (pd != None):
            path.add_adjacent(pd)
            cur_pos = pd.get_position()
            while (cur_pos != self.__from_position):
                adj_pd = self.__get_adjacent(cur_pos).copy()
                adj_positions = [self.__find_calculated(p.get_position()) for p in adj_pd]
                adj_positions = list(filter(lambda pd : pd != None, adj_positions))
                closest = min(adj_positions, key = (lambda pd : pd.get_distance()))
                path.add_adjacent(closest)
                cur_pos = closest.get_position()
        return path

    def is_from(self, pos : Position) -> bool:
        return (self.__from_position == pos)

    def __closest_border(self) -> Optional[PositionDistance]:
        """
        Получить граничную позицию с наименьшим расстоянием
        """
        closest_border : Optional[PositionDistance] = None
        for border_pos in self.__border:
            if (closest_border == None) or (border_pos.get_distance() < closest_border.get_distance()):
                closest_border = border_pos
        return closest_border

    def calculated_to(self, pos : Position) -> Optional[PositionDistance]:
        """
        Получить расстояние, рассчитанное для указанной позиции

        результат: стартовая позиция и расстояние до указанной 
        или None, если для указанной позиции расстояние не вычислено
        """
        pd = self.__find_calculated(pos)
        if (pd != None):
            return PositionDistance(self.__from_position, pd.get_distance())
        return None

    def __find_calculated(self, pos : Position) -> Optional[PositionDistance]:
        for pd in self.__calculated:
            if (pd.get_position() == pos):
                return pd
        return None

    def __find_border(self, pos : Position) -> Optional[PositionDistance]:
        for pd in self.__border:
            if (pd.get_position() == pos):
                return pd
        return None

    def advance(self) -> Optional[Position]:
        """
        Обработка ещё одной вершины

        результатом является 
        позиция, добавленная к множеству обработанных, 
        либо Null, если такой позиции не нашлось
        """
        border_pos = self.__closest_border()
        if (border_pos == None):
            return None
        self.__calculated.add(border_pos)
        self.__border.remove(border_pos)
        adj = self.__get_adjacent(border_pos.get_position()).copy()
        for pd in adj:
            if (self.__find_calculated(pd.get_position()) == None):
                pd_b = self.__find_border(pd.get_position())
                if (pd_b == None):
                    new_distance = pd.get_distance() + border_pos.get_distance()
                    self.__border.add(PositionDistance(pd.get_position(), new_distance))
                else:
                    new_distance = border_pos.get_distance() + pd.get_distance()
                    if (pd_b.get_distance() > new_distance):
                        pd_b_pos = pd_b.get_position()
                        self.__border.remove(pd_b)
                        self.__border.add(PositionDistance(pd_b_pos, new_distance))
        return border_pos.get_position()

class CalculatedDistances:
    """
    Класс найденных расстояний
    """
    def __init__(self, adjance_data : Optional[AdjanceData] = None) -> None:
        self.__calculated : Set[CalculatedForPosition] = set()      # множество точек с найденными от них расстояниями
        self.__adjance_data = adjance_data                          # объект данных о соседних позициях (если не задан, то соседние позиции запрашиваются у самой позиции)
        return

    def __find_calculated_from(self, pos : Position) -> Optional[CalculatedForPosition]:
        for calc in self.__calculated:
            if (calc.is_from(pos)):
                return calc
        return None

    def get_calculated_from(self, pos : Position) -> CalculatedForPosition:
        """
        Получить расстояния, найденные относительно указанной позиции

        если соответствующего объекта не существует, то он создаётся
        """
        calc = self.__find_calculated_from(pos)
        if (calc == None):
            calc = CalculatedForPosition(pos, self.__adjance_data)
            self.__calculated.add(calc)
        return calc

    def calculated_to(self, pos : Position) -> List[PositionDistance]:
        """
        Получить расстояния, рассчитанные для указанной позиции

        результат: список стартовых позиций и расстояний до указанной
        """
        c : List[PositionDistance] = []
        for calc in self.__calculated:
            pd = calc.calculated_to(pos)
            if (pd != None):
                c.append(pd)
        return c