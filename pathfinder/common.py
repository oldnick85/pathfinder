from typing import List, Optional, Set

class PositionDistance:
    """
    Класс для хранения позиции и расстояния до неё

    позиция и расстояние предполагаются константными, поэтому определены только геттеры -
    можно передавать объект, не опасаясь, что он будет изменён.
    """
    def __init__(self, position : "Position", distance : float) -> None:
        assert(distance >= 0.0)         # расстояние не может быть отрицательным
        self.__position = position      # позиция
        self.__distance = distance      # расстояние до или от этой позиции (в зависимости от контекста)
        return

    def get_position(self) -> "Position":
        return self.__position
    
    def get_distance(self) -> float:
        return self.__distance

class Position:
    """
    Класс, определяющий конкретную позицию
    """
    def __init__(self) -> None:
        return

    def __eq__(self, o : object) -> bool:
        """
        Сравнение позиций

        по умолчанию одинаковыми считаются только совпадающие позиции
        """
        return (self is o)

    def get_adjacent(self) -> Set[PositionDistance]:
        """
        Список соседних позиций с расстояниями до них относительно себя
        """
        raise NotImplementedError

class AdjanceData:
    """
    Класс, хранящий информацию о всех соседних позициях
    """
    def get_adjacent(self, position : Position) -> Set[PositionDistance]:
        """
        Список соседних позиций с расстояниями до них относительно указанной позиции
        """
        raise NotImplementedError

class Path:
    """
    Путь между позициями
    """
    def __init__(self) -> None:
        self.steps : List[Position] = []        # последовательность позиций
        self.length : float = 0.0               # длина пути
        return