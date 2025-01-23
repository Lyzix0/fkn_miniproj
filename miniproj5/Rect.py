from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtGui import QColor


class MovableRect(QRect):
    """
    Класс, представляющий прямоугольник, который можно перемещать
    (через метод move) и окрашивать (цвет хранится в self.color).
    """
    def __init__(
        self, begin: QPoint, end: QPoint, color: QColor = None, *args, **kwargs
    ):
        """
        :param begin: Координаты верхнего левого угла (QPoint)
        :param end: Координаты правого нижнего угла (QPoint)
        :param color: Цвет прямоугольника (QColor)
        """
        super().__init__(*args, **kwargs)

        # Запоминаем исходные точки
        self.begin = begin
        self.end = end

        # Если цвет не задан, используем чёрный
        if not color:
            color = QColor(0, 0, 0, 255)
        self.color = color

        self.setCoords(self.begin, self.end)

    def setCoords(self, begin: QPoint, end: QPoint, **kwargs):
        """Устанавливает координаты прямоугольника, используя"""
        return super().setCoords(begin.x(), begin.y(), end.x(), end.y())

    def move(self, point: QPoint):
        """Перемещает (сдвигает) прямоугольник на заданный вектор point,"""
        self.begin += point
        self.end += point
        self.setCoords(self.begin, self.end)

    def str(self):
        return f"({self.begin.x()}, {self.begin.y()})"


class RectBuilder:
    """
    Класс для управления коллекцией MovableRect.
    Хранит список прямоугольников self._rects,
    а также индекс текущего выбранного прямоугольника.
    """
    def __init__(self):
        self._rects = []
        # Индекс "текущего" (выбранного) прямоугольника
        self._current_rect = None

        # Создаём несколько тестовых прямоугольников
        rect1 = MovableRect(
            QPoint(500, 450), QPoint(600, 500), color=QColor(41, 52, 100)
        )
        rect2 = MovableRect(
            QPoint(530, 160), QPoint(630, 260), color=QColor(255, 255, 1)
        )
        rect3 = MovableRect(
            QPoint(700, 100), QPoint(800, 200), color=QColor(100, 255, 1)
        )

        # Добавляем созданные прямоугольники в общий список.
        self.rects.append(rect1)
        self.rects.append(rect2)
        self.rects.append(rect3)

    def add_rect(self, new_rect: MovableRect):
        self._rects.append(new_rect)

    def insert_rect(self, i: int, new_rect: MovableRect):
        """Вставить прямоугольник в позицию i в списке."""
        self._rects.insert(i, new_rect)

    def erase_rect(self, rect_id: int):
        """Удалить прямоугольник из списка по индексу"""
        self._rects.pop(rect_id)

    def set_current_rect(self, rect_id: int | None):
        self._current_rect = rect_id

    @property
    def rects(self):
        return self._rects

    @property
    def current_rect(self):
        return self._current_rect

    def __iter__(self):
        return iter(self._rects)


class TargetRect(QRect):
    """
    Класс «контейнерного» прямоугольника, который красится в зелёный,
    если внутри него (полностью) находится хотя бы один MovableRect.
    """

    def __init__(self, top_left: QPoint, bottom_right: QPoint):
        super().__init__(top_left, bottom_right)
        self.color = QColor("red")  # Исходно — красный

    def check_rects_inside(self, rect_list: list[MovableRect]):
        """
        Проверяем, помещается ли хотя бы один прямоугольник из rect_list
        целиком внутри данного TargetRect.
        Если да, закрашиваемся в зелёный, иначе — в красный.
        """
        inside_any = False
        for rect in rect_list:
            # Полное вхождение: верхняя левая и нижняя правая точки
            # MovableRect должны быть внутри TargetRect.
            if self.contains(rect.topLeft()) and self.contains(rect.bottomRight()):
                inside_any = True
                break

        if inside_any:
            self.color = QColor("green")
        else:
            self.color = QColor("red")
