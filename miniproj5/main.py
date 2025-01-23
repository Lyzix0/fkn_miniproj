import sys
from Rect import RectBuilder, TargetRect

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import QPoint, QSize
from PyQt6.QtGui import QPainter, QBrush


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(900, 700))

        self.move_pos = None
        self.builder = RectBuilder()  # Управляет списком прямоугольников

        self.target_rect = TargetRect(QPoint(100, 50), QPoint(410, 400))

        self.prev_pos: QPoint = QPoint()  # Запоминаем предыдущую позицию мыши

    def paintEvent(self, event):
        """
        Вызывается при перерисовке окна.
        Сначала рисуем target_rect, потом все прямоугольники.
        """
        painter = QPainter(self)

        # Рисуем текущим цветом (красный или зелёный).
        painter.setBrush(QBrush(self.target_rect.color))
        painter.drawRect(self.target_rect)

        # Рисуем все прямоугольники.
        for curr_rect in self.builder:
            brush = QBrush(curr_rect.color)
            painter.setBrush(brush)
            painter.drawRect(curr_rect)

    def mousePressEvent(self, event):
        """
        Обрабатываем нажатие мыши. Проверяем, попали ли в один из прямоугольников.
        Если попали, «поднимаем» его на передний план, чтобы он рисовался поверх остальных.
        """
        # Идём по списку прямоугольников с конца,
        # т.к. последний в списке — самый «верхний» при отрисовке.
        for i in reversed(range(len(self.builder.rects))):
            new_rect = self.builder.rects[i]

            # Проверяем, попали ли координаты клика (event.pos())
            # внутрь данного прямоугольника.
            if new_rect.contains(event.pos()):
                # Запоминаем индекс (i) — это будет выбранный прямоугольник:
                self.builder.set_current_rect(i)

                # Удаляем прямоугольник из текущей позиции i
                # (затем добавим в конец списка, чтобы он стал «верхним»).
                self.builder.erase_rect(i)

                # Добавляем тот же прямоугольник в конец списка:
                self.builder.add_rect(new_rect)

                # Текущий выбранный — теперь последний в списке (индекс = len - 1).
                self.builder.set_current_rect(len(self.builder.rects) - 1)

                # Запоминаем позицию мыши, чтобы потом вычислять смещения.
                self.prev_pos = event.pos()

                self.update()
                return  # Выходим, т.к. нашли самый верхний прямоугольник

        # Если мышкой не попали ни в один прямоугольник, сбрасываем текущий индекс
        self.builder.set_current_rect(None)

    def mouseMoveEvent(self, event):
        """
        Если у нас есть выбранный прямоугольник, двигаем его за мышью,
        затем проверяем, не находится ли хоть один в контейнере.
        """
        # Проверяем, есть ли текущий выбранный прямоугольник
        if self.builder.current_rect is not None:
            current_rect = self.builder.rects[self.builder.current_rect]

            # Вычисляем вектор смещения:
            move_pos = event.pos() - self.prev_pos

            # Переносим прямоугольник на это смещение:
            current_rect.move(move_pos)

            # Обновляем предыдущую позицию мыши
            self.prev_pos = event.pos()

            # Проверяем, есть ли хоть один прямоугольник внутри контейнера
            self.target_rect.check_rects_inside(self.builder.rects)

            # Обновляем окно
            self.update()

    def mouseReleaseEvent(self, event):
        """При отпускании мыши просто сбрасываем prev_pos и перерисовываем окно."""
        self.prev_pos = QPoint()
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    app.exec()
